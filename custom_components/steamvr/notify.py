"""Support for SteamVR Notifications notification."""

from __future__ import annotations

import json
from typing import Any

from homeassistant.components.notify import (
    ATTR_DATA,
    ATTR_TITLE,
    ATTR_TITLE_DEFAULT,
    BaseNotificationService,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType


def get_service(
    hass: HomeAssistant,
    config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None,
) -> SteamVRNotificationService:
    """Get the file notification service."""
    if discovery_info is None:
        raise ValueError("Discovery info is missing.")

    entry = hass.config_entries.async_get_entry(discovery_info["entry_id"])
    if entry is None:
        raise ValueError("Config entry not found.")
    return SteamVRNotificationService(entry.runtime_data)


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
                if key in ["imageData", "imagePath", "imageUrl", "customProperties"]:
                    payload[key] = val

        try:
            await self.coordinator.websocket.send(json.dumps(payload))
        except AttributeError as err:
            raise HomeAssistantError("SteamVR is not connected.") from err
        except ConnectionError as err:
            raise HomeAssistantError("SteamVR is not connected.") from err
        except Exception as err:
            raise HomeAssistantError("An unknown error occurred.") from err
