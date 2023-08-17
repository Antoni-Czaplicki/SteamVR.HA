"""Config flow for SteamVR Notifications integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class NFAndroidTVFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SteamVR."""

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initiated by the user."""
        errors = {}

        if user_input is not None:
            self._async_abort_entries_match(
                {CONF_HOST: user_input[CONF_HOST], CONF_NAME: user_input[CONF_NAME]}
            )
            if not user_input[CONF_NAME]:
                user_input[CONF_NAME] = user_input[CONF_HOST]
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input,
            )
            errors["base"] = error

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_PORT, default="8077"): str,
                    vol.Optional(CONF_NAME): str,
                }
            ),
            errors=errors,
        )
