from __future__ import print_function
from sys import stderr
import glfw
import config

_left_is_down = False
_counter = 0


def error(error, description):
    print(description, file=stderr)


def mousebutton(window, button, action, mods):

    if action == glfw.RELEASE and button == glfw.MOUSE_BUTTON_LEFT:
        OnLeftUp()
    elif action == glfw.PRESS:
        if button == glfw.MOUSE_BUTTON_LEFT:
            OnLeftDown()
        elif button == glfw.MOUSE_BUTTON_RIGHT:
            OnRightDown()


def mouseposition(window, xpos, ypos):
    OnMouseMotion(xpos, ypos)


def key(window, key, scancode, action, mods):

    # Check for keypress
    if action != 1:
        return

    # TODO: Replace with pause menu
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)
        return

    items = config.parser.items("Controls")
    key_map = {}

    for action in actions:
        for item in items:
            if item[0] == action[0]:
                key_chars = item[1].split(",")

        for char in key_chars:
            if char.startswith("NP_"):
                if char == "NP_7":
                    keys = [375, 331]

                elif char == "NP_8":
                    keys = [377, 332]

                elif char == "NP_9":
                    keys = [380, 333]

                elif char == "NP_4":
                    keys = [376, 328]

                elif char == "NP_5":
                    keys = [383, 329]

                elif char == "NP_6":
                    keys = [378, 330]

                elif char == "NP_1":
                    keys = [382, 325]

                elif char == "NP_2":
                    keys = [379, 326]

                elif char == "NP_3":
                    keys = [382, 327]
            else:

                keys = [ord(char)]

            for key_code in keys:
                key_map[key_code] = action[1]

    if key in key_map:
        # FIXME: "Z" does not work?
        key_map[key]()


def OnTopLeft():
    print("OnTopLeft")


def OnTopCenter():
    print("OnTopCenter")


def OnTopRight():
    print("OnTopRight")


def OnMiddleLeft():
    print("OnMiddleLeft")


def OnMiddleRight():
    print("OnMiddleRight")


def OnBottomLeft():
    print("OnBottomLeft")


def OnBottomCenter():
    print("OnBottomCenter")


def OnBottomRight():
    print("OnBottomRight")


def OnRotLeft():
    print("OnRotLeft")


def OnRotRight():
    print("OnRotRight")


def OnRotUp():
    print("OnRotUp")


def OnRotDown():
    print("OnRotDown")


def OnRotClock():
    print("OnRotClock")


def OnRotCounterClock():
    print("OnRotCounterClock")


def OnLeftDown():
    global _left_is_down
    print("OnLeftDown")
    _left_is_down = True


def OnLeftUp():
    global _left_is_down
    print("OnLeftUp")
    _left_is_down = False


def OnRightDown():
    print("OnRightDown")


def OnMouseMotion(xpos, ypos):
    global _left_is_down
    if not _left_is_down:
        return

    print("OnMouseMotion", xpos, ypos)


actions = [
    ["topleft", OnTopLeft],
    ["topcenter", OnTopCenter],
    ["topright", OnTopRight],
    ["middleleft", OnMiddleLeft],
    ["middleright", OnMiddleRight],
    ["bottomleft", OnBottomLeft],
    ["bottomcenter", OnBottomCenter],
    ["bottomright", OnBottomRight],
    ["rotleft", OnRotLeft],
    ["rotright", OnRotRight],
    ["rotup", OnRotUp],
    ["rotdown", OnRotDown],
    ["rotclock", OnRotClock],
    ["rotcounterclock", OnRotCounterClock]
]
