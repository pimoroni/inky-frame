import gc
import time
from urllib import urequest

import inky_helper as ih
import ujson
# from picographics import DISPLAY_INKY_FRAME_4 as DISPLAY  # 4.0"
# from picographics import DISPLAY_INKY_FRAME as DISPLAY    # 5.7"
# from picographics import DISPLAY_INKY_FRAME_7 as DISPLAY  # 7.3"
from picographics import \
    DISPLAY_INKY_FRAME_SPECTRA_7 as DISPLAY  # 7.3" Spectra
from picographics import PicoGraphics

ENDPOINT = "https://en.wikiquote.org/w/api.php?format=json&action=expandtemplates&prop=wikitext&text={{{{Wikiquote:Quote%20of%20the%20day/{3}%20{2},%20{0}}}}}"
MONTHNAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


last_date = ""


def parse_qotd(text):
    print(text)
    text = text.split("\n")
    author = text[8].split("|")[2][5:-4]
    text = text[6][2:]
    gc.collect()
    return text, author


gc.collect()
graphics = PicoGraphics(DISPLAY)
WIDTH, HEIGHT = graphics.get_bounds()
graphics.set_font("bitmap8")
gc.collect()


BADCHARS = {
    "’": "'",
    "—": "",
    "…": "..."
}


def display_quote(text, ox, oy, scale, wordwrap):
    # Processing text is memory intensive
    # so we'll do it one char at a time as we draw to the screen
    line_height = 9 * scale
    html_tag = ""
    word = ""
    extra_text = ""
    space_width = graphics.measure_text(" ", scale=scale)
    x = ox
    y = oy
    i = -1
    while True:
        if len(extra_text) == 0:
            i += 1
        if i >= len(text):
            break

        if len(extra_text) > 0:
            char = extra_text[0]
            extra_text = extra_text[1:]
        else:
            char = text[i]

        if char in BADCHARS:
            word += BADCHARS[char]
            continue

        # Unpick stuff like [[word]] and [[disambiguation|word]]
        # and  [[w:wikipedia_page|word]]
        # test cases: July 8th 2022, July 12th 2022
        if char == "[":
            if text[i:i + 2] == "[[":
                link = False
                if text[i + 2:i + 4] == "w:":
                    link = True
                    i += 2
                end = text[i:].index("]]")
                if "|" in text[i + 2:i + end]:
                    parts = text[i + 2:i + end].split("|")
                    word = parts[1]
                    if not link:
                        extra_text = " (" + parts[0] + ")"
                else:
                    word = text[i + 2:i + end]
                i += end + 1
                continue

        if char == "&":
            if text[i:i + 5] == "&amp;":
                word += "&"
                i += 4
                continue

        if char == "<":
            j = i + text[i:].index(">")
            html_tag = text[i + 1:j].replace("/", "").strip()
            i = j
            continue

        if char in (" ", "\n") or html_tag == "br":
            w = graphics.measure_text(word, scale=scale)
            if x + w > wordwrap or char == "\n" or html_tag == "br":
                x = ox
                y += line_height

            graphics.text(word, x, y, scale=scale)
            word = ""
            html_tag = ""
            x += w + space_width
            continue

        word += char

    # Last word
    w = graphics.measure_text(word, scale=scale)
    if x + w > wordwrap:
        x = ox
        y += line_height

    graphics.text(word, x, y, scale=scale)


while True:
    gc.collect()

    # Connect to WiFi
    try:
        from secrets import WIFI_PASSWORD, WIFI_SSID
        ih.network_connect(WIFI_SSID, WIFI_PASSWORD)
    except ImportError:
        print("Add your WiFi credentials to secrets.py")

    date = list(time.localtime())[:3]
    date.append(MONTHNAMES[date[1] - 1])

    if "{3} {2}, {0}".format(*date) == last_date:
        time.sleep(60)
        continue

    url = ENDPOINT.format(*date)
    print("Requesting URL: {}".format(url))
    # Wikipedia asks that you set a user-agent and respect their robot policy https://w.wiki/4wJS.
    headers = {"User-Agent": "Inky Frame Quote of the Day Example (https://github.com/pimoroni/inky-frame)"}
    socket = urequest.urlopen(url, headers=headers)
    j = ujson.load(socket)
    socket.close()

    text = j["expandtemplates"]["wikitext"]
    del j
    gc.collect()

    text, author = parse_qotd(text)

    print(text)

    graphics.set_pen(1)
    graphics.clear()
    graphics.set_pen(0)
    graphics.text("QoTD - {2} {3} {0:04d}".format(*date), 10, 10, scale=3)

    display_quote(text, 10, 40, 2, wordwrap=WIDTH - 20)

    graphics.text(author, 10, HEIGHT - 20, scale=2)

    graphics.update()
    gc.collect()

    last_date = "{3} {2}, {0}".format(*date)

    time.sleep(60)
