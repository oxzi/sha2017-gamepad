import buttons
import display
import socket
import wifi


"TCP port to be bound to."
PORT = 2342


"Map of hardware buttons to protocol numbers."
BUTTONS = {
    buttons.BTN_UP: 0,
    buttons.BTN_RIGHT: 1,
    buttons.BTN_DOWN: 2,
    buttons.BTN_LEFT: 3,
    buttons.BTN_A: 4,
    buttons.BTN_B: 5,
    buttons.BTN_SELECT: 6,
    buttons.BTN_START: 7,
}


def encode_action(button, mode):
    """ Encodes an event to a byte to be sent over the network.
        The button is a button, to be mapped to a BUTTONS code from above.
        The boolean mode represents either a push (T) or a release (F).
    """
    return int(mode) << 4 | BUTTONS[button]


def create_server():
    """ Establish a WiFi connection, opens a TCP socket, and returns a
        tuple of a server socket and its own "public" IPv4 address.
    """
    wifi.connect()
    if not wifi.wait():
        raise ValueError("cannot establish WiFi connection")

    ip, _, _, _ = wifi._STA_IF.ifconfig()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", PORT))
    server_socket.listen(1)

    return ip, server_socket


def send_client(client_socket, button, push):
    "Send an encoded state to the client."
    client_socket.send(bytes([encode_action(button, push)]))


def display_connection(ip):
    "Prints connection details on the display."
    display.drawFill(0x000000)
    display.drawText(5, 5, "{}:{}".format(ip, PORT), 0xFFFFFF)
    display.flush()


ip, server_socket = create_server()
display_connection(ip)

while True:
    client_socket, _ = server_socket.accept()

    for button, code in BUTTONS.items():
        buttons.detach(button)
        buttons.attach(
            button, lambda push, button=button: send_client(client_socket, button, push)
        )
