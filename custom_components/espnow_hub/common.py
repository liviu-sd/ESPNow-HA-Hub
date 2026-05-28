from homeassistant.core import HomeAssistant
from homeassistant.const import SIGNAL_STRENGTH_DECIBELS_MILLIWATT
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import (
    format_mac,
    async_get as async_get_device_registry,
    DeviceInfo,
    CONNECTION_NETWORK_MAC,
    DeviceEntry,
)

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
    BinarySensorDeviceClass,
)

from homeassistant.components.sensor import (
    SensorEntityDescription,
    EntityCategory,
    SensorStateClass,
    SensorDeviceClass,
)
from .const import DOMAIN

COMMON_ENTITY_DESCRIPTIONS: tuple[
    BinarySensorEntityDescription | SensorEntityDescription, ...
] = [
    # SensorEntityDescription(
    #     key="debug",
    #     name="Raw data",
    #     entity_category=EntityCategory.DIAGNOSTIC,
    #     entity_registry_enabled_default=False,
    #     entity_registry_visible_default=False,
    #     icon="mdi:message-processing-outline",
    # ),
    SensorEntityDescription(
        key="rssi",
        name="RSSI",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=True,  # important if false update state wil faul
    ),
]


def get_DeviceEntry(
    hass: HomeAssistant, entry: ConfigEntry, device_mac: str
) -> tuple[DeviceEntry, DeviceInfo, str]:
    # entity_registry = async_get_entity_registry(hass)
    device_registry = async_get_device_registry(hass)

    mac_safe = format_mac(device_mac)
    device_entry = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        connections={(CONNECTION_NETWORK_MAC, device_mac)},
        identifiers={(DOMAIN, mac_safe)},
        manufacturer="Liviu S. D.",
        model="ESPNow",
        name=f"ESPNow Device {device_mac}",
    )

    device_info = DeviceInfo(
        connections={(CONNECTION_NETWORK_MAC, device_mac)},
        identifiers={(DOMAIN, mac_safe)},
        manufacturer="Liviu S. D.",
        model="ESPNow",
        name=f"ESPNow Device {device_mac}",
    )

    return (
        device_registry,
        device_info,
        mac_safe,
    )
