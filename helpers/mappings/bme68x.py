from homeassistant.components.sensor import (
    SensorStateClass,
    SensorDeviceClass,
    EntityCategory,
)

from homeassistant.const import (
    CONCENTRATION_PARTS_PER_MILLION,
)

from .cayennellp_sensors import CayenneLLPSEnsor

SENSOR_DESCRIPTIONS: dict[str, CayenneLLPSEnsor] = {
    "concentration_0": CayenneLLPSEnsor(
        key="iaq",
        name="IAQ",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:gauge",
    ),
    "concentration_1": CayenneLLPSEnsor(
        key="iaq_static",
        name="IAQ Static",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:gauge",
    ),
    "concentration_2": CayenneLLPSEnsor(
        key="co2",
        name="CO2 Equivalent",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.CO2,
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
    ),
    "concentration_3": CayenneLLPSEnsor(
        key="breath_voc_equivalent",
        name="Breath VOC Equivalent",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS_PARTS,
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
    ),
    "generic_0": CayenneLLPSEnsor(
        key="gas_resistance",
        name="Gas Resistance",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:gas-cylinder",
        native_unit_of_measurement="Ω",
    ),
    "generic_40": CayenneLLPSEnsor(
        key="iaq_accuracy",
        name="IAQ Accuracy",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:checkbox-marked-circle-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
}
