import os.path

import OpenGL.constant
from OpenGL.GL import *


def program(shaders):
    for shader in shaders:
        if not type(shader) == tuple:
            raise TypeError("Expected a tuple", shader)
        if not len(shader) == 2:
            raise TypeError("Expected a pair", shader)

        if not isinstance(shader[0], basestring):
            raise TypeError("Expected first element to be a string", shader)
        if not os.path.isfile(shader[0]):
            raise ValueError("Expected first elements to be a file", shader)
        if not os.path.splitext(shader[0])[1] == ".glsl":
            raise ValueError(
                "Expected first element to be a .glsl file",
                shader,
            )

        if not isinstance(shader[1], OpenGL.constant.IntConstant):
            raise TypeError(
                "Expected second element to be an OpenGL constant",
                shader,
            )
        if not shader[1] in (
            GL_VERTEX_SHADER,
            GL_GEOMETRY_SHADER,
            GL_FRAGMENT_SHADER,
        ):
            raise ValueError(
                "Expected second element to be a valid shader stage",
                shader,
            )

    for index, (path, stage) in enumerate(shaders):
        with open(path, 'r') as f:
            source = f.read()
        shader = glCreateShader(stage)
        glShaderSource(shader, source)
        glCompileShader(shader)
        if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
            raise RuntimeError(
                'Could not compile shader',
                stage,
                glGetShaderInfoLog(shader),
            )

        shaders[index] = shader

    program = glCreateProgram()
    for shader in shaders:
        glAttachShader(program, shader)
    glLinkProgram(program)

    if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
        info = glGetProgramInfoLog(program)
        glDeleteProgram(program)
        for shader in shaders:
            glDeleteShader(shader)
        raise RuntimeError(
            'Could not link shader program',
            info,
        )

    for shader in shaders:
        glDeleteShader(shader)

    return program
