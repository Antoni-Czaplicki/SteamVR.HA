"""Constants for the SteamVR integration."""

from enum import IntFlag

DOMAIN = "steamvr"

OPENVR_EVENTS_URL = (
    "https://github.com/ValveSoftware/openvr/blob/master/headers/openvr_api.json#L385"
)


class SteamVRBinarySensorFeature(IntFlag):
    """Supported features for SteamVR binary sensors."""

    EVENTS = 1
