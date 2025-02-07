# https://github.com/micropython/micropython-lib/blob/master/micropython/bundles/bundle-networking/manifest.py
require("bundle-networking")
require("urllib.urequest")
require("umqtt.simple")

# SD Card
require("sdcard")

# Bluetooth
require("aioble")

freeze("$(MPY_DIR)/../pimoroni-pico/micropython/modules_py", "pimoroni.py")
freeze("$(MPY_DIR)/../pimoroni-pico/micropython/modules_py", "boot.py")
freeze("$(MPY_DIR)/../pimoroni-pico/micropython/modules_py", "lte.py")
freeze("../modules", "inky_frame.py")