from homeassistant.components.sensor import (
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.const import (
    UnitOfPressure,
    UnitOfTemperature,
    UnitOfPower,
    UnitOfEnergy,
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
)

from .cayennellp_sensors import CayenneLLPSEnsor

SENSOR_DESCRIPTIONS: dict[str, CayenneLLPSEnsor] = {
    "concentration": CayenneLLPSEnsor(
        key="concentration",
        name="Concentration",
        state_class=SensorStateClass.MEASUREMENT,
        unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        icon="mdi:gauge",
    ),
    "energy": CayenneLLPSEnsor(
        key="energy",
        name="Energy",
        device_class=SensorDeviceClass.ENERGY,
    ),
    "generic": CayenneLLPSEnsor(
        key="generic",
        name="Generic",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "humidity": CayenneLLPSEnsor(
        key="humidity",
        name="Humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
    ),
    "power": CayenneLLPSEnsor(
        key="power",
        name=" Power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "pressure": CayenneLLPSEnsor(
        key="pressure",
        name="Pressure",
        device_class=SensorDeviceClass.ATMOSPHERIC_PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPressure.HPA,
    ),
    "temperature": CayenneLLPSEnsor(
        key="temperature",
        name="Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    "time": CayenneLLPSEnsor(
        key="time",
        name="Time",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
}
