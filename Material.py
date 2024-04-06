# glBindVertexArray
from OpenGL.GL import *

# compileProgram
from OpenGL.GL.shaders import *

class Material:
    # subclass, compile shaders, add uniform and their types in dictionary.
    def __init__(self, vertex_shader, fragment_shader):
        # there should be better way than creating a temp/dummy vao just to compile a shader
        temp_vao = glGenVertexArrays(1)
        glBindVertexArray(temp_vao)
        self.progRef = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER),
                                      compileShader(fragment_shader, GL_FRAGMENT_SHADER))
        glBindVertexArray(0)

        self.uniform = {}
        self.settings = {}

    def addUniform(self, name, type, val=None):
        uniformRef = glGetUniformLocation(self.progRef, name)
        self.uniform[name] = {'ref': uniformRef, 'type': type, 'val': val}


class BasicMaterial(Material):
    vertex_shader = '''
    #version 330 core

    in vec3 vertex_position;
    in vec3 vertex_color;
    out vec3 pass_vertex_color;

    uniform mat4 projectionMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 modelMatrix; 

    void main(){
        gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertex_position, 1.0);
        pass_vertex_color = vertex_color;
    }
    '''

    fragment_shader = '''
    #version 330 core

    in vec3 pass_vertex_color;

    uniform vec3 base_color;
    uniform bool use_Vertex_Color;
    out vec4 fragment_color;

    void main(){
        fragment_color = vec4(base_color, 1.0);

        if (use_Vertex_Color)
            fragment_color *= vec4(pass_vertex_color, 1.0);       
    }
    '''

    def __init__(self):
        super().__init__(self.vertex_shader,
                         self.fragment_shader)  # how can i access variable declard in class body without self

        self.addUniform('projectionMatrix', 'mat4')
        self.addUniform('viewMatrix', 'mat4')
        self.addUniform('modelMatrix', 'mat4')

        self.addUniform('base_color', 'vec3', [.3, .8, .5])
        self.addUniform('use_Vertex_Color', 'bool', True)

        self.settings['draw_mode'] = GL_TRIANGLES