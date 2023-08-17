from __future__ import annotations

from homeassistant.components.sensor import (
    ENTITY_ID_FORMAT,
    SensorDeviceClass,
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant, callback

from . import SteamVRCoordinator

try:
    from homeassistant.helpers.device_registry import DeviceInfo
except ImportError:
    from homeassistant.helpers.entity import DeviceInfo

from homeassistant.helpers.entity import async_generate_entity_id
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .device import VRDeviceActivityLevel


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up entry."""
    coordinator = hass.data[DOMAIN][f"{config_entry.entry_id}_coordinator"]
    async_add_entities(
        [
            HMDSensor(
                config_entry,
                coordinator,
                async_generate_entity_id(
                    ENTITY_ID_FORMAT, f"{config_entry.title}_headset", hass=hass
                ),
            ),
            VRControllerBatterySensor(
                config_entry,
                coordinator,
                "right",
                async_generate_entity_id(
                    ENTITY_ID_FORMAT,
                    f"{config_entry.title}_right_controller_battery",
                    hass=hass,
                ),
            ),
            VRControllerBatterySensor(
                config_entry,
                coordinator,
                "left",
                async_generate_entity_id(
                    ENTITY_ID_FORMAT,
                    f"{config_entry.title}_left_controller_battery",
                    hass=hass,
                ),
            ),
            VRGameSensor(
                config_entry,
                coordinator,
                async_generate_entity_id(
                    ENTITY_ID_FORMAT,
                    f"{config_entry.title}_game",
                    hass=hass,
                ),
            ),
        ]
    )


class HMDSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    def __init__(
        self, config_entry: ConfigEntry, coordinator: SteamVRCoordinator, entity_id: str
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_name = "Headset status"
        self.entity_id = entity_id
        self._attr_icon = "mdi:safety-goggles"
        self._attr_unique_id = f"{config_entry.entry_id}_HMDSensor"
        self.device_name = f"VR Headset ({config_entry.title})"
        self.config_entry_id = config_entry.entry_id
        self._attr_translation_key = "vr_status"

        super().__init__(coordinator)

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, f"{self.config_entry_id}_vr_headset")
            },
            name=self.device_name,
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = VRDeviceActivityLevel(
            self.coordinator.data.hmd_activity_level
        ).name
        self._attr_extra_state_attributes = {
            "hmd_activity_level": self.coordinator.data.hmd_activity_level
        }
        super()._handle_coordinator_update()


class VRControllerBatterySensor(CoordinatorEntity, SensorEntity):
    """Representation of a VR Controller Battery Sensor."""

    def __init__(
        self,
        config_entry: ConfigEntry,
        coordinator: SteamVRCoordinator,
        controller_side: str,
        entity_id: str,
    ) -> None:
        """Initialize the VR Controller Battery Sensor."""
        self.coordinator = coordinator
        self.entity_id = entity_id
        self.controller_side = controller_side
        self._attr_name = f"{controller_side.capitalize()} Controller Battery"
        self._attr_unique_id = (
            f"{config_entry.entry_id}_{controller_side}_ControllerBattery"
        )
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_native_unit_of_measurement = PERCENTAGE
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
                (
                    DOMAIN,
                    f"{self.config_entry_id}_{self.controller_side}_controller",
                )
            },
            name=self.device_name,
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        controller_data = (
            self.coordinator.data.right_controller
            if self.controller_side == "right"
            else self.coordinator.data.left_controller
        )
        self._attr_native_value = controller_data.battery_percentage
        super()._handle_coordinator_update()


class VRGameSensor(CoordinatorEntity, SensorEntity):
    """Representation of a VR Game Sensor."""

    def __init__(
        self, config_entry: ConfigEntry, coordinator: SteamVRCoordinator, entity_id: str
    ) -> None:
        """Initialize the VR Game Sensor."""
        self.coordinator = coordinator
        self._attr_name = "VR Game"
        self.entity_id = entity_id
        self._attr_icon = "mdi:controller"
        self._attr_unique_id = f"{config_entry.entry_id}_VRGameSensor"
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

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        state_data = self.coordinator.data
        self._attr_native_value = state_data.current_application_name
        self._attr_extra_state_attributes = {
            "current_application_key": state_data.current_application_key,
        }
        super()._handle_coordinator_update()
