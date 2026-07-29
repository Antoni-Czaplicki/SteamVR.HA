"""Tests for the SteamVR integration."""
# ruff: noqa: INP001

import asyncio
import json
from unittest.mock import AsyncMock, patch

from custom_components.steamvr import (
    SteamVRCoordinator,
    async_setup,
    async_setup_entry,
    dataclass_from_dict,
)
from custom_components.steamvr.const import DOMAIN, OPENVR_EVENTS_URL
from custom_components.steamvr.device import VRController, VRState

from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from tests.common import MockConfigEntry  # noqa: TID251


async def test_actions_registered(hass: HomeAssistant) -> None:
    """Test entity actions are registered during integration setup."""
    assert await async_setup(hass, {})

    actions = hass.services.async_services()[DOMAIN]
    assert {
        "register_event",
        "send_notification",
        "unregister_event",
    } <= actions.keys()
    assert actions["register_event"].description_placeholders == {
        "openvr_events_url": OPENVR_EVENTS_URL
    }
    assert actions["unregister_event"].description_placeholders == {
        "openvr_events_url": OPENVR_EVENTS_URL
    }


async def test_setup_entry_uses_runtime_data(hass: HomeAssistant) -> None:
    """Test config entry setup stores the coordinator in runtime data."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_HOST: "127.0.0.1", CONF_PORT: "8077"},
    )
    entry.add_to_hass(hass)

    with (
        patch.object(
            SteamVRCoordinator,
            "async_config_entry_first_refresh",
            new=AsyncMock(),
        ) as first_refresh,
        patch.object(
            hass.config_entries,
            "async_forward_entry_setups",
            new=AsyncMock(),
        ) as forward_setups,
    ):
        assert await async_setup_entry(hass, entry)

    assert isinstance(entry.runtime_data, SteamVRCoordinator)
    first_refresh.assert_awaited_once()
    forward_setups.assert_awaited_once()


async def test_current_agent_state_payload(hass: HomeAssistant) -> None:
    """Test current Agent state fields produce a typed coordinator state."""
    entry = MockConfigEntry(domain=DOMAIN, data={}, options={})
    coordinator = SteamVRCoordinator(hass, entry, "ws://127.0.0.1:8077")

    await coordinator.on_message(
        json.dumps(
            {
                "type": "state",
                "is_steamvr_process_running": True,
                "is_openvr_connected": False,
                "right_controller": {"is_connected": False},
                "left_controller": {"is_connected": False},
                "future_agent_field": "ignored",
            }
        )
    )

    assert isinstance(coordinator.data, VRState)
    assert coordinator.data.is_steamvr_process_running is True
    assert coordinator.data.is_openvr_connected is False
    assert isinstance(coordinator.data.right_controller, VRController)
    assert isinstance(coordinator.data.left_controller, VRController)


def test_dataclass_parser_ignores_unknown_fields() -> None:
    """Test future Agent fields do not make the parser return a dictionary."""
    state = dataclass_from_dict(
        VRState,
        {
            "is_openvr_connected": True,
            "unknown": "value",
        },
    )

    assert isinstance(state, VRState)
    assert state.is_openvr_connected is True


async def test_coordinator_shutdown(hass: HomeAssistant) -> None:
    """Test shutdown closes the websocket and waits for task cancellation."""
    entry = MockConfigEntry(domain=DOMAIN, data={})
    coordinator = SteamVRCoordinator(hass, entry, "ws://127.0.0.1:8077")
    started = asyncio.Event()

    async def websocket_loop() -> None:
        started.set()
        await asyncio.Future()

    websocket_task = asyncio.create_task(websocket_loop())
    await started.wait()
    websocket = AsyncMock()
    coordinator._websocket_task = websocket_task  # noqa: SLF001
    coordinator.websocket = websocket

    await coordinator.async_shutdown()

    websocket.close.assert_awaited_once()
    assert websocket_task.cancelled()
    assert coordinator._websocket_task is None  # noqa: SLF001
    assert coordinator.websocket is None
    assert coordinator._shutdown_requested  # noqa: SLF001
