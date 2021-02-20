#!/usr/bin/env python3

""" Listens for CEC keypresses and prints the keycode
"""

from time import sleep
import cec
from cecdaemon.const import USER_CONTROL_CODES, COMMANDS
import json

def print_keycode(event, *data):
    """ Takes a python-cec cec.EVENT_COMMAND callback and prints the user control code

    :param event: cec event type (is passed from callback even if unneeded
    :type event: int
    :param data: (code, milsec)
    :type data: tuple
    :param code: cec user command code
    :type code: int
    :param milsec: time pressed in miliseconds
    :type milsec: int
    """
    assert event == 2
    code, milsec = data
    if milsec > 0:
        print(f'{USER_CONTROL_CODES[code]} pressed (hex: {hex(code)}, dec: {code})')

def print_event(event, data):
    assert event == 4
    opcode = data['opcode']
    try:
        event_name = COMMANDS[opcode]
    except KeyError:
        event_name = "<unknown>"
    print("%s command (code: %x, data: %s)" % (event_name, opcode, json.dumps(data)))

def main():
    """ Inits cec and listens for remote keystrokes
    """
    print('Initializing CEC, please wait...')
    print('If this takes too long ensure the device is not already in use')
    cec.init()
    cec.add_callback(print_keycode, 2)
    cec.add_callback(print_event, 4)
    print('CEC device initialized, press remote keys or hit ^C to quit')

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':
    main()
