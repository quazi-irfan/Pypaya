from Node import Node
from OpenGL.GL import *


class Mesh(Node):
    def __init__(self, name, geometry, material):
        super().__init__(name)

        self.geometry = geometry  # Why do you need to store the reference?
        self.material = material

        self.visible = True

        self.vaoRef = glGenVertexArrays(1)
        glBindVertexArray(self.vaoRef) # Activate the vaoRef
        for attribName, attribProp in self.geometry.attributes.items():
            glBindBuffer(GL_ARRAY_BUFFER, attribProp['ref'])
            attribRef = glGetAttribLocation(self.material.progRef, attribName)
            # glVertexAttribPointer(attribRef, attribProp['length'], attribProp['type'], GL_FALSE, attribProp['type'].bit_count() * attribProp['length'], ctypes.c_void_p(attribProp['offset']))
            glVertexAttribPointer(attribRef, 3, attribProp['type'], GL_FALSE, 12, ctypes.c_void_p(
                attribProp['offset']))  # 3 items, GL_FLOAT * 3 = 12; but we don't specify how many points
            glEnableVertexAttribArray(attribRef)
        glBindVertexArray(0)
