from ShaderInterface import ShaderInterface

class Shader5(ShaderInterface):
	# source: http://glslsandbox.com/e#53878.0
    name = "Shader5"

    def params(self):
        return {}
        
    def fragShader(self):
        return  '''
					vec4 frag_color_Shader5;
					vec4 color_Shader5;
					
					// no idea how to get this to work since we don't have a vertex shader to grab this from
					in vec2 surfacePosition;
					
					#define MAX_ITER 4.0
					void main_Shader5(  ) {
						vec2 p = surfacePosition*22.0;
						vec2 i = p;
						float c = 0.0;
						float inten = 0.15;
						float r = length(p+vec2(sin(time),sin(time*0.833+2.))*3.);
						
						for (float n = 0.0; n < MAX_ITER; n++) {
							float t = r-time * (1.0 - (1.9 / (n+1.)));
								  t = r-time/(n+0.6);//r-sin(time) * (1.0 + (0.5 / float(n+1.)));
							i -= p + vec2(
								cos(t - i.x-r) + sin(t + i.x), 
								sin(t - i.y) + cos(t + i.x)+r
							);
							c += 1.0/length(vec2(
								(sin(i.x+t)/inten),
								(cos(i.y+t)/inten)
								)
							);
						
						}
						c /= float(MAX_ITER);

						color_Shader5 = frag_color_Shader5;
						color_Shader5 += vec4(vec3(c,c,c)*vec3(2.4, 2.0, 2.5)-0.15, 1.0);
					}
                '''
