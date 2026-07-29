"""Tests for the SteamVR config flow."""
# ruff: noqa: INP001

from unittest.mock import patch

from custom_components.steamvr.config_flow import (
    SteamVRFlowHandler,
    SteamVROptionsFlowHandler,
)
from custom_components.steamvr.const import DOMAIN

from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from tests.common import MockConfigEntry  # noqa: TID251


async def test_user_step_uses_host_as_optional_name(hass: HomeAssistant) -> None:
    """Test an omitted name falls back to the host."""
    flow = SteamVRFlowHandler()
    flow.hass = hass

    with patch.object(flow, "_async_abort_entries_match") as abort_entries_match:
        result = await flow.async_step_user(
            {
                CONF_HOST: "192.0.2.10",
                CONF_PORT: "8077",
            }
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "192.0.2.10"
    assert result["data"][CONF_NAME] == "192.0.2.10"
    abort_entries_match.assert_called_once_with(
        {
            CONF_HOST: "192.0.2.10",
            CONF_PORT: "8077",
        }
    )


def test_options_flow_does_not_assign_config_entry() -> None:
    """Test options flow construction uses Home Assistant's property."""
    entry = MockConfigEntry(domain=DOMAIN)

    flow = SteamVRFlowHandler.async_get_options_flow(entry)

    assert isinstance(flow, SteamVROptionsFlowHandler)
    assert "config_entry" not in flow.__dict__
