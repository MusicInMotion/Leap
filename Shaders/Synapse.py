from ShaderInterface import ShaderInterface

class Synapse(ShaderInterface):
    name = "Synapse"

    def params(self):
        return {'resolutionX_Synapse' : 0.5, 'resolutionY_Synapse' : 0.5, 'posX_Synapse' : 0, 'posY_Synapse' : 0, 'strength_Synapse' : 1}
        
    def fragShader(self):
        return  '''
					vec4 frag_color_Synapse;
					vec4 color_Synapse;
                    const vec2 resolutionX_Synapse_Range = vec2(screenWidth/2, screenWidth*1.5);
                    const vec2 resolutionY_Synapse_Range = vec2(screenHeight/2, screenHeight*1.5);  
                    const vec2 posX_Synapse_Range = vec2(0, 1000);
                    const vec2 posY_Synapse_Range = vec2(0, 1000);
                    const vec2 strength_Synapse_Range = vec2(0, 1);


                    uniform float resolutionX_Synapse;
                    uniform float resolutionY_Synapse;
                    uniform float posX_Synapse;
                    uniform float posY_Synapse; 
                    uniform float strength_Synapse;

                    vec2 pos_Synapse = vec2(scale(posX_Synapse, posX_Synapse_Range), scale(posY_Synapse, posY_Synapse_Range));
                    vec2 resolution_Synapse = vec2(scale(resolutionX_Synapse, resolutionX_Synapse_Range), scale(resolutionY_Synapse, resolutionY_Synapse_Range));
                    float strength_Synapse_Scaled = scale(strength_Synapse, strength_Synapse_Range);

                    mat2 rotate(float a) {
                        float c = cos(a),
                            s = sin(a);
                        return mat2(c, s, -s, c);
                    }

                    void main_Synapse() {
						color_Synapse = vec4(frag_color_Synapse);
                        vec2 uv = (2. * (gl_FragCoord.xy + pos_Synapse) - resolution_Synapse) / resolution_Synapse.y;

                        vec3 col = vec3(0.);
                        vec3 ray = vec3(uv, 1.);
                            
                        float s = .5;
                        for (int i = 0; i < 8; i++) {
                            ray = abs(ray) / dot(ray, ray);
                            ray -= s;
                            ray.xy *= rotate(time * .1);
                            ray.xz *= rotate(time * .1);
                            ray.yz *= rotate(time * .1);
                            s *= .95;
                            col += .01 / max(abs(ray.x), abs(ray.y));
                        }

                        color_Synapse = vec4(col, 1.) * strength_Synapse_Scaled;
                        color_Synapse += frag_color_Synapse;
                    }
                '''
