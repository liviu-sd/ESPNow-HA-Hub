"""The ESPNow Hub component."""

from homeassistant.core import HomeAssistant, Event
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceEntry

from .const import DOMAIN, EVENT_TYPE, DEFAULT_PLATFORMS


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the ESPNow Hub component (legacy)."""

    # see tasmota component
    # @callback
    # def handle_espnow_messages(event: Event):
    #     # hass.async_create_task(
    #     #     _async_handle_event(hass, event, entry, async_add_entities)
    #     # )

    # hass.bus.async_listen(EVENT_TYPE, handle_espnow_messages)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ESPNow Hub from a config entry."""
    # Load the DEFAULT_PLATFORMS
    await hass.config_entries.async_forward_entry_setups(entry, DEFAULT_PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload the DEFAULT_PLATFORMS
    await hass.config_entries.async_unload_platforms(entry, DEFAULT_PLATFORMS)
    return True

async def async_remove_config_entry_device(
    hass: HomeAssistant, config_entry: ConfigEntry, device_entry: DeviceEntry
) -> bool:
    """Remove a config entry from a device."""

