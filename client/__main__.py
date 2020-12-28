import socket

from pynput.keyboard import Key as kbd_key

from client.handler import *
from client.proto import Keys, unpack_event


def main():
    proxy = ProxyHandler()
    arrow_handler = ArrowShiftHandler(Keys.BTN_A, 0.1)
    for k in (Keys.BTN_UP, Keys.BTN_RIGHT, Keys.BTN_DOWN, Keys.BTN_LEFT, Keys.BTN_A):
        proxy.register(k, arrow_handler)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(("10.128.20.186", 2342))
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
