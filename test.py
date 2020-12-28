import socket

from pynput import keyboard

PORT = 2342


BUTTONS = {
    0: keyboard.Key.up,
    1: keyboard.Key.right,
    2: keyboard.Key.down,
    3: keyboard.Key.left,
    # TODO: following codes
    #buttons.BTN_A: 4,
    #buttons.BTN_B: 5,
    #buttons.BTN_SELECT: 6,
    #buttons.BTN_START: 7,
}



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    kbd = keyboard.Controller()

    sock.connect(("10.128.20.186", PORT))
    while True:
        cmd = int(sock.recv(1)[0])
        push = bool(cmd >> 4)
        code = cmd & 0x0F

        if code in BUTTONS:
            if push:
                kbd.press(BUTTONS[code])
            else:
                kbd.release(BUTTONS[code])
