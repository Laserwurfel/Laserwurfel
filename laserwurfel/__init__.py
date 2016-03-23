from __future__ import unicode_literals

import os.path

import glfw
from OpenGL.GL import *

import callback
import model
import shader


def main():
    os.chdir(os.path.join(
        os.path.dirname(__file__),
        '..',
    ))

    if not glfw.init():
        return False

    # setup OpenGL to core 3.3
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, GL_FALSE)

    glfw.set_error_callback(callback.error)

    # create window
    window = glfw.create_window(640, 480, "Laserwurfel", None, None)
    if not window:
        glfw.terminate()
        return False
    glfw.make_context_current(window)

    glfw.set_key_callback(window, callback.key)
    glfw.set_mouse_button_callback(window, callback.mousebutton)
    glfw.set_cursor_pos_callback(window, callback.mouseposition)

    glViewport(0, 0, 640, 480)

    # create and load shaders
    program = shader.program([
        ('src/shaders/vertex.glsl', GL_VERTEX_SHADER),
        ('src/shaders/fragment.glsl', GL_FRAGMENT_SHADER),
    ])

    # glfw.swap_interval(1)

    cube = model.Asset('assets/models/game_elements/cube_01.obj')

    # with cube as cube:
    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClearColor(0.0, 0.5, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(program)
        # cube()

        glfw.swap_buffers(window)
    glfw.terminate()
    return True


if __name__ == "__main__":
    main()
