"""Tests for SteamVR event name handling."""
# ruff: noqa: INP001

from custom_components.steamvr.utils import (
    VR_EVENT_MAPPING,
    VR_EVENT_NAMES,
    denormalize_vr_event_name,
    normalize_vr_event_name,
)


def test_event_names_round_trip() -> None:
    """Test all canonical Agent event names round-trip."""
    assert len(VR_EVENT_MAPPING) == len(VR_EVENT_NAMES)

    for agent_name in VR_EVENT_NAMES:
        home_assistant_name = normalize_vr_event_name(agent_name)
        assert denormalize_vr_event_name(home_assistant_name) == agent_name


def test_unknown_event_name_is_preserved() -> None:
    """Test future Agent event names pass through unchanged."""
    assert normalize_vr_event_name("VREvent_FutureEvent") == "VREvent_FutureEvent"
    assert denormalize_vr_event_name("vr-event-future-event") == (
        "vr-event-future-event"
    )
