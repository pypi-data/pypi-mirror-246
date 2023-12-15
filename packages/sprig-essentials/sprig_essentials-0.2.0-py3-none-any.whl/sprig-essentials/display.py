from typing import Union
import board
import displayio, digitalio, busio, terminalio
from adafruit_display_text import label
from adafruit_st7735r import ST7735R

# Reset all pins to allow new connections
displayio.release_displays()

# To show return tooltips for functions
class pin_number:pass
class digitalio__digital_in_out:pass
class busio__spi:pass
class displayio__display_bus:pass
class st7735r:pass
class displayio__group:pass
class displayio__bitmap:pass
class displayio__palette:pass
class displayio__sprite:pass
class terminalio__font:pass
class label__label:pass

# Convert rgb colour values to hex
def convertRGBToHex(rgb: list):
    if len(rgb) > 3:
        raise IndexError(f"The list should have 3 value for the red, green, and blue channels! You have: {len(rgb)} values in your list.")
    elif rgb[0] > 255 or rgb[0] < 0 or rgb[1] > 255 or rgb[1] < 0 or rgb[2] > 255 or rgb[2] < 0:
        raise ValueError(f"The values should be between 0 and 255 inclusive! Your input is: {rgb}.")
    elif (type(rgb[0]) != int and type(rgb[0]) != float) or (type(rgb[1]) != int and type(rgb[1]) != float) or (type(rgb[2]) != int and type(rgb[2]) != float):
        raise TypeError("The values in the list are not of the correct type! It should either be an int or a float.")
    else:
        return int("{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2]), 16)

# Turn on backlight as it doesn't turn on automatically
def startBacklight(backlight_pin: pin_number) -> digitalio__digital_in_out:
    led = digitalio.DigitalInOut(backlight_pin)
    led.direction = digitalio.Direction.OUTPUT
    led.value = True
    return led

def createSPI(clock_pin: pin_number,
              MOSI_pin: pin_number,
              MISO_pin: pin_number) -> busio__spi:
    spi = busio.SPI(clock=clock_pin, MOSI=MOSI_pin, MISO=MISO_pin)
    return spi

def createDisplayBus(spi: busio__spi,
                     cs_pin: pin_number,
                     dc_pin: pin_number,
                     reset_pin: pin_number) -> displayio__display_bus:
    display_bus = displayio.FourWire(spi, command=dc_pin, chip_select=cs_pin, reset=reset_pin)
    return display_bus

def initDisplay(display_bus: displayio__display_bus,
                width: int,
                height: int,
                rotation: int = 0,
                bgr: bool = True,
                auto_refresh: bool = True) -> st7735r:
    display = ST7735R(display_bus, width=width, height=height, rotation=rotation, bgr=bgr)
    display.auto_refresh = auto_refresh
    return display

# Automates display creation, assuming you're using a Sprig
def quickStartDisplay() -> Union[digitalio__digital_in_out, busio__spi, displayio__display_bus, st7735r]:
    backlight = startBacklight(board.GP17)
    spi = createSPI(board.GP18, board.GP19, board.GP16)
    display_bus = createDisplayBus(spi, board.GP20, board.GP22, board.GP26)
    display = initDisplay(display_bus, 160, 128, rotation=270)
    return backlight, spi, display_bus, display

def createDisplayGroup(x: int = 0,
                       y: int = 0,
                       scale: int = 1) -> displayio__group:
    group = displayio.Group(x=x, y=y, scale=scale)
    return group

def showDisplayGroup(display: st7735r,
                     group: displayio__group) -> None:
    display.show(group)

def createBitmap(width: int,
                 height: int,
                 value_count: int = 1) -> displayio__bitmap:
    bitmap = displayio.Bitmap(width, height, value_count)
    return bitmap

def createColourPalette(colours: list) -> displayio__palette:
    color_palette = displayio.Palette(len(colours))
    for i in range(len(colours)):
        color_palette[i] = colours[i]
    return color_palette

def createSprite(bitmap: displayio__bitmap,
                 pixel_shader: displayio__palette,
                 x: int = 0,
                 y: int = 0) -> displayio__sprite:
    sprite = displayio.TileGrid(bitmap, pixel_shader=pixel_shader, x=x, y=y)
    return sprite

def showSprite(group: displayio__group,
               sprite: displayio__sprite) -> None:
    group.append(sprite)

def createTextSprite(text: str,
                     colour: list,
                     x: int = 0,
                     y: int = 0,
                     font: terminalio__font = terminalio.FONT) -> label__label:
    text_area = label.Label(font, text=text, color=colour[-1], x=x, y=y)
    return text_area
