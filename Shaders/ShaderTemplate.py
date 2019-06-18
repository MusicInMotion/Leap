# See how to use this template in /desktop-app/README
from ShaderInterface import ShaderInterface

class SHADERNAME(ShaderInterface):
    name = “SHADERNAME”

    def params(self):
        return {'resolutionX_SHADERNAME’ : 1, 'resolutionY_SHADERNAME’ : 1[, MORE SHADER PARAMETERS HERE]}
        
    def fragShader(self):
        return  '''
	       vec4 frag_color_SHADERNAME;
	       vec4 color_SHADERNAME;
	
               uniform float resolutionX_SHADERNAME;
               const vec2 resolutionX_SHADERNAME_Range = vec2(screenWidth/4, screenWidth);

               uniform float resolutionY_SHADERNAME;
               const vec2 resolutionY_SHADERNAME_Range = vec2(screenHeight/4, screenHeight); 

               vec2 resolution_SHADERNAME_Scaled = vec2(scale(resolutionX_SHADERNAME, resolutionX_SHADERNAME_Range),
                                                        scale(resolutionY_SHADERNAME, resolutionY_SHADERNAME_Range));

			// SHADER CODE GOES HERE
                '''
