"""Notify entity for SteamVR."""

from __future__ import annotations

import json
from typing import Any

import voluptuous as vol

from homeassistant.components.notify import NotifyEntity, NotifyEntityFeature
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv, entity_platform
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import SteamVRConfigEntry, SteamVRCoordinator
from .const import DOMAIN

DEFAULT_TITLE = "Home Assistant"

SEND_NOTIFICATION_SCHEMA = {
    vol.Required("message"): cv.string,
    vol.Optional("title"): cv.string,
    vol.Optional("image_url"): cv.string,
    vol.Optional("image_path"): cv.string,
    vol.Optional("image_data"): cv.string,
    vol.Optional("custom_properties"): dict,
}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: SteamVRConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the SteamVR notify entity."""
    async_add_entities([SteamVRNotifyEntity(config_entry, config_entry.runtime_data)])

    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        "send_notification",
        SEND_NOTIFICATION_SCHEMA,
        "async_send_rich_notification",
    )


class SteamVRNotifyEntity(NotifyEntity):
    """SteamVR notify entity."""

    _attr_has_entity_name = True
    _attr_translation_key = "notify"
    _attr_supported_features = NotifyEntityFeature.TITLE
    _attr_icon = "mdi:bell"

    def __init__(
        self, config_entry: SteamVRConfigEntry, coordinator: SteamVRCoordinator
    ) -> None:
        """Initialize the notify entity."""
        self.coordinator = coordinator
        self._attr_unique_id = f"{config_entry.entry_id}_notify"
        self._config_entry_id = config_entry.entry_id
        self._device_name = f"VR Status ({config_entry.title})"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, f"{self._config_entry_id}_vr_status")},
            name=self._device_name,
        )

    async def _send_payload(self, payload: dict[str, Any]) -> None:
        """Send a notification payload to the Agent."""
        if self.coordinator.websocket is None:
            raise HomeAssistantError("SteamVR is not connected.")
        try:
            await self.coordinator.websocket.send(json.dumps(payload))
        except (AttributeError, ConnectionError) as err:
            raise HomeAssistantError("SteamVR is not connected.") from err

    async def async_send_message(
        self, message: str, title: str | None = None
    ) -> None:
        """Send a basic notification to the headset."""
        await self._send_payload(
            {
                "basicTitle": title or DEFAULT_TITLE,
                "basicMessage": message,
            }
        )

    async def async_send_rich_notification(
        self,
        message: str,
        title: str | None = None,
        image_url: str | None = None,
        image_path: str | None = None,
        image_data: str | None = None,
        custom_properties: dict[str, Any] | None = None,
    ) -> None:
        """Send a notification that may include an image attachment."""
        payload: dict[str, Any] = {
            "basicTitle": title or DEFAULT_TITLE,
            "basicMessage": message,
        }
        if image_url is not None:
            payload["imageUrl"] = image_url
        if image_path is not None:
            payload["imagePath"] = image_path
        if image_data is not None:
            payload["imageData"] = image_data
        if custom_properties is not None:
            payload["customProperties"] = custom_properties
        await self._send_payload(payload)
