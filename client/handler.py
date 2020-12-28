import os
import threading
import time

from pynput import keyboard

from client.proto import Keys


class Handler:
    """ A handler will be registered for a Key and acts on its push and
        release actions.
    """

    def push(self, event):
        "Method to be called if a push event was received."
        raise NotImplementedError()

    def release(self, event):
        "Method to be called if a release event was received."
        raise NotImplementedError()

    def handle(self, event):
        "Handle an event."
        if event.is_push:
            self.push(event)
        else:
            self.release(event)

    def stop(self):
        "Method called to shut down a handler."
        pass


class KeystrokeHandler(Handler):
    "An extended handler to invoke a single keystroke."

    def __init__(self, keystroke):
        self._keystroke = keystroke
        self._keyboard = keyboard.Controller()

    def push(self, event):
        self._keyboard.press(self._keystroke)
        self._keyboard.release(self._keystroke)

    def release(self, event):
        pass


class KeyHoldHandler(Handler):
    "An handler to refire a keystroke until the hardware key is pressed."

    def __init__(self, keystroke, interval):
        self._keystroke = keystroke
        self._interval = interval
        self._keyboard = keyboard.Controller()

        self._active = False

    def _thread_worker(self):
        while self._active:
            self._keyboard.press(self._keystroke)
            time.sleep(self._interval)
            self._keyboard.release(self._keystroke)

    def push(self, event):
        self._active = True
        threading.Thread(target=self._thread_worker).start()

    def release(self, event):
        self._active = False


class ArrowShiftHandler(Handler):
    """ Handler for a special use case: send the badge's arrow keys to the
        system. Furthermore, toggle having the Shift key pressed by toggling
        another badge key, e.g., the A.

        This handler was especially written to play Work Adventure on the rC3.
    """

    def __init__(self, badge_shift_key, interval):
        self._interval = interval
        self._keyboard = keyboard.Controller()

        self._key = None
        self._shift = False

        self._handlers = {
            Keys.BTN_UP: lambda e: self._handle_arrow(e, keyboard.Key.up),
            Keys.BTN_RIGHT: lambda e: self._handle_arrow(e, keyboard.Key.right),
            Keys.BTN_DOWN: lambda e: self._handle_arrow(e, keyboard.Key.down),
            Keys.BTN_LEFT: lambda e: self._handle_arrow(e, keyboard.Key.left),
            badge_shift_key: lambda e: self._handle_shift(e),
        }

        self._active = True
        threading.Thread(target=self._thread_worker).start()

    def _handle_arrow(self, event, arrow_key):
        self._key = arrow_key if event.is_push else None

    def _handle_shift(self, event):
        if event.is_push:
            self._shift = not self._shift

    def _thread_worker(self):
        while self._active:
            k = self._key

            if not k:
                time.sleep(self._interval)
                continue

            if self._shift:
                with self._keyboard.pressed(keyboard.Key.shift):
                    self._keyboard.press(k)
                    time.sleep(self._interval)
                    self._keyboard.release(k)
            else:
                self._keyboard.press(k)
                time.sleep(self._interval)
                self._keyboard.release(k)

    def handle(self, event):
        self._handlers[event.key](event)

    def stop(self):
        self._active = False


class CmdHandler(Handler):
    "Execute a system command on key press."

    def __init__(self, cmd):
        self._cmd = cmd

    def push(self, event):
        os.system(self._cmd)

    def release(self, event):
        pass


class ProxyHandler(Handler):
    "A meta handler to dispatch an event to the right handler."

    def __init__(self):
        self._map = dict()

    def register(self, key, handler):
        "Register a new handler instance for a key."
        self._map[key] = handler

    def unregister(self, key):
        "Unregister a key's handler."
        try:
            self._map[key].stop()
        except KeyError:
            pass

        del self._map[key]

    def handle(self, event):
        self._map[event.key].handle(event)

    def stop(self):
        for _, handler in self._map.items():
            handler.stop()

        self._map = dict()
