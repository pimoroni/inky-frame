import time
import inky_frame
# from picographics import DISPLAY_INKY_FRAME_4 as DISPLAY  # 4.0"
# from picographics import DISPLAY_INKY_FRAME as DISPLAY    # 5.7"
# from picographics import DISPLAY_INKY_FRAME_7 as DISPLAY  # 7.3"
from picographics import DISPLAY_INKY_FRAME_SPECTRA_7 as DISPLAY  # 7.3" Spectra
from picographics import PicoGraphics
import inky_helper as ih

# Set tz_offset to be the number of hours off of UTC for your local zone.
# Examples:  tz_offset = -7 # Pacific time (PST)
#            tz_offset =  1 # CEST (Paris)
tz_offset = 0
tz_seconds = tz_offset * 3600

# Sync the Inky (always on) RTC to the Pico W so that "time.localtime()" works.
inky_frame.pcf_to_pico_rtc()

# Avoid running code unless we've been triggered by an event
# Keeps this example from locking up Thonny when we want to tweak the code
if inky_frame.woken_by_rtc() or inky_frame.woken_by_button():
    graphics = PicoGraphics(DISPLAY)
    WIDTH, HEIGHT = graphics.get_bounds()

    graphics.set_pen(1)
    graphics.clear()

    # Look, just because this is an RTC demo,
    # doesn't mean we can't make it rainbow.
    for x in range(WIDTH):
        h = x / WIDTH
        p = graphics.create_pen_hsv(h, 1.0, 1.0)
        graphics.set_pen(p)
        graphics.line(x, 0, x, HEIGHT)

    graphics.set_pen(0)
    graphics.rectangle(0, 0, WIDTH, 14)
    graphics.set_pen(1)
    graphics.text("Inky Frame", 1, 0)
    graphics.set_pen(0)

    year, month, day, hour, minute, second, dow, _ = time.localtime(time.time() + tz_seconds)

    # Connect to the network and get the time if it's not set
    if year < 2023:
        # Connect to WiFi and set the time
        try:
            from secrets import WIFI_PASSWORD, WIFI_SSID
            ih.network_connect(WIFI_SSID, WIFI_PASSWORD)
            inky_frame.set_time()
        except ImportError:
            print("Add your WiFi credentials to secrets.py")

    # Display the date and time
    year, month, day, hour, minute, second, dow, _ = time.localtime(time.time() + tz_seconds)

    date_time = f"{year:04}/{month:02}/{day:02} {hour:02}:{minute:02}:{second:02}"

    graphics.set_font("bitmap8")

    text_scale = 8 if WIDTH == 800 else 6
    text_height = 8 * text_scale

    offset_left = (WIDTH - graphics.measure_text(date_time, scale=text_scale)) // 2
    offset_top = (HEIGHT - text_height) // 2

    graphics.set_pen(graphics.create_pen(50, 50, 50))
    graphics.text(date_time, offset_left + 2, offset_top + 2, scale=text_scale)
    graphics.set_pen(1)
    graphics.text(date_time, offset_left, offset_top, scale=text_scale)

    graphics.update()

    inky_frame.sleep_for(2)
