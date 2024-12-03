# https://github.com/micropython/micropython-lib/blob/master/micropython/bundles/bundle-networking/manifest.py
require("bundle-networking")
require("urllib.urequest")
require("umqtt.simple")

# SD Card
require("sdcard")

# Bluetooth
require("aioble")

freeze("../../pimoroni-pico/micropython/modules_py", "pimoroni.py")
freeze("../../pimoroni-pico/micropython/modules_py", "boot.py")
freeze("../modules", "inky_frame.py")