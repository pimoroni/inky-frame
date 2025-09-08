import gc
from urllib import urequest

import qrcode
from inky_frame import BLACK, BLUE, RED, WHITE

# Uncomment one URL to use (Top Stories, World News and technology)
# URL = "https://feeds.bbci.co.uk/news/rss.xml"
# URL = "https://feeds.bbci.co.uk/news/world/rss.xml"
URL = "https://feeds.bbci.co.uk/news/technology/rss.xml"

# Length of time between updates in minutes.
# Frequent updates will reduce battery life!
UPDATE_INTERVAL = 90

graphics = None
WIDTH = None
HEIGHT = None
code = qrcode.QRCode()


def read_until(stream, find):
    result = b""
    while len(c := stream.read(1)) > 0:
        if c == find:
            return result
        result += c

    return None


def discard_until(stream, find):
    _ = read_until(stream, find)


def parse_xml_stream(s, accept_tags, group_by, max_items=3):
    tag = []
    text = b""
    count = 0
    current = {}

    while True:
        char = s.read(1)
        if len(char) == 0:
            break

        if char == b"<":
            next_char = s.read(1)

            # Discard stuff like <?xml vers...
            if next_char == b"?":
                discard_until(s, b">")
                continue

            # Detect <![CDATA
            elif next_char == b"!":
                s.read(1)  # Discard [
                discard_until(s, b"[")  # Discard CDATA[
                text = read_until(s, b"]")
                discard_until(s, b">")  # Discard ]>
                gc.collect()

            elif next_char == b"/":
                current_tag = read_until(s, b">")
                top_tag = tag[-1]

                # Populate our result dict
                if top_tag in accept_tags:
                    current[top_tag.decode("utf-8")] = text.decode("utf-8")

                # If we've found a group of items, yield the dict
                elif top_tag == group_by:
                    yield current
                    current = {}
                    count += 1
                    if count == max_items:
                        return
                tag.pop()
                text = b""
                gc.collect()
                continue

            else:
                current_tag = read_until(s, b">")
                if not current_tag.endswith(b"/"):
                    tag += [next_char + current_tag.split(b" ")[0]]
                    text = b""

        else:
            text += char


def measure_qr_code(size, code):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size


def draw_qr_code(ox, oy, size, code):
    size, module_size = measure_qr_code(size, code)
    graphics.set_pen(1)
    graphics.rectangle(ox, oy, size, size)
    graphics.set_pen(0)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                graphics.rectangle(ox + x * module_size, oy + y * module_size, module_size, module_size)


# A function to get the data from an RSS Feed, this in case BBC News.
def get_rss():
    try:
        stream = urequest.urlopen(URL)
        return list(parse_xml_stream(stream, [b"title", b"description", b"guid", b"pubDate"], b"item"))

    except OSError as e:
        print(e)
        return []


feed = None


def update():
    global feed
    # Gets Feed Data
    feed = get_rss()


def draw():
    global feed
    graphics.set_font("bitmap8")

    # Clear the screen
    graphics.set_pen(WHITE)
    graphics.clear()
    graphics.set_pen(BLACK)

    # Draws 2 articles from the feed if they're available.
    if len(feed) > 0:

        # Title
        graphics.set_pen(graphics.create_pen(200, 0, 0))
        graphics.rectangle(0, 0, WIDTH, 40)
        graphics.set_pen(BLACK)
        graphics.text("Headlines from BBC News:", 10, 10, WIDTH, 3)

        graphics.set_pen(RED)
        graphics.text(feed[0]["title"], 10, 70, WIDTH - 150, 3 if graphics.measure_text(feed[0]["title"]) < WIDTH else 2)
        graphics.text(feed[1]["title"], 130, 260, WIDTH - 140, 3 if graphics.measure_text(feed[1]["title"]) < WIDTH else 2)

        graphics.set_pen(BLUE)
        graphics.text(feed[0]["description"], 10, 155 if graphics.measure_text(feed[0]["title"]) < 650 else 130, WIDTH - 150, 2)
        graphics.text(feed[1]["description"], 130, 320 if graphics.measure_text(feed[1]["title"]) < 650 else 340, WIDTH - 145, 2)

        graphics.line(10, 215, WIDTH - 10, 215)

        code.set_text(feed[0]["guid"])
        draw_qr_code(WIDTH - 110, 65, 100, code)
        code.set_text(feed[1]["guid"])
        draw_qr_code(10, 265, 100, code)

        graphics.set_pen(graphics.create_pen(200, 0, 0))
        graphics.rectangle(0, HEIGHT - 20, WIDTH, 20)

    else:
        graphics.set_pen(RED)
        graphics.rectangle(0, (HEIGHT // 2) - 20, WIDTH, 40)
        graphics.set_pen(BLACK)
        graphics.text("Unable to display news feed!", 5, (HEIGHT // 2) - 15, WIDTH, 2)
        graphics.text("Check your network settings in secrets.py", 5, (HEIGHT // 2) + 2, WIDTH, 2)

    graphics.update()
