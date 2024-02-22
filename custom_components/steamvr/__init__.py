"""The SteamVR integration."""

import json
import logging
from dataclasses import fields

import websockets
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import discovery
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN
from .device import VRController, VRDeviceActivityLevel, VRState

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.NOTIFY, Platform.SENSOR, Platform.BINARY_SENSOR, Platform.BUTTON]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the SteamVR component."""

    hass.data["steamvr_hass_config"] = config
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SteamVR from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][f"{entry.entry_id}_coordinator"] = SteamVRCoordinator(
        hass, entry, f"ws://{entry.data[CONF_HOST]}:{entry.data[CONF_PORT]}"
    )
    await hass.data[DOMAIN][f"{entry.entry_id}_coordinator"].async_refresh()
    hass.async_create_task(
        discovery.async_load_platform(
            hass,
            Platform.NOTIFY,
            DOMAIN,
            {
                CONF_HOST: entry.data[CONF_HOST],
                CONF_PORT: entry.data[CONF_PORT],
                CONF_NAME: entry.data[CONF_NAME],
                "entry_id": entry.entry_id,
            },
            hass.data["steamvr_hass_config"],
        )
    )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS[1:])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS[1:]
    ):
        await hass.data[DOMAIN][f"{entry.entry_id}_coordinator"].websocket.close()
        hass.data[DOMAIN].pop(f"{entry.entry_id}_coordinator")

    return unload_ok


class SteamVRCoordinator(DataUpdateCoordinator):
    """SteamVR coordinator."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry, url) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="SteamVR data",
        )
        self.hass = hass
        self.url = url
        self.config_entry = config_entry
        self.websocket = None

    async def _async_update_data(self):
        self.config_entry.async_create_background_task(
            self.hass, self.run_server(), "steam_vr_ws"
        )
        return VRState(is_openvr_connected=False)

    async def run_server(self):
        async for websocket in websockets.connect(self.url):
            try:
                self.websocket = websocket
                async for message in websocket:
                    await self.on_message(message)
            except websockets.ConnectionClosed:
                self.async_set_updated_data(VRState(is_openvr_connected=False))
                continue
            finally:
                self.async_set_updated_data(VRState(is_openvr_connected=False))

    async def on_message(self, message: str | bytes):
        message_dict = json.loads(message)
        if "type" not in message_dict:
            # Support for legacy client, will be removed in the future
            if (
                "is_openvr_connected" in message_dict
                and message_dict["is_openvr_connected"]
            ):
                if self.config_entry.options.get("replace_standby_with_idle", False) and (
                    message_dict["hmd_activity_level"]
                    == VRDeviceActivityLevel.standby.value
                ):
                    message_dict["hmd_activity_level"] = VRDeviceActivityLevel.idle
                vr_state = dataclass_from_dict(VRState, message_dict)
                self.async_set_updated_data(vr_state)
            # elif "error" in vr_state_dict and vr_state_dict["error"]:
            #     self.async_set_updated_data(VRState(False, error=vr_state_dict["error"]))
            return
        if message_dict["type"] == "state":
            if (
                "is_openvr_connected" in message_dict
                and message_dict["is_openvr_connected"]
            ):
                if self.config_entry.options.get("replace_standby_with_idle", False) and (
                    message_dict["hmd_activity_level"]
                    == VRDeviceActivityLevel.standby.value
                ):
                    message_dict["hmd_activity_level"] = VRDeviceActivityLevel.idle
                vr_state = dataclass_from_dict(VRState, message_dict)
                self.async_set_updated_data(vr_state)
                return
        if message_dict["type"] == "event":
            if message_dict["event_type"] == "port_changed" and self.config_entry.options.get("port_auto_update", True):
                entry_data = {**self.config_entry.data}
                entry_data[CONF_PORT] = message_dict["event_data"]
                self.hass.config_entries.async_update_entry(
                    self.config_entry, data=entry_data
                )
                self.hass.async_create_task(
                    self.hass.config_entries.async_reload(self.config_entry.entry_id)
                )
                return



def dataclass_from_dict(_class, d):
    try:
        fieldtypes = {f.name: f.type for f in fields(_class)}
        return _class(**{f: dataclass_from_dict(fieldtypes[f], d[f]) for f in d})
    except:
        return d  # Not a dataclass field
