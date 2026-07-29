"""Action registration for SteamVR."""

import voluptuous as vol

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import config_validation as cv, service
from homeassistant.helpers.typing import VolDictType

from .const import DOMAIN, OPENVR_EVENTS_URL, SteamVRBinarySensorFeature

EVENT_SCHEMA: VolDictType = {
    vol.Required("event"): cv.string,
}

SEND_NOTIFICATION_SCHEMA: VolDictType = {
    vol.Required("message"): cv.string,
    vol.Optional("title"): cv.string,
    vol.Optional("image_url"): cv.string,
    vol.Optional("image_path"): cv.string,
    vol.Optional("image_data"): cv.string,
    vol.Optional("custom_properties"): dict,
}


@callback
def async_setup_actions(hass: HomeAssistant) -> None:
    """Register SteamVR entity actions."""
    for action in ("register_event", "unregister_event"):
        service.async_register_platform_entity_service(
            hass,
            DOMAIN,
            action,
            description_placeholders={"openvr_events_url": OPENVR_EVENTS_URL},
            entity_domain=Platform.BINARY_SENSOR,
            func=f"async_{action}",
            required_features=[SteamVRBinarySensorFeature.EVENTS],
            schema=EVENT_SCHEMA,
        )

    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        "send_notification",
        entity_domain=Platform.NOTIFY,
        func="async_send_rich_notification",
        schema=SEND_NOTIFICATION_SCHEMA,
    )
