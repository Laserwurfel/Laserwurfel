from __future__ import unicode_literals

import os.path

import pyassimp
from OpenGL.GL import *
from array import array


class Asset:
    def __init__(self, path):
        if not isinstance(path, basestring):
            raise TypeError("Expected string", path)
        if not os.path.isfile(path):
            raise ValueError("Expected path", path)

        self._path = path

    def __enter__(self):
        scene = pyassimp.load(self._path)
        mesh = scene.meshes[0]

        self._vao = glGenVertexArrays(1)
        self._vbo = glGenBuffers(1)
        self._ebo = glGenBuffers(1)

        glBindVertexArray(self._vao)

        vertices = array(
            'f',
            [component for vertex in mesh.vertices for component in vertex],
        )
        glBindBuffer(GL_ARRAY_BUFFER, self._vbo)
        glBufferData(
            GL_ARRAY_BUFFER,
            vertices.tostring(),
            GL_STATIC_DRAW,
        )

        indices = array(
            'L',
            [component for face in mesh.faces for component in face],
        )
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._ebo)
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER,
            indices.tostring(),
            GL_STATIC_DRAW,
        )
        self._length = len(indices)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)

        glBindVertexArray(0)

        # free resources
        pyassimp.release(scene)

        return self._draw

    def __exit__(self, exc_type, exc_val, exc_tb):
        glDeleteVertexArrays(1, self._vao)
        glDeleteBuffers(1, self._vbo)
        glDeleteBuffers(1, self._ebo)

    def _draw(self):
        glBindVertexArray(self._vao)
        glDrawElements(GL_TRIANGLES, self._length, GL_UNSIGNED_INT, 0)
        glBindVertexArray(0)
