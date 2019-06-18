from ShaderInterface import ShaderInterface

class Shader6(ShaderInterface):
    name = "Shader6"

    def params(self):
        return {'resolutionX_Shader6' : 1, 'resolutionY_Shader6' : 1, 'rate_Shader6' : 1, 'xTilt_Shader6' : 1, 'yTilt_Shader6' : 1, 'depth_Shader6' : 1, 'zoom_Shader6' : 1, 'strength_Shader6' : 1}
        
    def fragShader(self):
        return  '''
                    #ifdef GL_ES
                    precision mediump float;
                    #endif

                    #extension GL_OES_standard_derivatives : enable

                    vec4 frag_color_Shader6;
                    vec4 color_Shader6;
                    uniform vec2 mouse;
                    uniform float resolutionX_Shader6;
                    uniform float resolutionY_Shader6;
                    uniform strength_Shader6;

                const vec2 resolutionX_Shader6_Range = vec2(720, 2160);
                const vec2 resolutionY_Shader6_Range = vec2(405, 1215); 
                const vec2 strength_Shader6_Range = vec2(0, 1);
                vec2 resolution_Shader6 = vec2(scale(resolutionX_Shader6, resolutionX_Shader6_Range), scale(resolutionY_Shader6, resolutionY_Shader6_Range));

                    uniform float strength_Shader6;
                float strength_Shader6_Scaled = scale(strength_Shader6, strength_Shader6_Range);

                    uniform float rate_Shader6;
                    uniform float depth_Shader6;
                    uniform float xTilt_Shader6;
                    uniform float yTilt_Shader6;
                    uniform float zoom_Shader6;



                    void main_Shader6() {
                        vec2 uv = (2. * gl_FragCoord.xy - resolution_Shader6) / resolution_Shader6.y;
                        
                        mat2 rot = mat2(.707, -.707, .707, .707) * zoom_Shader6;

                        uv *= rot;

                        uv = 2.0 * fract(uv) - 1.0; 
                        
                        uv = abs(uv) - 0.4 + 0.1 * sin(time * rate_Shader6) * depth_Shader6;
                        uv.x *= xTilt_Shader6;
                        uv.y *= yTilt_Shader6;
                        
                        
                        float a = 0.5+ 0.05 * cos(8.0 * atan(uv.y, uv.x));
                        float d = pow(.04 / abs(length(uv) - a), 4.0);
                        d = clamp(sin(d*time), 0.0, 1.0);
                        vec3 col = mix(vec3(0, 0, 0), vec3(1, 0, 0), d);
                            

                        color_Shader6 = vec4(col, 1.) * strength_Shader6_Scaled;
                        color_Shader6 += frag_color_Shader6;
                    }
                '''
