from __future__ import annotations
import re

from homeassistant.components.sensor import EntityCategory

# from homeassistant.config_entries import ConfigEntry

from .mappings.cayennellp_sensors import CayenneLLPSEnsor

# from .mappings.bme68x import SENSOR_DESCRIPTIONS as BME68x_SENSORS
from .mappings.generic import SENSOR_DESCRIPTIONS as GENERIC_SENSORS

from ..const import DOMAIN
from .const import (
    ESPNOW_CONFIG_CHANNELS,
    ESPNOW_DIAGNOSTIC_CHANNELS,
    ESPNOW_SYS_INFO_CHANNEL,
    ESPNOW_SPECIAL_SENSORS,
)


def getBrandedSensor(
    name: str, all_sensors_data: dict = None
) -> tuple[CayenneLLPSEnsor | None, int | None]:
    r = re.split(r"_(?=\d)", name)
    sensor = r[0]
    channel = int(r[1]) if len(r) > 1 else None

    if all_sensors_data:
        # ckeck if know brand
        if (
            brand_code := all_sensors_data.get(f"generic_{ESPNOW_SYS_INFO_CHANNEL}")
        ) and (brand := ESPNOW_SPECIAL_SENSORS.get(brand_code)):
            if name in brand.keys():
                return brand[name], channel, False

    return (GENERIC_SENSORS.get(sensor), channel, True)


def get_sensor(
    name: str, all_sensors_data: dict = None
) -> tuple[CayenneLLPSEnsor | None, str | None]:

    sensor, channel, isGeneric = getBrandedSensor(name, all_sensors_data)

    if sensor and isGeneric:
        # set entity category
        if channel in ESPNOW_CONFIG_CHANNELS:
            sensor.entity_category = EntityCategory.CONFIG
        elif channel in ESPNOW_DIAGNOSTIC_CHANNELS + [ESPNOW_SYS_INFO_CHANNEL]:
            sensor.entity_category = EntityCategory.DIAGNOSTIC

    return sensor, channel
