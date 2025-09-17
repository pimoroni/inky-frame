import gc
from urllib import urequest

import inky_helper as ih
import jpegdec
import machine
import sdcard
import uos
# from picographics import DISPLAY_INKY_FRAME_4 as DISPLAY  # 4.0"
# from picographics import DISPLAY_INKY_FRAME as DISPLAY    # 5.7"
# from picographics import DISPLAY_INKY_FRAME_7 as DISPLAY  # 7.3"
from picographics import \
    DISPLAY_INKY_FRAME_SPECTRA_7 as DISPLAY  # 7.3" Spectra
from picographics import PicoGraphics

"""
xkcd daily

You *must* insert an SD card into Inky Frame!
We need somewhere to save the jpg for display.

Fetches a pre-processed XKCD daily image from:
https://pimoroni.github.io/feed2image/xkcd-daily.jpg

See https://xkcd.com/ for more webcomics!
"""

gc.collect()  # We're really gonna need that RAM!

# Connect to WiFi
try:
    from secrets import WIFI_PASSWORD, WIFI_SSID
    ih.network_connect(WIFI_SSID, WIFI_PASSWORD)
except ImportError:
    print("Add your WiFi credentials to secrets.py")

graphics = PicoGraphics(DISPLAY)

WIDTH, HEIGHT = graphics.get_bounds()
FILENAME = "/sd/xkcd-daily.jpg"
ENDPOINT = "https://pimoroni.github.io/feed2image/xkcd-daily.jpg"


sd_spi = machine.SPI(0, sck=machine.Pin(18, machine.Pin.OUT), mosi=machine.Pin(19, machine.Pin.OUT), miso=machine.Pin(16, machine.Pin.OUT))
sd = sdcard.SDCard(sd_spi, machine.Pin(22))
uos.mount(sd, "/sd")
gc.collect()  # Claw back some RAM!


url = ENDPOINT

if (WIDTH, HEIGHT) != (600, 448):
    url = url.replace("xkcd-", f"xkcd-{WIDTH}x{HEIGHT}-")

socket = urequest.urlopen(url)

# Stream the image data from the socket onto disk in 1024 byte chunks
# the 600x448-ish jpeg will be roughly ~24k, we really don't have the RAM!
data = bytearray(1024)
with open(FILENAME, "wb") as f:
    while True:
        if socket.readinto(data) == 0:
            break
        f.write(data)
socket.close()
gc.collect()  # We really are tight on RAM!


jpeg = jpegdec.JPEG(graphics)
gc.collect()  # For good measure...

graphics.set_pen(1)
graphics.clear()

jpeg.open_file(FILENAME)
jpeg.decode()

graphics.update()
