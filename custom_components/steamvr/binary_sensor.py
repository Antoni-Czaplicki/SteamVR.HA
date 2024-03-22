"""Support for SteamVR binary sensors."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.components.binary_sensor import (
    ENTITY_ID_FORMAT,
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.helpers import config_validation as cv, entity_platform

from . import SteamVRCoordinator

try:
    from homeassistant.helpers.device_registry import DeviceInfo
except ImportError:
    from homeassistant.helpers.entity import DeviceInfo

from homeassistant.helpers.entity import Entity, async_generate_entity_id
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up entry."""
    coordinator: SteamVRCoordinator = hass.data[DOMAIN][f"{config_entry.entry_id}_coordinator"]
    async_add_entities(
        [
            VRControllerBinarySensor(
                config_entry,
                coordinator,
                "right",
                async_generate_entity_id(
                    ENTITY_ID_FORMAT,
                    f"{config_entry.title}_right_controller",
                    hass=hass,
                ),
            ),
            VRControllerChargingBinarySensor(
                config_entry,
                coordinator,
                "right",
                async_generate_entity_id(
                    ENTITY_ID_FORMAT,
                    f"{config_entry.title}_right_controller_charging",
                    hass=hass,
                ),
            ),
            VRControllerBinarySensor(
                config_entry,
                coordinator,
                "left",
                async_generate_entity_id(
                    ENTITY_ID_FORMAT, f"{config_entry.title}_left_controller", hass=hass
                ),
            ),
            VRControllerChargingBinarySensor(
                config_entry,
                coordinator,
                "left",
                async_generate_entity_id(
                    ENTITY_ID_FORMAT,
                    f"{config_entry.title}_left_controller_charging",
                    hass=hass,
                ),
            ),
            VRStatusBinarySensor(
                config_entry,
                coordinator,
                async_generate_entity_id(
                    ENTITY_ID_FORMAT,
                    f"{config_entry.title}_status",
                    hass=hass,
                ),
            ),
        ]
    )

    async def custom_register_event(entity: VRStatusBinarySensor, call: ServiceCall) -> None:
        """Register an event."""
        event = call.data["event"]
        await entity.register_event(event)

    async def custom_unregister_event(entity: VRStatusBinarySensor, call: ServiceCall) -> None:
        """Unregister an event."""
        event = call.data["event"]
        await entity.unregister_event(event)

    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        "register_event",
        {
            vol.Required('event'): cv.string,
        },
        custom_register_event,
    )
    platform.async_register_entity_service(
        "unregister_event",
        {
            vol.Required('event'): cv.string,
        },
        custom_unregister_event,
    )


class VRControllerBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a VR Controller Binary Sensor."""

    def __init__(
        self,
        config_entry: ConfigEntry,
        coordinator: SteamVRCoordinator,
        controller_side: str,
        entity_id: str,
    ) -> None:
        """Initialize the VR Controller Binary Sensor."""
        self.coordinator = coordinator
        self.controller_side = controller_side
        self._attr_name = f"{controller_side.capitalize()} Controller"
        self.entity_id = entity_id
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
        self._attr_icon = "mdi:gamepad-square"
        self._attr_unique_id = (
            f"{config_entry.entry_id}_{controller_side}_ControllerBinarySensor"
        )
        self.device_name = (
            f"{controller_side.capitalize()} Controller ({config_entry.title})"
        )
        self.config_entry_id = config_entry.entry_id

        super().__init__(coordinator)

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                (DOMAIN, f"{self.config_entry_id}_{self.controller_side}_controller")
            },
            name=self.device_name,
        )

    @property
    def is_on(self) -> bool:
        """Return True if the controller is connected, otherwise False."""
        controller_data = (
            self.coordinator.data.right_controller
            if self.controller_side == "right"
            else self.coordinator.data.left_controller
        )
        return controller_data.is_connected

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        super()._handle_coordinator_update()


class VRControllerChargingBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a VR Controller Charging Binary Sensor."""

    def __init__(
        self,
        config_entry: ConfigEntry,
        coordinator: SteamVRCoordinator,
        controller_side: str,
        entity_id: str,
    ) -> None:
        """Initialize the VR Controller Charging Binary Sensor."""
        self.coordinator = coordinator
        self.controller_side = controller_side
        self._attr_name = f"{controller_side.capitalize()} Controller Charging"
        self.entity_id = entity_id
        self._attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING
        self._attr_unique_id = (
            f"{config_entry.entry_id}_{controller_side}_ControllerCharging"
        )
        self.device_name = (
            f"{controller_side.capitalize()} Controller ({config_entry.title})"
        )
        self.config_entry_id = config_entry.entry_id

        super().__init__(coordinator)

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                (DOMAIN, f"{self.config_entry_id}_{self.controller_side}_controller")
            },
            name=self.device_name,
        )

    @property
    def is_on(self) -> bool:
        """Return True if the controller is charging."""
        controller_data = (
            self.coordinator.data.right_controller
            if self.controller_side == "right"
            else self.coordinator.data.left_controller
        )
        return controller_data.is_charging

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        super()._handle_coordinator_update()


class VRStatusBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a VR Status Binary Sensor."""

    def __init__(
        self, config_entry: ConfigEntry, coordinator: SteamVRCoordinator, entity_id: str
    ) -> None:
        """Initialize the VR Status Binary Sensor."""
        self.coordinator = coordinator
        self._attr_name = "VR Status"
        self.entity_id = entity_id
        self._attr_device_class = BinarySensorDeviceClass.RUNNING
        self._attr_unique_id = f"{config_entry.entry_id}_VRStatusBinarySensor"
        self.device_name = f"VR Status ({config_entry.title})"
        self.config_entry_id = config_entry.entry_id

        super().__init__(coordinator)

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, f"{self.config_entry_id}_vr_status")},
            name=self.device_name,
        )

    @property
    def is_on(self) -> bool:
        """Return True if VR is connected, otherwise False."""
        state_data = self.coordinator.data
        self._attr_extra_state_attributes = {
            "error": state_data.error,
        }
        return state_data.is_openvr_connected

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        super()._handle_coordinator_update()


    async def register_event(self, event: str) -> None:
        """Register an event."""
        await self.coordinator.register_event(event)

    async def unregister_event(self, event: str) -> None:
        """Unregister an event."""
        await self.coordinator.unregister_event(event)
