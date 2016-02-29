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
    glfw.window_hint(glfw.RESIZABLE, False)

    glfw.set_error_callback(callback.error)

    # create window
    window = glfw.create_window(640, 480, "Laserwurfel", None, None)
    if not window:
        glfw.terminate()
        return False
    glfw.make_context_current(window)

    glfw.set_key_callback(window, callback.key)

    # load shaders
    shader_program = shader.program(
        shader.compile('src/shaders/vertex.glsl', GL_VERTEX_SHADER),
        shader.compile('src/shaders/fragment.glsl', GL_FRAGMENT_SHADER),
    )

    # load models
    (cube, faces) = model.import_asset('assets/models/game_elements/cube_01.blend')

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClearColor(0.0, 0.5, 1.0, 1.0)  # TODO proper background color
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(shader_program)
        glBindVertexArray(cube)
        glDrawElements(GL_TRIANGLES, faces, GL_UNSIGNED_INT, 0)
        glBindVertexArray(0)

        glfw.swap_buffers(window)

    glfw.terminate()
    return True


if __name__ == "__main__":
    main()
