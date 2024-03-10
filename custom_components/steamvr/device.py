"""The SteamVR device classes."""

from dataclasses import dataclass, field
from enum import Enum


class VRDeviceActivityLevel(Enum):
    """Enum representing the activity level of a VR device."""

    unknown = -1
    idle = 0
    user_interaction = 1
    user_interaction_timeout = 2
    standby = 3
    idle_timeout = 4


@dataclass
class VRController:
    """Dataclass representing a VR controller."""

    is_connected: bool = False
    battery_percentage: int | None = None
    is_charging: bool | None = None


@dataclass
class VRState:
    """Dataclass representing the state of the VR system."""

    type: str = "state"
    is_openvr_connected: bool = False
    hmd_activity_level: VRDeviceActivityLevel = VRDeviceActivityLevel.unknown
    current_application_key: str | None = None
    current_application_name: str | None = None
    right_controller: VRController = field(default_factory=lambda: VRController(False))
    left_controller: VRController = field(default_factory=lambda: VRController(False))
    error: str | None = None
