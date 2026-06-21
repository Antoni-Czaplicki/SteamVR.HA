"""The SteamVR integration."""

import asyncio
import json
import logging
from contextlib import suppress
from dataclasses import fields

import homeassistant.helpers.config_validation as cv
import websockets
from homeassistant.components import persistent_notification
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import discovery
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN
from .device import VRDeviceActivityLevel, VRState
from .utils import denormalize_vr_event_name, normalize_vr_event_name

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.NOTIFY, Platform.SENSOR, Platform.BINARY_SENSOR, Platform.BUTTON]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


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
        coordinator = hass.data[DOMAIN].pop(f"{entry.entry_id}_coordinator", None)
        if coordinator:
            await coordinator.async_shutdown()

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
        self._websocket_task = None
        self._stopping = False
        self.entry_id = config_entry.entry_id
        self.device_id = None

    async def _async_update_data(self):
        if self._websocket_task is None or self._websocket_task.done():
            self._stopping = False
            self._websocket_task = self.config_entry.async_create_background_task(
                self.hass, self.run_server(), "steam_vr_ws"
            )
        return VRState(is_openvr_connected=False)

    async def run_server(self):
        """Connect to the websocket server."""
        try:
            async for websocket in websockets.connect(self.url):
                if self._stopping:
                    break

                should_stop = False

                try:
                    self.websocket = websocket
                    async for message in websocket:
                        if self._stopping:
                            should_stop = True
                            break
                        await self.on_message(message)
                except websockets.ConnectionClosed:
                    if self._stopping:
                        should_stop = True
                    else:
                        self.async_set_updated_data(VRState(is_openvr_connected=False))
                        continue
                finally:
                    if self.websocket is websocket:
                        self.websocket = None

                    self.async_set_updated_data(VRState(is_openvr_connected=False))

                if should_stop or self._stopping:
                    break
        except asyncio.CancelledError:
            raise

    async def async_shutdown(self):
        """Stop the websocket connection and background task."""
        self._stopping = True

        if self.websocket is not None:
            await self.websocket.close()

        if self._websocket_task is not None and not self._websocket_task.done():
            self._websocket_task.cancel()
            with suppress(asyncio.CancelledError):
                await self._websocket_task

        self._websocket_task = None
        self.websocket = None
        self.async_set_updated_data(VRState(is_openvr_connected=False))

    async def on_message(self, message: str | bytes):
        """Handle incoming messages from the websocket server.

        Args:
            message (str | bytes): The incoming message.

        """
        message_dict = json.loads(message)
        if "type" not in message_dict:
            # Support for legacy client, will be removed in the future
            if (
                "is_openvr_connected" in message_dict
                and message_dict["is_openvr_connected"]
            ):
                if self.config_entry.options.get(
                    "replace_standby_with_idle", False
                ) and (
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
                if self.config_entry.options.get(
                    "replace_standby_with_idle", False
                ) and (
                    message_dict["hmd_activity_level"]
                    == VRDeviceActivityLevel.standby.value
                ):
                    message_dict["hmd_activity_level"] = VRDeviceActivityLevel.idle
                vr_state = dataclass_from_dict(VRState, message_dict)
                self.async_set_updated_data(vr_state)
                return
        if message_dict["type"] == "event":
            if message_dict[
                "event_type"
            ] == "port_changed" and self.config_entry.options.get(
                "port_auto_update", True
            ):
                entry_data = {**self.config_entry.data}
                entry_data[CONF_PORT] = message_dict["event_data"]
                self.hass.config_entries.async_update_entry(
                    self.config_entry, data=entry_data
                )
                persistent_notification.async_create(
                    self.hass,
                    f"SteamVR port has changed to {message_dict['event_data']}, configuration has been updated.",
                    "SteamVR Port Changed",
                )

                self.hass.async_create_task(
                    self.hass.config_entries.async_reload(self.config_entry.entry_id)
                )
                return
            if not self.device_id:
                device_registry = dr.async_get(self.hass)
                device_entry = device_registry.async_get_device(
                    identifiers={(DOMAIN, f"{self.entry_id}_vr_status")}
                )
                if device_entry:
                    self.device_id = device_entry.id
            if self.device_id:
                # Normalize the event type from WebSocket API format to Home Assistant format
                normalized_event_type = normalize_vr_event_name(
                    message_dict["event_type"]
                )
                event_data = {
                    "device_id": self.device_id,
                    "type": normalized_event_type,
                    "data": message_dict["event_data"],
                }
                self.hass.bus.async_fire("steamvr_event", event_data)

    async def register_event(self, event):
        """Register SteamVR event.

        Args:
            event: The event to register (in Home Assistant format).

        Raises:
            HomeAssistantError: If there is no websocket connection.

        """
        if self.websocket:
            # Convert from Home Assistant format to WebSocket API format
            websocket_event = denormalize_vr_event_name(event)
            await self.websocket.send(
                json.dumps({"type": "register_event", "command": websocket_event})
            )
        else:
            raise HomeAssistantError("No websocket connection")

    async def unregister_event(self, event):
        """Unregister SteamVR event.

        Args:
            event: The event to unregister (in Home Assistant format).

        Raises:
            HomeAssistantError: If there is no websocket connection.

        """
        if self.websocket:
            # Convert from Home Assistant format to WebSocket API format
            websocket_event = denormalize_vr_event_name(event)
            await self.websocket.send(
                json.dumps({"type": "unregister_event", "command": websocket_event})
            )
        else:
            raise HomeAssistantError("No websocket connection")


def dataclass_from_dict(_class, d):
    """Convert a dictionary to a dataclass object."""
    try:
        fieldtypes = {f.name: f.type for f in fields(_class)}
        return _class(**{f: dataclass_from_dict(fieldtypes[f], d[f]) for f in d})
    except Exception:
        return d  # Not a dataclass field
