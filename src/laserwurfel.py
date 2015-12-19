import callback

import glfw


def main():
    if not glfw.init():
        return False

    glfw.set_error_callback(callback.error)

    window = glfw.create_window(640, 480, "Hello, World", None, None)
    if not window:
        glfw.terminate()
        return False

    glfw.make_context_current(window)

    glfw.set_key_callback(window, callback.key)

    while not glfw.window_should_close(window):
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
    return True


if __name__ == "__main__":
    main()
