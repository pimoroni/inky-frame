"""
This example connects to the Carbon Intensity API to give you a regional
forecast of how your (UK) electricity is being generated and its carbon impact.

Carbon Intensity API only reports data from the UK National Grid.

Find out more about what the numbers mean at:
https://carbonintensity.org.uk/

Make sure to uncomment the correct size for your display!

"""

import urequests
from inky_frame import BLACK, BLUE, GREEN, ORANGE, RED, WHITE

graphics = None
WIDTH = None
HEIGHT = None

# Length of time between updates in minutes.
# Frequent updates will reduce battery life!
UPDATE_INTERVAL = 240

# Set (the first half) of your UK postcode as CARBON_POSTCODE in secrets.py,
# e.g. CARBON_POSTCODE = "S9", or change the default here.
try:
    from secrets import CARBON_POSTCODE as POSTCODE
except ImportError:
    POSTCODE = "S9"

URL = "https://api.carbonintensity.org.uk/regional/postcode/" + str(POSTCODE)

# Top of the chart's 100%-of-scale line, below the header text (and room for a % label above a full bar)
CHART_TOP = 88


def update():
    global region, forecast, index, power_list, datetime_to, datetime_from
    print(f"Requesting URL: {URL}")
    r = urequests.get(URL)
    # open the json data
    j = r.json()
    print("Data obtained!")
    print(j)

    # parse the json data
    region = j["data"][0]["shortname"]

    forecast = j["data"][0]["data"][0]["intensity"]["forecast"]
    index = j["data"][0]["data"][0]["intensity"]["index"]

    power_list = []
    for power in j["data"][0]["data"][0]["generationmix"]:
        power_list.append(power["perc"])

    datetime_to = j["data"][0]["data"][0]["to"].split("T")
    datetime_from = j["data"][0]["data"][0]["from"].split("T")

    # close the socket
    r.close()


def draw():
    # we're setting up our PicoGraphics buffer after we've made our RAM intensive https request
    w, h = WIDTH, HEIGHT
    graphics.set_pen(WHITE)
    graphics.clear()

    # draw lines
    labels = ["biomass", "coal", "imports", "gas", "nuclear", "other", "hydro", "solar", "wind"]
    bar_colours = [ORANGE, RED, ORANGE, RED, BLUE, ORANGE, GREEN, GREEN, GREEN]
    bar_w = w / 9

    # Scale the chart to the biggest bar, rounded up to a "nice" maximum,
    # so small shares are still visible when nothing dominates.
    biggest = max(power_list) if power_list else 0
    scale_max = 100
    for nice in (20, 40, 60, 80, 100):  # quarters of these are all whole numbers
        if biggest <= nice:
            scale_max = nice
            break

    # The chart sits below the header text and above the footer
    plot_top = CHART_TOP
    plot_h = h - plot_top

    def y_for(percent):
        return int(h - percent * plot_h / scale_max)

    # Gridlines at each quarter of the scale (drawn first so bars sit on top)
    graphics.set_pen(BLACK)
    for q in range(5):
        y = y_for(scale_max * q / 4)
        graphics.line(0, y, w, y)

    # Bars
    for i, p in enumerate(power_list):
        graphics.set_pen(bar_colours[i])
        top = y_for(p)
        graphics.rectangle(int(i * bar_w), top, int(bar_w), h - top)

    # Rotated fuel names, once thick in white as a halo, then in black
    graphics.set_font("sans")
    for pen, thickness in ((WHITE, 4), (BLACK, 2)):
        graphics.set_pen(pen)
        graphics.set_thickness(thickness)
        for i, label in enumerate(labels):
            graphics.text(label, int(i * bar_w + bar_w / 2), h - 10, angle=270, scale=1)

    # Work out where each bar's percentage label goes: above the bar, or above
    # the rotated fuel name if the bar is shorter than the name.
    graphics.set_font("sans")
    name_tops = [h - 10 - graphics.measure_text(label, 1) for label in labels]
    graphics.set_font("bitmap8")
    pct_labels = []
    for i, p in enumerate(power_list):
        text = ("%d%%" if p == int(p) else "%.1f%%") % p
        text_w = graphics.measure_text(text, 2)
        y = min(y_for(p), name_tops[i]) - 20
        x = int(i * bar_w + (bar_w - text_w) / 2)
        pct_labels.append((text, x, y, text_w))

    # Gridline labels on the right, on a white background so they're readable over the bars.
    # Skip any that would collide with the rightmost bar's percentage label.
    last_y = pct_labels[-1][2] if pct_labels else -100
    for q in range(1, 5):
        text = "%d%%" % (scale_max * q // 4)
        text_w = graphics.measure_text(text, 2)
        y = y_for(scale_max * q / 4) + 3
        if abs(y - last_y) < 20:
            continue
        graphics.set_pen(WHITE)
        graphics.rectangle(w - text_w - 6, y - 1, text_w + 6, 18)
        graphics.set_pen(BLACK)
        graphics.text(text, w - text_w - 3, y, scale=2)

    # Percentage labels
    for text, x, y, text_w in pct_labels:
        graphics.set_pen(WHITE)
        graphics.rectangle(x - 2, y - 1, text_w + 4, 18)
        graphics.set_pen(BLACK)
        graphics.text(text, x, y, scale=2)

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
