# SHA2017 Gamepad

Use your [SHA2017 badge][sha2017-badge] as a gamepad, especially for the [rC3][rc3].


## Badge / Server

The badge starts a trivial TCP server to send keystrokes to a connecting client.
To install the app on your badge, just use your badge's app installer.
The server app is available in the [badge.team Hatchery][badge-team-gamepad].

After starting up the app, it will connect to the configured WiFi and starts listening on a TCP port.
The connection details (IP address and port) will be written on the badge's screen.


## Client

After firing up your badge, you can establish a connection from your computer to the badge.
The client code handles the messages and translates them to keystrokes for your machine.

```
$ python -m client -h
usage: sha2017-gamepad [-h] host [port]

SHA2017 badge gamepad

positional arguments:
  host        Badge's host resp. IP
  port        Badge's port, defaults to 2342

optional arguments:
  -h, --help  show this help message and exit
```

The current configuration is particularly suitable as a gamepad for a [WorkAdventure][work-adventure], e.g., at the [rC3][rc3].

The script requires [pynput][] to be installed.


[badge-team-gamepad]: https://badge.team/projects/gamepad
[pynput]: https://github.com/moses-palmer/pynput
[rc3]: https://rc3.world/rc3/
[sha2017-badge]: https://wiki.sha2017.org/w/Projects:Badge
[work-adventure]: https://workadventu.re/
