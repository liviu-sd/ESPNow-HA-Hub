from __future__ import annotations
import re

from homeassistant.components.sensor import EntityCategory

from .mappings.cayennelpp_sensors import CayenneLPPSensor

from .mappings.generic import (
    BINARY_SENSOR_DESCRIPTIONS as GENERIC_BINARY_SENSOR,
    SENSOR_DESCRIPTIONS as GENERIC_SENSORS,
    SWITCH_DESCRIPTIONS as GENERIC_SWITCHES,
)

from ..const import DOMAIN

from .const import (
    ESPNOW_CONFIG_CHANNELS,
    ESPNOW_DIAGNOSTIC_CHANNELS,
    ESPNOW_SYS_INFO_CHANNEL,
)

from .mappings import ESPNOW_SPECIAL_SENSORS

def parse_name_channel(name: str) -> tuple[str, int]:
    r = re.split(r"_(?=\d)", name)
    ha_name = r[0]
    channel = int(r[1]) if len(r) > 1 else None
    return ha_name, channel


def get_entity_category(channel: int) -> EntityCategory | None:
    if channel in ESPNOW_CONFIG_CHANNELS:
        return EntityCategory.CONFIG
    elif channel in ESPNOW_DIAGNOSTIC_CHANNELS + [ESPNOW_SYS_INFO_CHANNEL]:
        return EntityCategory.DIAGNOSTIC

    return None


def getBrandedSensor(name: str, all_sensors_data: dict) -> CayenneLPPSensor | None:
    ret_val = None

    if all_sensors_data:
        # ckeck if know brand
        if (
            brand_code := all_sensors_data.get(f"generic_{ESPNOW_SYS_INFO_CHANNEL}")
        ) and (brand := ESPNOW_SPECIAL_SENSORS.get(brand_code)):
            if name in brand.keys():
                ret_val = brand[name]

    return ret_val


def get_sensor(
    name: str, all_sensors_data: dict = None
) -> tuple[CayenneLPPSensor | None, str | None]:
    ha_name, channel = parse_name_channel(name)

    cayenne_sensor = getBrandedSensor(name, all_sensors_data)

    if cayenne_sensor is None and (cayenne_sensor := GENERIC_SENSORS.get(ha_name)):
        cayenne_sensor.entity_category = get_entity_category(channel)

    return cayenne_sensor, channel


def get_binary_sensor(
    name: str, all_sensors_data: dict = None
) -> tuple[CayenneLPPSensor | None, str | None]:
    ha_name, channel = parse_name_channel(name)

    cayenne_sensor = getBrandedSensor(name, all_sensors_data)

    if cayenne_sensor is None and (
        cayenne_sensor := GENERIC_BINARY_SENSOR.get(ha_name)
    ):
        cayenne_sensor.entity_category = get_entity_category(channel)

    return cayenne_sensor, channel


def get_switch(
    name: str, all_sensors_data: dict = None
) -> tuple[CayenneLPPSensor | None, str | None]:
    ha_name, channel = parse_name_channel(name)

    cayenne_sensor = getBrandedSensor(name, all_sensors_data)

    if cayenne_sensor is None and (cayenne_sensor := GENERIC_SWITCHES.get(ha_name)):
        cayenne_sensor.entity_category = get_entity_category(channel)

    return cayenne_sensor, channel
