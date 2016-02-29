from __future__ import unicode_literals

import pyassimp
from OpenGL.GL import *
from array import array


def import_asset(file):
    scene = pyassimp.load(file)
    mesh = scene.meshes[0]

    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    ebo = glGenBuffers(1)

    glBindVertexArray(vao)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(
        GL_ARRAY_BUFFER,
        array(
            'f',
            [component for vertex in mesh.vertices for component in vertex],
        ).tostring(),
        GL_STATIC_DRAW,
    )

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(
        GL_ARRAY_BUFFER,
        array(
            'L',
            [component for face in mesh.faces for component in face],
        ).tostring(),
        GL_STATIC_DRAW,
    )

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)

    glBindVertexArray(0)

    # don't forget this one, or you will leak!
    pyassimp.release(scene)

    return (vao, len(mesh.faces))
