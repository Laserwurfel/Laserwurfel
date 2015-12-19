from __future__ import print_function
from sys import stderr
import glfw


def error(error, description):
    print(description, file=stderr)


def key(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)
