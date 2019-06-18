from importlib import import_module
import numpy as np
from GLSLInstance import GLSLInstance, Listener
from LeapSDK import *
# from Linux import Leap

# a collection of functions that take a frame of Leap hand data and return a standardized
#   value in the range [0, 100]
# can add more functions for other values the Leap reads & delivers
def PalmX(hand):
    return (np.clip(hand.palm_position.x, -500, 500) + 500) / 1000

def PalmY(hand):
    return (np.clip(hand.palm_position.y, 100, 600) - 100) / 500

def SphereX(hand):
    return (np.clip(hand.sphere_center.x, -500, 500) + 500) / 1000

def SphereY(hand):
    return (np.clip(hand.sphere_center.y, 100, 600) - 100) / 500

def SphereR(hand):
    return (np.clip(hand.sphere_radius - 30, 0, 100)) / 100

def Pinch(hand):
    return 1 if hand.pinch_strength > 0.98 else 0

def PalmRoll(hand):
    return (np.clip(hand.direction.y + 1, 0, 2)) / 2

def PalmPitch(hand):
    return (np.clip(hand.direction.x + 1, 0, 2)) / 2

def PalmYaw(hand):
    return (np.clip(hand.direction.z + 1, 0, 2)) / 2

def PalmVelX(hand):
    return (np.clip(hand.palm_velocity.x, -2000, 2000) + 2000) / 4000

def PalmVelY(hand):
    return (np.clip(hand.palm_velocity.y, -2000, 2000) + 2000) / 4000

def PalmVelZ(hand):
    return (np.clip(hand.palm_velocity.z, -2000, 2000) + 2000) / 4000

def pinch(hand):
    return hand.pinch_strength

def IndexDirX(hand):
	return (np.clip(hand.fingers.finger_type(Leap.Finger.TYPE_INDEX)[0].direction.y + 1, 0, 2)) / 2

class Combiner:
    # for each OpenGL -> Leap mapping, adds mapping to each hand's list of mappings
    def assignVars(self, leapMappings):
        progVars = {"Right" : [], "Left" : []}

        for gl, leap in leapMappings.items():
            leap = leap.split("_")
            hand, param = leap[0], leap[1]
            # each mapping is a pair of (OpenGL attribute, standardization function)
            progVars[hand].append((gl, globals()[param]))

        return progVars

    # given list of shaders to render and OpenGL -> Leap mappings, creates and runs 
    #   a combined shader using the given Leap mappings
    def run(self, shaders, mapping):
        # initialize some stuff common to all shaders
        initVars = {'time' : 0}
        fragShader = "#version 330\nout vec4 color;\nuniform float time;\nfloat scale(float r, vec2 range) {\n\treturn range.x + r * (range.y - range.x);\n}\n" + "const float screenWidth = {0};\nconst float screenHeight = {1};\n".format(1280,720)#format(pyautogui.size()[0], pyautogui.size()[1])
        main = "void main() { \n"
        input = "vec4 (0,0,0,0)"

        # add each shader, piping its output into the next shader's input
        for shader in shaders:
            if shader != "None":
                x = getattr(import_module("Shaders." + shader), shader)()
                initVars.update(x.params())
                fragShader += x.fragShader()
                main += "frag_color_" + shader + "=" + input + ";\n"
                main += "main_" + shader + "();\n"
                input = "color_" + shader

        main += "color = " + input + ";\n"
        main += "color.xy = color.yx;"
        fragShader += main + "}"

        progVars = self.assignVars(mapping)

        # runs for each frame of Leap data and updates shader through listener
        def on_frame_func(listener, controller):
            frame = controller.frame()

            for hand in frame.hands:
                if hand.is_right:
                    for (gl, param) in progVars["Right"]:
                        # for smoothing purposes, use weighted sum w/ last frame's values
                        listener.progVars[gl] = listener.progVars[gl] * 0.2 + param(hand) * 0.8
                else:
                    for (gl, param) in progVars["Left"]:
                        listener.progVars[gl] = listener.progVars[gl] * 0.2 + param(hand) * 0.8

        return (GLSLInstance, fragShader, Listener(on_frame_func, initVars), initVars.keys())