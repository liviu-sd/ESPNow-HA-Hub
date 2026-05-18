from dataclasses import dataclass, field

from homeassistant.components.sensor import (
    SensorEntityDescription,
    SensorStateClass,
    SensorDeviceClass,
    EntityCategory,
)


@dataclass
class CayenneLLPSEnsor:
    key: str
    name: str
    device_class: SensorDeviceClass | None = None
    state_class: SensorStateClass | None = None
    unit_of_measurement: str | None = None
    native_unit_of_measurement: str | None = None
    icon: str | None = None
    entity_category: EntityCategory | None = None
    has_entity_name: bool = True  # False

    def getSensorEntityDescription(
        self,
        new_key: str | None = None,
        entity_category: EntityCategory | None = None,
        has_entity_name: bool | None = None,
    ) -> SensorEntityDescription:
        return SensorEntityDescription(
            key=new_key if new_key else self.key,
            name=self.name,
            device_class=self.device_class,
            state_class=self.state_class,
            native_unit_of_measurement=self.native_unit_of_measurement,
            icon=self.icon,
            has_entity_name=(
                has_entity_name if has_entity_name else self.has_entity_name
            ),
            entity_category=(
                entity_category if entity_category else self.entity_category
            ),
        )
