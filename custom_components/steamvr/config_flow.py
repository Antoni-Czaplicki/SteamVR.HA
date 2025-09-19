"""Config flow for SteamVR integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class SteamVRFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SteamVR."""

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return SteamVROptionsFlowHandler(config_entry)

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


class SteamVROptionsFlowHandler(config_entries.OptionsFlow):
    """Options flow handler for SteamVR integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "replace_standby_with_idle",
                        default=self.config_entry.options.get(
                            "replace_standby_with_idle", False
                        ),
                    ): bool,
                    vol.Required(
                        "port_auto_update",
                        default=self.config_entry.options.get("port_auto_update", True),
                    ): bool,
                }
            ),
        )
