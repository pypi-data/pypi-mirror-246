from typing import Union
import board
import displayio, digitalio

# Reset all pins to allow new connections
displayio.release_displays()

# To show return tooltips for functions
class pin_number:pass
class digitalio__digital_in_out:pass

# Create a button
def createButton(btn_pin: pin_number) -> digitalio__digital_in_out:
    button = digitalio.DigitalInOut(btn_pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP

    return button

# Gets the current state of the button
# True is pressed, False is open
def getPressed(button: digitalio__digital_in_out) -> bool:
    return not button.value

# Automates buttons creation, assuming you're using a Sprig
def quickStartButtons() -> digitalio__digital_in_out:
    w = digitalio.DigitalInOut(board.GP07)
    w.direction = digitalio.Direction.INPUT
    w.pull = digitalio.Pull.UP

    a = digitalio.DigitalInOut(board.GP09)
    a.direction = digitalio.Direction.INPUT
    a.pull = digitalio.Pull.UP

    s = digitalio.DigitalInOut(board.GP10)
    s.direction = digitalio.Direction.INPUT
    s.pull = digitalio.Pull.UP

    d = digitalio.DigitalInOut(board.GP11)
    d.direction = digitalio.Direction.INPUT
    d.pull = digitalio.Pull.UP

    i = digitalio.DigitalInOut(board.GP16)
    i.direction = digitalio.Direction.INPUT
    i.pull = digitalio.Pull.UP

    j = digitalio.DigitalInOut(board.GP17)
    j.direction = digitalio.Direction.INPUT
    j.pull = digitalio.Pull.UP

    k = digitalio.DigitalInOut(board.GP19)
    k.direction = digitalio.Direction.INPUT
    k.pull = digitalio.Pull.UP

    l = digitalio.DigitalInOut(board.GP20)
    l.direction = digitalio.Direction.INPUT
    l.pull = digitalio.Pull.UP

    return w, a, s, d, i, j, k, l
