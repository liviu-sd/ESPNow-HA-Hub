# Complete project details at https://RandomNerdTutorials.com

from machine import Pin
from time import sleep
import dht 

# sensor = dht.DHT22(Pin(2))
sensor = dht.DHT22(Pin(4)) # prod
#sensor = dht.DHT11(Pin(14))

def map_range(x, in_min, in_max, out_min, out_max):
# Usage: Map raw ADC (0-65535) to 0-3.3V
# voltage = map_range(adc.read_u16(), 0, 65535, 0, 3.3)
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def get_data(wait=2, d=False):
    while True:
      try:
        if wait > 0:
            sleep(wait)
        sensor.measure()
        temp_raw = sensor.temperature()
        hum_raw = sensor.humidity()
        temp_f = temp_raw * (9/5) + 32.0
        if d:
            print('Temperature: %3.1f C' %temp_raw)
            print('Humidity: %3.1f %%' %hum_raw)
        t_out = map_range(temp_raw, 5.7, 34.1, 4, 33.6)
        h_out = map_range(hum_raw, 0, 80.40, 0, 79.02)
        return t_out, h_out, temp_raw, hum_raw
      except OSError as e:
        print('Failed to read sensor.')
    
    return None, None, None, None