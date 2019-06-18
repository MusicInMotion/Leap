from ShaderInterface import ShaderInterface

class Lagoon(ShaderInterface):
    name = "Lagoon"
        
    def params(self):
    	return {'resolutionX_Lagoon' : 1, 'resolutionY_Lagoon' : 1, 'rate1_Lagoon' : 1, 'rate2_Lagoon' : 1, 'rate3_Lagoon' : 1, 'rate4_Lagoon' : 1, 'rate5_Lagoon' : 1, 'strength_Lagoon' : 1}
        
    def fragShader(self):
        return  '''
					vec4 frag_color_Lagoon;
					vec4 color_Lagoon;
                    const vec2 resolutionX_Lagoon_Range = vec2(screenWidth/4, screenWidth);
                    const vec2 resolutionY_Lagoon_Range = vec2(screenHeight/4, screenHeight);
                    const vec2 rate1_Lagoon_Range = vec2(0, 1);
                    const vec2 rate2_Lagoon_Range = vec2(0, 1);
                    const vec2 rate3_Lagoon_Range = vec2(0, 1);
                    const vec2 rate4_Lagoon_Range = vec2(0, 1);
                    const vec2 rate5_Lagoon_Range = vec2(0, 1);
                    const vec2 strength_Lagoon_Range = vec2(0, 1); 


                    uniform float resolutionX_Lagoon;
                    uniform float resolutionY_Lagoon;
                    vec2 resolution_Lagoon = vec2(scale(resolutionX_Lagoon, resolutionX_Lagoon_Range), scale(resolutionY_Lagoon, resolutionY_Lagoon_Range));
                    uniform float rate1_Lagoon;
                    uniform float rate2_Lagoon;
                    uniform float rate3_Lagoon;
                    uniform float rate4_Lagoon;
                    uniform float rate5_Lagoon;
                    uniform float strength_Lagoon;

                    float rate1_Lagoon_Scaled = scale(rate1_Lagoon, rate1_Lagoon_Range);
                    float rate2_Lagoon_Scaled = scale(rate2_Lagoon, rate2_Lagoon_Range);
                    float rate3_Lagoon_Scaled = scale(rate3_Lagoon, rate3_Lagoon_Range); 
                    float rate4_Lagoon_Scaled = scale(rate4_Lagoon, rate4_Lagoon_Range); 
                    float rate5_Lagoon_Scaled = scale(rate5_Lagoon, rate5_Lagoon_Range); 
                    float strength_Lagoon_Scaled = scale(strength_Lagoon, strength_Lagoon_Range); 

                    void main_Lagoon() {
                        color_Lagoon = vec4(frag_color_Lagoon);

                        vec2 position = ( gl_FragCoord.xy / resolution_Lagoon.xy);

                        float c = 0;
                        c += sin( position.x * cos( time*rate1_Lagoon_Scaled / 15.0 ) * 80.0 ) + cos( position.y * cos( time*rate1_Lagoon_Scaled / 15.0 ) * 10.0 );
                        c += sin( position.y * sin( time*rate2_Lagoon_Scaled / 10.0 ) * 40.0 ) + cos( position.x * sin( time*rate2_Lagoon_Scaled / 25.0 ) * 40.0 );
                        c += sin( position.x * sin( time*rate3_Lagoon_Scaled / 5.0 ) * 10.0 ) + sin( position.y * sin( time*rate3_Lagoon_Scaled / 35.0 ) * 80.0 );
                        c *= sin( time*rate4_Lagoon_Scaled / 10.0 ) * 0.5;

                        vec4 c_vec = vec4(vec3(c, c * 0.5, sin(c + time*rate5_Lagoon_Scaled / 3.0) * 0.75), 1.0);
                        color_Lagoon = c_vec * strength_Lagoon_Scaled;
                        color_Lagoon += frag_color_Lagoon;
                    }
                '''
