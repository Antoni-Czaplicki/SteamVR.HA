"""Config flow for SteamVR integration."""

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT
from homeassistant.core import callback

from .const import DOMAIN


class SteamVRFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SteamVR."""

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> SteamVROptionsFlowHandler:
        """Get the options flow for this handler."""
        return SteamVROptionsFlowHandler()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initiated by the user."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]
            name = user_input.get(CONF_NAME) or host

            user_input[CONF_NAME] = name

            self._async_abort_entries_match(
                {
                    CONF_HOST: host,
                    CONF_PORT: port,
                }
            )

            return self.async_create_entry(
                title=name,
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

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
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
