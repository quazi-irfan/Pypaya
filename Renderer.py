# https://www.loc.gov/preservation/digital/formats/fdd/fdd000507.shtml
# https://www.martinreddy.net/gfx/3d/OBJ.spec
# https://pypi.org/project/PyWavefront/#history
# https://github.com/pyglet/pyglet/blob/master/pyglet/graphics/vertexarray.py
# https://learnopengl.com/Guest-Articles/2021/Scene/Scene-Graph
# https://www.songho.ca/opengl/gl_projectionmatrix.html
# https://learnopengl.com/Getting-started/Coordinate-Systems
# https://lisyarus.github.io/blog/programming/2023/02/21/exponential-smoothing.html

# local transformation means pivoting around current parent
# numpy.linalg.inv(mesh.parent.modelMatrix) @ mesh.modelMatrix
# mesh.modelMatrix @ Transformation
# global transformation means pivoting around root


import glfw
from OpenGL.GL import *
from Mesh import Mesh

class Renderer:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height

        glfw.init()

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        self.window = glfw.create_window(width, height, title, None, None)
        glfw.make_context_current(self.window)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        # glEnable(GL_CULL_FACE)
        # glPolygonMode(GL_FRONsT_AND_BACK, GL_LINE)

    def render(self, rootNode, cameraNode):
        import numpy

        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # cameraNode.modelMatrix = numpy.linalg.inv(cameraNode.modelMatrix) @ cameraNode.modelMatrix

        def renderMesh(meshNode, accu_modelMatrix):
            glUseProgram(meshNode.material.progRef)
            glBindVertexArray(meshNode.vaoRef)

            for uniformName, uniformProp in meshNode.material.uniform.items():
                if uniformName == 'projectionMatrix':
                    glUniformMatrix4fv(uniformProp['ref'], 1, GL_TRUE, cameraNode.projectionMatrix)  # cameraNode
                elif uniformName == 'viewMatrix':
                    glUniformMatrix4fv(uniformProp['ref'], 1, GL_TRUE, numpy.linalg.inv(cameraNode.modelMatrix))  #
                elif uniformName == 'modelMatrix':
                    glUniformMatrix4fv(uniformProp['ref'], 1, GL_TRUE, accu_modelMatrix)
                else:
                    # we need to look at uniformProp['type'] to find the function we will be calling
                    if uniformProp['type'] == 'vec3':
                        glUniform3f(uniformProp['ref'], *uniformProp['val'])
                    elif uniformProp['type'] == 'bool':
                        glUniform1i(uniformProp['ref'], uniformProp['val'])
                    else:
                        # other uniform data type
                        pass

            # glVertexAttribPointer specified how to read the buffer
            # glDrawArrays reads certain number of vertex the specification defined by glVertexAttribPointer
            # glDrawArrays takes the start index of the enabled array and number of vertices to render
            glDrawArrays(meshNode.material.settings['draw_mode'], 0, meshNode.geometry.attributes['vertex_position'][
                'length'])  # there could be a better way than getting vertex count from vertex position
            glBindVertexArray(meshNode.vaoRef)


        def render_dfs(node, accu_modelMatrix):
            if isinstance(node, Mesh):
                # https://stackoverflow.com/questions/3807754/confused-about-frustum-culling
                # if the mesh is outside fo frustum then we can skip it, we will be avoiding additional work
                # frustum calling works with simplified version of an object
                renderMesh(node, accu_modelMatrix)

            if not node.children:
                return

            for n in node.children:
                render_dfs(n, accu_modelMatrix @ n.modelMatrix)

        render_dfs(rootNode, rootNode.modelMatrix)