# src/input_handler.py
try:
    import RPi.GPIO as GPIO
    print("Running on Raspberry Pi")
except ImportError:
    from unittest.mock import MagicMock
    GPIO = MagicMock()
    print("Running on MacOS or non-RPi environment")

class InputHandler:
    def __init__(self, config):
        """
        Initialize the input handler with GPIO pin configuration.
        :param config: Dictionary containing GPIO pin mappings for joystick and buttons.
        """
        self.config = config
        self.joystick_state = {"up": False, "down": False, "left": False, "right": False, "center": False}
        self.button_state = {"menu": False}

        # GPIO setup (only for Raspberry Pi)
        if not isinstance(GPIO, MagicMock):
            GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
            for pin in config.values():
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read_inputs(self):
        """
        Read the state of all configured GPIO pins.
        """
        if not isinstance(GPIO, MagicMock):
            self.joystick_state["up"] = not GPIO.input(self.config["up"])
            self.joystick_state["down"] = not GPIO.input(self.config["down"])
            self.joystick_state["left"] = not GPIO.input(self.config["left"])
            self.joystick_state["right"] = not GPIO.input(self.config["right"])
            self.joystick_state["center"] = not GPIO.input(self.config["center"])
            self.button_state["menu"] = not GPIO.input(self.config["menu"])
        else:
            # Mock input for development on MacOS
            print("Mock input: Joystick and button states are not updated.")

    def get_joystick_state(self):
        """
        Get the current joystick state.
        :return: Dictionary with joystick directions and their states (True/False).
        """
        return self.joystick_state

    def get_button_state(self):
        """
        Get the current button state.
        :return: Dictionary with button names and their states (True/False).
        """
        return self.button_state

    def cleanup(self):
        """
        Clean up GPIO settings when shutting down the application.
        """
        if not isinstance(GPIO, MagicMock):
            GPIO.cleanup()
