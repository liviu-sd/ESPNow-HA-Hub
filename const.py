"""Constants for ESPNow Hub."""

from typing import Final

from homeassistant.const import Platform

DOMAIN = "espnow_hub"
EVENT_TYPE = "esphome.espnow_message"

DEFAULT_PLATFORMS: Final[list[Platform]] = [
    Platform.SENSOR,
]


