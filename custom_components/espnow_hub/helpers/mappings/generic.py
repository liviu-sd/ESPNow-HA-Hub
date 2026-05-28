from homeassistant.components.sensor import (
    SensorStateClass,
    SensorDeviceClass,
)

from homeassistant.components.binary_sensor import BinarySensorDeviceClass

from homeassistant.components.switch import SwitchDeviceClass

from homeassistant.const import (
    UnitOfPressure,
    UnitOfTemperature,
    UnitOfPower,
    UnitOfEnergy,
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
)

from .cayennelpp_sensors import CayenneLPPSensor

BINARY_SENSOR_DESCRIPTIONS: dict[str, CayenneLPPSensor] = {
    "presence": CayenneLPPSensor(
        key="presence",
        name="Presence",
        device_class=BinarySensorDeviceClass.PRESENCE,
    ),
}

SWITCH_DESCRIPTIONS: dict[str, CayenneLPPSensor] = {
    "switch": CayenneLPPSensor(
        key="switch",
        name="Switch",
        device_class=SwitchDeviceClass.SWITCH,
    ),
}

SENSOR_DESCRIPTIONS: dict[str, CayenneLPPSensor] = {
    "concentration": CayenneLPPSensor(
        key="concentration",
        name="Concentration",
        state_class=SensorStateClass.MEASUREMENT,
        unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        icon="mdi:gauge",
    ),
    "energy": CayenneLPPSensor(
        key="energy",
        name="Energy",
        device_class=SensorDeviceClass.ENERGY,
    ),
    "generic": CayenneLPPSensor(
        key="generic",
        name="Generic",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "humidity": CayenneLPPSensor(
        key="humidity",
        name="Humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
    ),
    "power": CayenneLPPSensor(
        key="power",
        name=" Power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "pressure": CayenneLPPSensor(
        key="pressure",
        name="Pressure",
        device_class=SensorDeviceClass.ATMOSPHERIC_PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPressure.HPA,
    ),
    "temperature": CayenneLPPSensor(
        key="temperature",
        name="Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    "time": CayenneLPPSensor(
        key="time",
        name="Time",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
}
