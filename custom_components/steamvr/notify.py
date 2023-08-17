"""Support for SteamVR Notifications notification."""
from __future__ import annotations

import json
import os
from typing import Any, TextIO

import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util
import voluptuous as vol
from homeassistant.components.notify import (
    ATTR_DATA,
    ATTR_TITLE,
    ATTR_TITLE_DEFAULT,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN


def get_service(
    hass: HomeAssistant,
    config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None,
) -> SteamVRNotificationService:
    """Get the file notification service."""

    return SteamVRNotificationService(
        hass.data[DOMAIN][f"{discovery_info['entry_id']}_coordinator"]
    )


class SteamVRNotificationService(BaseNotificationService):
    """Implement the notification service for the SteamVR Notifications service."""

    def __init__(self, coordinator) -> None:
        """Initialize the service."""
        self.coordinator = coordinator

    async def async_send_message(self, message: str = "", **kwargs: Any) -> None:
        """Send a notification to SteamVR."""

        payload = {
            "basicTitle": kwargs.get(ATTR_TITLE, ATTR_TITLE_DEFAULT),
            "basicMessage": message,
        }

        if data := kwargs.get(ATTR_DATA):
            # Pick out fields that should go into the notification directly vs
            # into the notification data dictionary.

            for key, val in data.items():
                if key in ["imageData", "imagePath", "customProperties"]:
                    payload[key] = val

        await self.coordinator.websocket.send(json.dumps(payload))
