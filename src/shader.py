from OpenGL.GL import *


def compile(path, shader_type):
    with open(path) as f:
        source = f.read()
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(
            'Could not compile shader',
            glGetShaderInfoLog(shader),
        )
    return shader


def program(*shaders):
    shader_program = glCreateProgram()

    for shader in shaders:
        glAttachShader(shader_program, shader)

    glLinkProgram(shader_program)

    if glGetProgramiv(shader_program, GL_LINK_STATUS) != GL_TRUE:
        info = glGetProgramInfoLog(shader_program)
        glDeleteProgram(shader_program)
        for shader in shaders:
            glDeleteShader(shader)
        raise RuntimeError(
            'Could not link shader program',
            info,
        )

    for shader in shaders:
        glDeleteShader(shader)

    return shader_program
