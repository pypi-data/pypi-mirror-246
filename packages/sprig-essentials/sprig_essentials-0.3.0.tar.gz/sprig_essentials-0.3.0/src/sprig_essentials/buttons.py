import board
import displayio, digitalio
from typing import Any, Union

# To show return tooltips for functions
class pin_number:pass
class digitalio__digital_in_out:pass

class Button:
    def __init__(self,
                 button_pin: pin_number = None,
                 quick_start: bool = False) -> None:
        # Reset all pins to allow new connections
        displayio.release_displays()

        # Store inputs for future use if needed
        self.quick_start = quick_start

        # Intial button states
        self.prev_state = False
        self.cur_state = False

        if quick_start:
            self.w, self.a, self.s, self.d, self.i, self.j, self.k, self.l = self.quickStartButtons()
        elif button_pin != None:
            self.button_pin = button_pin
            self.button = self.createButton(button_pin)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self.quick_start:
            return self.w, self.a, self.s, self.d, self.i, self.j, self.k, self.l
        else:
            return self.button

    # Create a button
    def createButton(self,
                     btn_pin: pin_number) -> digitalio__digital_in_out:
        button = digitalio.DigitalInOut(btn_pin)
        button.direction = digitalio.Direction.INPUT
        button.pull = digitalio.Pull.UP

        return button

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

    # Gets the current state of the button
    # True is pressed, False is released
    def getPressed(self,
                   button: digitalio__digital_in_out = None) -> Union[bool, list[bool]]:
        if button != None:
            return not button.value

        if not self.quick_start:
            return not self.button.value
        else:
            # Return a list of all the buttons that are pressed currently
            return [self.getPressed(self.w), self.getPressed(self.a), self.getPressed(self.s), self.getPressed(self.d),
                    self.getPressed(self.i), self.getPressed(self.j), self.getPressed(self.k), self.getPressed(self.l)]

    # Update the current and previous state of the button
    # TODO
    def updateButton(self) -> None:
        pass
