from ShaderInterface import ShaderInterface

class Aesthetic(ShaderInterface):
    name = "Aesthetic"

    def params(self):
        return {'resolutionX_Aesthetic' : 1, 'resolutionY_Aesthetic' : 1, 'xZoom_Aesthetic' : 1, 'yZoom_Aesthetic' : 1, 'rate_Aesthetic' : 1, 'strength_Aesthetic' : 1}
        
    def fragShader(self):
        return  '''
                    precision mediump float;

                    uniform float resolutionX_Aesthetic;
                    uniform float resolutionY_Aesthetic;
                    vec4 frag_color_Aesthetic;
                    vec4 color_Aesthetic;
                    uniform float xZoom_Aesthetic;
                    uniform float yZoom_Aesthetic;
                    uniform float rate_Aesthetic;
                    uniform float strength_Aesthetic;

                const vec2 xZoom_Aesthetic_Range = vec2(0, 1);
                const vec2 yZoom_Aesthetic_Range = vec2(0, 1); 
                float xZoom_Aesthetic_Scaled = scale(xZoom_Aesthetic, xZoom_Aesthetic_Range);
                float yZoom_Aesthetic_Scaled = scale(yZoom_Aesthetic, yZoom_Aesthetic_Range);

                const vec2 resolutionX_Aesthetic_Range = vec2(screenWidth/4, screenWidth);
                const vec2 resolutionY_Aesthetic_Range = vec2(screenHeight/4, screenHeight); 
                const vec2 strength_Aesthetic_Range = vec2(0, 1);
                vec2 resolution_Aesthetic = vec2(scale(resolutionX_Aesthetic, resolutionX_Aesthetic_Range), scale(resolutionY_Aesthetic, resolutionY_Aesthetic_Range));

                float strength_Aesthetic_Scaled = scale(strength_Aesthetic, strength_Aesthetic_Range);

                    #define LINES 10.0

                      
                    void main_Aesthetic() {
                      float x, y, xpos, ypos;
                      float t = time * 12.0 * rate_Aesthetic;
                      vec3 c = vec3(0.0);

                      xpos = (gl_FragCoord.x / resolution_Aesthetic.x) * xZoom_Aesthetic_Scaled;
                      ypos = (gl_FragCoord.y / resolution_Aesthetic.y) * yZoom_Aesthetic_Scaled;
                      
                      x = xpos;
                      for (float i = 0.0; i < LINES; i += 5.0) {
                        y = ypos + (
                            0.146 * cos(x * 10.100 + i * 0.4 + t * 0.10)
                          + 0.101 * cos(x * 4.350 + i * 1.7 + t * 0.20)
                          + 0.120 * sin(x * 5.0 + i * 0.8 + t * 0.14)
                          + 0.59
                        );
                        
                        c.r += (1.0 - pow(clamp(abs(1.0 - y) * 0.1, 0.0, 1.1) , 0.1));
                          
                        c.g += (1.0 - pow(
                          clamp(abs(1.4 - y) * 0.5, 0.09, 1.5)  
                        , 0.1));
                        
                        c.b += (pow(
                          clamp(abs(1.4 - y) * 6.0, 9.1, 4.5)  
                        , 0.5));
                      }
                      
                      color_Aesthetic = vec4(c, 1.0) * strength_Aesthetic_Scaled;
                      color_Aesthetic += frag_color_Aesthetic;

                    }
                '''
