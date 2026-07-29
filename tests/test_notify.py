"""Tests for SteamVR notifications."""
# ruff: noqa: INP001

import json
from unittest.mock import AsyncMock, patch

from custom_components.steamvr import SteamVRCoordinator
from custom_components.steamvr.const import DOMAIN
from custom_components.steamvr.notify import SteamVRNotifyEntity

from homeassistant.core import HomeAssistant
from tests.common import MockConfigEntry  # noqa: TID251


async def test_send_basic_notification(hass: HomeAssistant) -> None:
    """Test sending a basic notification payload."""
    entry = MockConfigEntry(domain=DOMAIN, title="Gaming PC")
    coordinator = SteamVRCoordinator(hass, entry, "ws://127.0.0.1:8077")
    websocket = AsyncMock()
    coordinator.websocket = websocket
    entity = SteamVRNotifyEntity(entry, coordinator)

    await entity.async_send_message("Ready", title="Home")

    payload = json.loads(websocket.send.await_args.args[0])
    assert payload == {
        "basicMessage": "Ready",
        "basicTitle": "Home",
    }


async def test_send_rich_notification(hass: HomeAssistant) -> None:
    """Test sending a rich notification payload."""
    entry = MockConfigEntry(domain=DOMAIN, title="Gaming PC")
    coordinator = SteamVRCoordinator(hass, entry, "ws://127.0.0.1:8077")
    websocket = AsyncMock()
    coordinator.websocket = websocket
    entity = SteamVRNotifyEntity(entry, coordinator)

    with patch.object(entity, "_async_record_notification") as record_notification:
        await entity.async_send_rich_notification(
            "Ready",
            image_url="https://example.com/image.png",
            custom_properties={"timeout": 5},
        )

    payload = json.loads(websocket.send.await_args.args[0])
    assert payload == {
        "basicMessage": "Ready",
        "basicTitle": "Home Assistant",
        "customProperties": {"timeout": 5},
        "imageUrl": "https://example.com/image.png",
    }
    record_notification.assert_called_once_with()
