"""Support for SteamVR binary buttons."""
from __future__ import annotations

import json

from homeassistant.components.button import (
    ENTITY_ID_FORMAT,
    ButtonDeviceClass,
    ButtonEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import SteamVRCoordinator

try:
    from homeassistant.helpers.device_registry import DeviceInfo
except ImportError:
    from homeassistant.helpers.entity import DeviceInfo

from homeassistant.helpers.entity import async_generate_entity_id
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up entry."""
    coordinator = hass.data[DOMAIN][f"{config_entry.entry_id}_coordinator"]
    async_add_entities(
        [
            VRControllerIdentifyButton(
                config_entry,
                coordinator,
                "right",
                async_generate_entity_id(
                    ENTITY_ID_FORMAT,
                    f"{config_entry.title}_right_controller_identify",
                    hass=hass,
                ),
            ),
            VRControllerIdentifyButton(
                config_entry,
                coordinator,
                "left",
                async_generate_entity_id(
                    ENTITY_ID_FORMAT,
                    f"{config_entry.title}_left_controller_identify",
                    hass=hass
                ),
            ),
        ]
    )


class VRControllerIdentifyButton(ButtonEntity):
    """Representation of a VR Controller Identify Button (quick vibration)."""

    def __init__(
        self,
        config_entry: ConfigEntry,
        coordinator: SteamVRCoordinator,
        controller_side: str,
        entity_id: str,
    ) -> None:
        """Initialize the VR Controller Identify Button."""
        self.coordinator = coordinator
        self.controller_side = controller_side
        self._attr_name = f"{controller_side.capitalize()} Controller Identify"
        self.entity_id = entity_id
        self._attr_device_class = ButtonDeviceClass.IDENTIFY
        self._attr_icon = "mdi:vibrate"
        self._attr_unique_id = (
            f"{config_entry.entry_id}_{controller_side}_ControllerIdentify"
        )
        self.device_name = (
            f"{controller_side.capitalize()} Controller ({config_entry.title})"
        )
        self.config_entry_id = config_entry.entry_id

        super().__init__()

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                (DOMAIN, f"{self.config_entry_id}_{self.controller_side}_controller")
            },
            name=self.device_name,
        )


    async def async_press(self) -> None:
        """Handle the button press."""
        payload = {
            "type": "command",
            "command": f"vibrate_controller_{self.controller_side}"
        }

        await self.coordinator.websocket.send(json.dumps(payload))
