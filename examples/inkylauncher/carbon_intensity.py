"""
This example connects to the Carbon Intensity API to give you a regional
forecast of how your (UK) electricity is being generated and its carbon impact.

Carbon Intensity API only reports data from the UK National Grid.

Find out more about what the numbers mean at:
https://carbonintensity.org.uk/

Make sure to uncomment the correct size for your display!

"""

import inky_helper as ih
import urequests
from inky_frame import BLACK, BLUE, GREEN, ORANGE, RED, WHITE

graphics = None
WIDTH = None
HEIGHT = None

# Length of time between updates in minutes.
# Frequent updates will reduce battery life!
UPDATE_INTERVAL = 240

# Set (the first half) of your UK postcode here
POSTCODE = "S9"

URL = "https://api.carbonintensity.org.uk/regional/postcode/" + str(POSTCODE)


region = None  # stays None until we've had a successful update


def update():
    global region, forecast, index, power_list, datetime_to, datetime_from

    # Without a connection the request can block forever; keep any previous data instead.
    if not ih.is_connected():
        print("No network connection, skipping update")
        return

    try:
        print(f"Requesting URL: {URL}")
        r = urequests.get(URL)
        # open the json data
        j = r.json()
        # close the socket
        r.close()
        print("Data obtained!")
        print(j)

        # parse the json data
        data = j["data"][0]["data"][0]
        power_list = [power["perc"] for power in data["generationmix"]]
        forecast = data["intensity"]["forecast"]
        index = data["intensity"]["index"]
        datetime_to = data["to"].split("T")
        datetime_from = data["from"].split("T")
        region = j["data"][0]["shortname"]  # set last, so a partial parse doesn't count as success
    except (OSError, ValueError, KeyError, IndexError, TypeError) as e:  # network errors, bad JSON, unexpected response
        print("Carbon Intensity update failed:", e)


def draw():
    # we're setting up our PicoGraphics buffer after we've made our RAM intensive https request
    w, h = WIDTH, HEIGHT
    graphics.set_pen(WHITE)
    graphics.clear()

    if region is None:
        graphics.set_font("bitmap8")
        graphics.set_pen(RED)
        graphics.rectangle(0, (HEIGHT // 2) - 20, WIDTH, 40)
        graphics.set_pen(WHITE)
        graphics.text("Unable to get Carbon Intensity data!", 5, (HEIGHT // 2) - 15, WIDTH, 2)
        graphics.text("Check your network settings in secrets.py", 5, (HEIGHT // 2) + 2, WIDTH, 2)
        graphics.update()
        return

    # draw lines
    graphics.set_pen(BLACK)
    graphics.line(0, int((h / 100) * 0), w, int((h / 100) * 0))
    graphics.line(0, int((h / 100) * 50), w, int((h / 100) * 50))
    graphics.set_font("bitmap8")
    graphics.text("100%", w - 40, 10, scale=2)
    graphics.text("50%", w - 40, int((h / 100) * 50 + 10), scale=2)

    # draw bars
    bar_colours = [
        ORANGE,
        RED,
        ORANGE,
        RED,
        BLUE,
        ORANGE,
        GREEN,
        GREEN,
        GREEN
    ]
    for p in power_list:
        graphics.set_pen(bar_colours[power_list.index(p)])
        graphics.rectangle(int(power_list.index(p) * w / 9), int(h - p * (h / 100)),
                           int(w / 9), int(h / 100 * p))

    # draw labels
    graphics.set_font("sans")
    # once in white for a background
    graphics.set_pen(WHITE)
    labels = ["biomass", "coal", "imports", "gas", "nuclear", "other", "hydro", "solar", "wind"]
    graphics.set_thickness(4)
    for label in labels:
        graphics.text(f"{label}", int((labels.index(label) * w / 9) + (w / 9) / 2), h - 10, angle=270, scale=1)
    # again in black
    graphics.set_pen(BLACK)
    labels = ["biomass", "coal", "imports", "gas", "nuclear", "other", "hydro", "solar", "wind"]
    graphics.set_thickness(2)
    for label in labels:
        graphics.text(f"{label}", int((labels.index(label) * w / 9) + (w / 9) / 2), h - 10, angle=270, scale=1)

    # draw header
    graphics.set_thickness(3)
    graphics.set_pen(GREEN)
    if index in ["high", "very high"]:
        graphics.set_pen(RED)
    if index in ["moderate"]:
        graphics.set_pen(ORANGE)
    graphics.set_font("sans")
    graphics.text("Carbon Intensity", 10, 35, scale=1.2, angle=0)

    # draw small text
    graphics.set_pen(BLACK)
    graphics.set_font("bitmap8")
    graphics.text(f"Region: {region}", int((w / 2) + 30), 10, scale=2)
    graphics.text(f"{forecast} gCO2/kWh ({index})", int((w / 2) + 30), 30, scale=2)
    graphics.text(f"{datetime_from[0]} {datetime_from[1]} to {datetime_to[1]}", int((w / 2) + 30), 50, scale=2)

    graphics.update()
