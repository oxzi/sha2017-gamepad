import argparse
import socket

from pynput.keyboard import Key as kbd_key

from client.handler import *
from client.proto import Keys, unpack_event


def main():
    parser = argparse.ArgumentParser(
        prog="sha2017-gamepad", description="SHA2017 badge gamepad"
    )

    parser.add_argument("host", type=str, help="Badge's host resp. IP")
    parser.add_argument(
        "port",
        nargs="?",
        type=int,
        default=2342,
        help="Badge's port, defaults to %(default)s",
    )

    args = parser.parse_args()

    arrow_handler = ArrowShiftHandler(Keys.BTN_A)
    enter_handler = KeystrokeHandler(kbd_key.enter)
    mic_toggle_handler = CmdHandler("amixer -c 0 set Capture toggle")

    proxy = ProxyHandler()
    for k in (Keys.BTN_UP, Keys.BTN_RIGHT, Keys.BTN_DOWN, Keys.BTN_LEFT, Keys.BTN_A):
        proxy.register(k, arrow_handler)
    proxy.register(Keys.BTN_START, enter_handler)
    proxy.register(Keys.BTN_SELECT, mic_toggle_handler)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((args.host, args.port))
        while True:
            try:
                event = unpack_event(sock.recv(1))
                proxy.handle(event)
            except KeyError as e:
                print(f"Unregistered key: {e}")
            except KeyboardInterrupt:
                proxy.stop()
                return


if __name__ == "__main__":
    main()
