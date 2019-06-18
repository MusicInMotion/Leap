from ShaderInterface import ShaderInterface

class Eyeball(ShaderInterface):
    name = "Eyeball"

    def params(self):
        return {'resolutionX_Eyeball' : 1, 'resolutionY_Eyeball' : 1, 'eyeX_Eyeball' : 1, 'eyeY_Eyeball' : 1, 'strength_Eyeball' : 1}
        
    def fragShader(self):
        return  '''
                    #ifdef GL_ES
                    precision mediump float;
                    #endif

                    uniform float eyeX_Eyeball;                                                                                                                                                           
                    uniform float eyeY_Eyeball;
                    vec2 mouse_Eyeball = vec2(eyeX_Eyeball*sin(time), eyeY_Eyeball*cos(time));
                    vec4 color_Eyeball;                                                                                                                                                                    
                    vec4 frag_color_Eyeball;                                                                                                                                                               
                    uniform float strength_Eyeball;                                                                                                                                                        

                    const vec2 resolutionX_Eyeball_Range = vec2(screenWidth/4, screenWidth);
                    const vec2 resolutionY_Eyeball_Range = vec2(screenHeight/4, screenHeight);
                    const vec2 strength_Eyeball_Range = vec2(0, 1);
                    uniform float resolutionX_Eyeball;
                    uniform float resolutionY_Eyeball;
                    vec2 resolution_Eyeball = vec2(scale(resolutionX_Eyeball, resolutionX_Eyeball_Range), scale(resolutionY_Eyeball, resolutionY_Eyeball_Range));

                    float strength_Eyeball_Scaled = scale(strength_Eyeball, strength_Eyeball_Range);

                    vec2 mouse2 = mouse_Eyeball*2.0-1.0;

                    #define RADIANS 0.017453292

                    float eye_Eyeball(vec3 p) {
                      return length(p) - 1.0;
                    }

                    vec3 texture_Eyeball(vec3 n) {
                      vec3 e = normalize(vec3(mouse2.x, mouse2.y, -1.0)) - n;
                            float r = length(e);

                      float iris = 0.33;
                      float pupil = 0.11;
                      
                      if(r<iris) {
                        r *=2.5;
                        float d = smoothstep(-5.0, 5.0, min(sin(e.y*4.0/e.x*3.1431)-0.74, cos(e.x*3.1432/e.y*3.14321)-1.2))*2.0;
                          
                        if(r < pupil) return vec3(0.0);
                      
                        float s = r-pupil;
                        
                        vec3 c = mix(mix(vec3(0.0), mix(vec3(0.0, 0.28, 0.45)*5.0, vec3(0.0, 0.31, 0.55)*2.5 , abs(sin(d*0.4 + (s-pupil)/(iris-pupil)))*0.5+1.5),
                              abs(sin((r-pupil)/(iris-pupil)))), vec3(1.0), 1.0-smoothstep(0.0, 1.0, 1.0-(s-pupil)/s*0.25));
                        return c;
                      }

                      return mix(vec3(0.3),vec3(1.0), smoothstep(0.0, 1.0, (r-iris)/0.02));
                    }

                    void main_Eyeball()
                    {
                        vec2 uv = ((gl_FragCoord.xy / resolution_Eyeball.xy) * 2.0 - 1.0);
                        float t = time;
                        float aspect = resolution_Eyeball.x / resolution_Eyeball.y + (t*0.00000001);
                        float fov    = tan( 70.0 * RADIANS * 0.5); 
                        vec3 origin = vec3(0.0, 0.0, -2.0);
                        vec3 dir = normalize( vec3( uv.x * aspect * fov, uv.y * fov, 1.0) );
                        vec3 ray = origin;
                        float d;
                        for(int i=0;i<15;i++)
                        {
                            d = eye_Eyeball(ray);
                            ray += dir * d;
                        }
                        vec3 n = normalize(sin(ray));
                        vec3 e = normalize(vec3(mouse_Eyeball.x*2.0-1.0, mouse_Eyeball.y*2.0-1.0, -1.0)) - n;
                        vec3 c = texture_Eyeball(normalize(n));
                        float s = 1.0 - length(vec3(0.0, 0.0, -1.0) - n) * length(e); 
                        vec4 ccc =vec4(vec3(c*s), 1.0);
                        color_Eyeball = ccc * strength_Eyeball_Scaled;
                        color_Eyeball += frag_color_Eyeball;
                    }

                '''
