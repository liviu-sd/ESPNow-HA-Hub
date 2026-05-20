"""Platform for ESPNow Hub sensor integration."""

from __future__ import annotations
from datetime import datetime, timezone

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    EntityCategory,
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.const import SIGNAL_STRENGTH_DECIBELS_MILLIWATT
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, Event, callback
from homeassistant.helpers.device_registry import (
    format_mac,
    async_get as async_get_device_registry,
    DeviceInfo,
    CONNECTION_NETWORK_MAC,
    DeviceEntry,
)
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry

from homeassistant.helpers.entity_platform import AddEntitiesCallback
import homeassistant.util.dt as dt_util  # For timezone conversion

from .const import (
    DOMAIN,
    EVENT_TYPE,
)

from .helpers import supported_sensors

COMMON_SENSOR_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = [
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


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the ESPNow Hub sensor platform."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {"devices": {}}

    @callback
    def handle_event(event: Event):
        hass.async_create_task(
            _async_handle_event(hass, event, entry, async_add_entities)
        )

    hass.bus.async_listen(event_type=EVENT_TYPE, listener=handle_event)


async def _async_handle_event(
    hass: HomeAssistant,
    event: Event,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Handle an ESPNow event and create/update sensors."""

    event_data = event.data
    sender_data: dict[str, any] = event_data.get("sender_data")
    sender_mac = event_data.get("sender")
    rssi = event_data.get("rssi")

    if not sender_mac or not sender_data:
        return

    sender_safe = format_mac(sender_mac)  # sender_mac.replace(":", "")

    # entity_registry = async_get_entity_registry(hass)
    device_registry = async_get_device_registry(hass)

    device_entry: DeviceEntry = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        connections={(CONNECTION_NETWORK_MAC, sender_mac)},
        identifiers={(DOMAIN, sender_safe)},
        manufacturer="Liviu S. D.",
        model="ESPNow",
        name=f"ESPNow Device {sender_mac}",
    )

    device_info: DeviceInfo = DeviceInfo(
        connections={(CONNECTION_NETWORK_MAC, sender_mac)},
        identifiers={(DOMAIN, sender_safe)},
        manufacturer="Liviu S. D.",
        model="ESPNow",
        name=f"ESPNow Device {sender_mac}",
    )

    new_entities_discovered = False

    for k, v in sorted(sender_data.items(), key=lambda item: item[0]):
        sensor_description, suffix = supported_sensors.get_sensor(k, sender_data)

        if sensor_description:
            if sender_safe not in hass.data[DOMAIN]["devices"]:
                hass.data[DOMAIN]["devices"][sender_safe] = {}

                for common_entity in COMMON_SENSOR_DESCRIPTIONS:
                    kcommon_entity = common_entity.key
                    hass.data[DOMAIN]["devices"][sender_safe][kcommon_entity] = (
                        ESPNowSensor(
                            description=common_entity,
                            device_info=device_info,
                            sender_mac=sender_mac,
                            sender_safe=sender_safe,
                        )
                    )

            entity_state = None
            if sensor_description.device_class == "timestamp":
                entity_state = datetime.fromtimestamp(sender_data[k], tz=timezone.utc)
            else:
                entity_state = sender_data[k]

            if k not in hass.data[DOMAIN]["devices"][sender_safe]:
                new_entity = ESPNowSensor(
                    description=sensor_description.getSensorEntityDescription(
                        new_key=k
                    ),
                    device_info=device_info,
                    sender_mac=sender_mac,
                    sender_safe=sender_safe,
                )
                new_entities_discovered = True  # .append(new_entity)
                hass.data[DOMAIN]["devices"][sender_safe][k] = new_entity
            # else:
            # hass.data[DOMAIN]["devices"][sender_safe][k]._attr_state = entity_state
            # hass.data[DOMAIN]["devices"][sender_safe][k].async_write_ha_state()

            hass.data[DOMAIN]["devices"][sender_safe][k]._attr_state = entity_state

    for common_entity in COMMON_SENSOR_DESCRIPTIONS:
        entity_state = event_data.get(common_entity.key)
        hass.data[DOMAIN]["devices"][sender_safe][
            common_entity.key
        ]._attr_state = entity_state

    if new_entities_discovered:
        async_add_entities(hass.data[DOMAIN]["devices"][sender_safe].values())

    for entity in hass.data[DOMAIN]["devices"][sender_safe].values():
        entity.async_write_ha_state()


class ESPNowSensor(SensorEntity):
    _attr_has_entity_name = True  # Use entity description name as the base

    def __init__(
        self,
        description: SensorEntityDescription,
        device_info: DeviceInfo,
        sender_mac: str,
        sender_safe: str,
    ):

        self._attr_device_info = device_info
        self.entity_description = description

        """Initialize the sensor."""
        self._sender = sender_mac
        self._sender_safe = sender_safe

        self._attr_unique_id = f"{DOMAIN}_{sender_safe}_{description.key}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._attr_state

    @property
    def extra_state_attributes(self) -> dict[str, any] | None:
        """Return entity specific state attributes."""

        local_valid_time = dt_util.as_local(dt_util.now())
        return {"last_updated": local_valid_time.isoformat()}
