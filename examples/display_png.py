# from picographics import PicoGraphics, DISPLAY_INKY_FRAME as DISPLAY      # 5.7"
# from picographics import PicoGraphics, DISPLAY_INKY_FRAME_4 as DISPLAY  # 4.0"
# from picographics import PicoGraphics, DISPLAY_INKY_FRAME_7 as DISPLAY  # 7.3"
from picographics import PicoGraphics, DISPLAY_INKY_FRAME_SPECTRA_7 as DISPLAY  # 7.3" Spectra
from inky_frame import BLACK, WHITE
import pngdec

# Create a PicoGraphics instance
graphics = PicoGraphics(DISPLAY)
WIDTH, HEIGHT = graphics.get_bounds()

# Set the font
graphics.set_font("bitmap8")

# Create an instance of the PNG Decoder
png = pngdec.PNG(graphics)

# Clear the screen
graphics.set_pen(WHITE)
graphics.clear()
graphics.set_pen(BLACK)

# Few lines of text.
graphics.text("PNG Pencil", 70, 100, WIDTH, 3)

# Open our PNG File from flash. In this example we're using a cartoon pencil.
# You can use Thonny to transfer PNG Images to your Inky Frame.
try:
    png.open_file("pencil_256x256.png")

    # Decode our PNG file and set the X and Y
    png.decode(200, 100)

except OSError:
    graphics.text("Unable to find PNG file! Copy 'pencil_256x256.png' to your Inky Frame using Thonny :)", 10, 70, WIDTH, 3)

# Start the screen update
graphics.update()
