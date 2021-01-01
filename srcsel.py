#!/usr/bin/python3

import subprocess
import time

import RPi.GPIO as GPIO


# The file path for `ddcutil`
DDCUTIL = "/usr/local/bin/ddcutil"

# The I2C bus number for `ddcutil`
I2C_BUS = 1

# The MCCS version for `ddcutil`
MCCS_VER = "2.2"

# The GPIO pin identifiers assigned to each switch.
# The index of this list corresponds to the identifier of each switch.
PINS = [33, 31, 37, 35]

# The input source identifiers
# used in VCP code 0x60 (Input Select)
# as defined in the VESA Monitor Control Command Set Standard.
# The index of this list corresponds to the identifier of each switch.
SOURCES = [0x11, 0x12, 0x0f, 0x13]


def _pin_to_switch(pin):
    """
    Convert from pin identifier to switch identifier.

    Parameters
    ----------
    pin : int
        The GPIO pin identifier.

    Returns
    -------
    switch : int
        The switch identifier specified as a zero-based integer.
    """
    for i in range(len(PINS)):
        if PINS[i] == pin:
            return i


def on_pressed(channel):
    """
    Callback function called when the switch is pressed.

    Parameters
    ----------
    channel : int
        In this program, ``channel`` is a pin identifier
        corresponding to the pressed switch.
    """
    change_source(_pin_to_switch(channel))


def change_source(switch):
    """
    Change the input source of the monitor.

    This function depends on ddcutil.
    https://github.com/rockowitz/ddcutil

    Parameters
    ----------
    switch : int
        The identifier of the switch
        corresponding to the input source of the monitor.
        The identifier is specified as a zero-based integer.
    """
    subprocess.run(
        [
            DDCUTIL,
            "--bus",
            str(I2C_BUS),
            "--mccs",
            MCCS_VER,
            "setvcp",
            "0x60",  # VCP Code for "Input Select"
            str(SOURCES[switch]),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def setup():
    GPIO.setmode(GPIO.BOARD)

    for i in range(len(PINS)):
        GPIO.setup(PINS[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(
            PINS[i],
            GPIO.FALLING,
            callback=on_pressed,
            bouncetime=200
        )


def run():
    try:
        while True:
            time.sleep(0.01)

    except KeyboardInterrupt:
        pass

    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    setup()
    run()
