import moderngl
import pyautogui
import numpy as np
# from Linux import Leap
from LeapSDK import Leap

#Instance of GLSL shader creating and aggregating Leap and ModernGL objects for rendering
class GLSLInstance:
    WINDOW_SIZE = pyautogui.size()

    def __init__(self, fragShader, listener, glVars):
        #Leap objects
        self.listener = listener
        self.controller = Leap.Controller()
        self.controller.add_listener(self.listener)

        #ModernGL context exposes OpenGL features
        #Currently creates simplest framework necessary to render a shader
        #specified through fragShader passed into constructor
        self.ctx = moderngl.create_context()

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec2 vert;
                void main() {
                    gl_Position = vec4(vert, 0.0, 1.0);
                }
            ''',
            fragment_shader=fragShader,)

        #Desired uniform vars to edit in realtime (<= total # of uniform vars)
        self.proVars = dict()
        for var in glVars:
            self.proVars[var] = self.prog[var]
        self.time = self.prog['time']

        vertices = np.array([
            1.0, 1.0,

            1.0, -1.0,

            -1.0, 1.0,

            -1.0, -1.0,
        ])

        self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'vert')

    #updates ModernGL uniforms and renders shader
    def render(self):
        self.ctx.viewport = self.wnd.viewport
        self.ctx.clear(1.0, 1.0, 1.0)
        self.time.value = self.wnd.time

        for progItem, progVal in zip(self.proVars.items(), self.listener.progVars.values()):
            if progItem[0] == 'time':
                self.time.value += progVal;
            else:
                progItem[1].value = progVal
        self.vao.render(mode=5)

# Override Leap listener class - defines on_frame callback function to respond to Leap
# controller. Stores reference to OpenGL uniforms that can be manipulated by user movements
class Listener(Leap.Listener):
    def __init__(self, on_frame_func, progVars):
        Leap.Listener.__init__(self)
        self.on_frame_func = on_frame_func
        self.progVars = dict()
        for var, value in progVars.items():
            self.progVars[var] = value

    def on_frame(self, controller):
        self.on_frame_func(self, controller)
