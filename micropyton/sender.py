import network
import espnow
from time import sleep

from cayennelpp.lpp_frame import LppFrame
import dht22

from const import ESPNOW_DIAGNOSTIC_CHANNELS
import const

def wifi_reset(channel):   # Reset wifi to AP_IF off, STA_IF on and disconnected
  sta = network.WLAN(network.WLAN.IF_STA); sta.active(False)
  ap = network.WLAN(network.WLAN.IF_AP); ap.active(False)
  sta.active(True)
  sta.config(channel=10)
  while not sta.active():
      time.sleep(0.1)
  sta.disconnect()   # For ESP8266
  while sta.isconnected():
      time.sleep(0.1)
  return sta, ap

e = espnow.ESPNow()
e.active(True)
# 24:4C:AB:29:52:80 => b'\x24\x4c\xab\x29\x52\x80'
peer = b'\x24\x4c\xab\x29\x52\x80'   # MAC address of peer's wifi interface ie 
bcast = b'\xff\xff\xff\xff\xff\xff' # * 6

e.add_peer(peer)      # Must add_peer() before send()
# e.add_peer(bcast) on esp8266 seem broked

sta, ap = wifi_reset(10)

f = LppFrame()

def send(r=10, s=0.1):
    for i in range(r):
        t, h, t_raw, h_raw = dht22.get_data(0, False)
        if t:
            f.reset()
            f.add_temperature(0, t)
            f.add_humidity(0, h)
            f.add_temperature(const.ESPNOW_DIAGNOSTIC_CHANNELS[0], t_raw)
            f.add_humidity(const.ESPNOW_DIAGNOSTIC_CHANNELS[0], h_raw)
            
            bytes2send = f.to_bytes()
            
            e.send(bcast, bytes2send)
#             e.send(peer, bytes2send, True)        
        print(t, h, t_raw, h_raw)
        sleep(s)

