import busio
import board
from digitalio import DigitalInOut, Pull

class Button:
    """
    This class serves to initialize the buttons with the board
    and to detect button presses.
    """

    # Note there is a pull-up resistor, so unpressed = voltage = True
    # And therefore pressed corresponds to FAlse
    # Note the is_pressed method returns True if the button was pressed
    def __init__(self, button: str):
        if button.lower() == 'down':
            print('Button down init')
            self.button = DigitalInOut(board.BUTTON_DOWN)
        else:
            print('Button up init')
            self.button = DigitalInOut(board.BUTTON_UP)
        self.button.switch_to_input(pull=Pull.UP)
        self.last_state = True
        
    def is_pressed(self):

        # Here we look for a state change from high to low
        pressed = (self.button.value is False) and (self.last_state is True)
        self.last_state = self.button.value
        return pressed
    
