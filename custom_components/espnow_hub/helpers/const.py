from typing import Final
from enum import Enum, auto

ESPNOW_CONFIG_CHANNELS: Final[list[int]] = [
    v for v in range(50, 59)
]  # EntityCategory.CONFIG
ESPNOW_DIAGNOSTIC_CHANNELS: Final[list[int]] = [
    v for v in range(40, 49)
]  # EntityCategory.DIAGNOSTIC

ESPNOW_SYS_INFO_CHANNEL = 60
ESPNOW_SYS_CMD_CHANNEL = 61

