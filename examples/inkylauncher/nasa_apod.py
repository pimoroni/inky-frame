import gc
from urllib import urequest

import jpegdec
import pngdec
from inky_frame import BLACK, RED, WHITE
from ujson import load

"""
NASA Astronomy Picture of the Day

Fetches the latest APOD from NASA's website, https://science.nasa.gov/apod/
NASA's image server can resize the image to fit your Inky Frame, so we can download it directly.
"""

graphics = None
WIDTH = None
HEIGHT = None

# Length of time between updates in minutes.
# Frequent updates will reduce battery life!
UPDATE_INTERVAL = 240

gc.collect()

FILENAME = "nasa-apod-daily"

# The latest APOD post (just its title and image ID)
POST_URL = "https://science.nasa.gov/wp-json/wp/v2/image-article?categories=22766&per_page=1&_fields=title,featured_media"
# The URL of an image, given its ID
MEDIA_URL = "https://science.nasa.gov/wp-json/wp/v2/media/{}?_fields=source_url"

apod_title = "Image Title Unavailable"
error = None


def get_json(url):
    gc.collect()
    socket = urequest.urlopen(url)
    j = load(socket)
    socket.close()
    return j


def update():
    global apod_title, error

    error = None

    try:
        post = get_json(POST_URL)[0]

        # Titles look like "APOD: 2026 November 6 &#8211; A Farewell to Swift"
        title = post["title"]["rendered"]
        title = title.replace("&#8211;", "-").replace("–", "-").replace("&#8217;", "'")
        apod_title = title.split(" - ", 1)[-1]

        image_url = get_json(MEDIA_URL.format(post["featured_media"]))["source_url"]

        # Ask NASA to resize the image to fit our display
        socket = urequest.urlopen(f"{image_url}?w={WIDTH}&h={HEIGHT}")

        # Stream the image data from the socket onto disk in 1024 byte chunks
        data = bytearray(1024)
        with open(FILENAME, "wb") as f:
            while True:
                n = socket.readinto(data)
                if n == 0:
                    break
                f.write(data[:n])
        socket.close()
        gc.collect()

    except (OSError, ValueError, KeyError, IndexError) as e:
        print(e)
        error = "Unable to download today's image"


def draw():
    global error

    gc.collect()  # For good measure...

    # Space is black, so fill any gaps around the image with black
    graphics.set_pen(BLACK)
    graphics.clear()

    try:
        # NASA's images can be either JPEG or PNG
        # PNG files always start with these 4 bytes
        with open(FILENAME, "rb") as f:
            is_png = f.read(4) == b"\x89PNG"
        image = pngdec.PNG(graphics) if is_png else jpegdec.JPEG(graphics)

        # Centre the image on the display
        image.open_file(FILENAME)
        image.decode((WIDTH - image.get_width()) // 2, (HEIGHT - image.get_height()) // 2)
    except OSError:
        error = "Unable to display image"

    if error:
        graphics.set_pen(RED)
        graphics.rectangle(0, 10, WIDTH, 35)
        graphics.set_pen(BLACK)
        graphics.text(error, 5, 16, WIDTH, 2)

    graphics.set_pen(WHITE)
    graphics.rectangle(0, HEIGHT - 25, WIDTH, 25)
    graphics.set_pen(BLACK)
    graphics.text(apod_title, 5, HEIGHT - 20, WIDTH, 2)

    graphics.update()
