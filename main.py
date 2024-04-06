import sys
sys.setrecursionlimit(2000)


import glfw
import random
from Renderer import Renderer
from Node import * # Node, Camera
from Mesh import * # Mesh
from Material import * # Material, Basic Material
# Geometry, TriangleGeometry, RectangularGeometry, BoxGeometry, PolygonGeometry, ParametricGeometry, PlaneGeometry
from Geometry import * 

class Texture:
    pass

width, height = 800, 600
renderer = Renderer(width, height, "Pypaya 0.0.1") # initializes glfw

def keyboard_callback(window, key, scancode, action, mods):
    global move
    if action == glfw.PRESS:
        move = not move

# This can be called because glfw.init() was called already by Renderer.__init__
# glfw.set_cursor_pos_callback(self.window, self.cursor_position_callback);
glfw.set_key_callback(renderer.window, keyboard_callback)


cameraNode = Camera(width, height)
rootNode = Node('root')

temp = rootNode
for i in range(1000):
    newMesh = Mesh(str(i), BoxGeometry(random.random(),random.random(),random.random()), BasicMaterial())
    newMesh.translate(random.randint(-1, 1) / 10, random.randint(-1, 1) / 10, random.randint(-1, 1) / 10)
    newMesh.rotate(['x','y','z'][random.randint(0, 2)], 5)
    temp.addChild(newMesh)
    temp = newMesh

import time, math

move = False

tempMesh = Mesh('temp', BoxGeometry(1,1,1), BasicMaterial())
rootNode.addChild(tempMesh)
while not glfw.window_should_close(renderer.window):
    glfw.poll_events()

    # move between -1 and 1 along x axis
    # tempMesh.translate(math.sin(time.time()) / 20, 0, 0)
    # print(move)

    rootNode.rotate('y', 0.01)
    # nextMesh = rootNode
    # rootNode.rotate('y', 0.01)
    # for i in range(1000):
    #     nextMesh.rotate('z', random.random()/100)
    #     nextMesh = nextMesh.children[0]
    # rootNode.rotate('z', 0.001)

    # print(glfw.get_cursor_pos(renderer.window))

    if glfw.get_key(renderer.window, glfw.KEY_W) == glfw.PRESS:
        cameraNode.modelMatrix = Matrix.translate(0, 0, -0.1) @ cameraNode.modelMatrix
    if glfw.get_key(renderer.window, glfw.KEY_S) == glfw.PRESS:
        cameraNode.modelMatrix = Matrix.translate(0, 0,0.1) @ cameraNode.modelMatrix
    if glfw.get_key(renderer.window, glfw.KEY_A) == glfw.PRESS:
        cameraNode.modelMatrix = Matrix.translate(-0.1, 0,0) @ cameraNode.modelMatrix
    if glfw.get_key(renderer.window, glfw.KEY_D) == glfw.PRESS:
        cameraNode.modelMatrix = Matrix.translate(0.1, 0,0) @ cameraNode.modelMatrix
    if glfw.get_key(renderer.window, glfw.KEY_Q) == glfw.PRESS:
        cameraNode.modelMatrix = Matrix.translate(0, 0.1,0) @ cameraNode.modelMatrix
    if glfw.get_key(renderer.window, glfw.KEY_Z) == glfw.PRESS:
        cameraNode.modelMatrix = Matrix.translate(0, -0.1,0) @ cameraNode.modelMatrix

    renderer.render(rootNode, cameraNode)

    glfw.swap_buffers(renderer.window)

# need to clean up compiled shaders too
glfw.terminate()
