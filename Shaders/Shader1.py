from ShaderInterface import ShaderInterface

class Shader1(ShaderInterface):
	# source: http://glslsandbox.com/e#53927.0
    name = "Shader1"

    def params(self):
        return {'resolutionX_Shader1' : 1, 'resolutionY_Shader1' : 1, 'posX_Shader1' : 1}
        
    def fragShader(self):
        return  '''
					vec4 frag_color_Shader1;
					vec4 color_Shader1;
					const vec2 resolutionX_Shader1_Range = vec2(screenWidth/4, screenWidth);
                    const vec2 resolutionY_Shader1_Range = vec2(screenHeight/4, screenHeight);
                    const vec2 posX_Shader1_Range = vec2(5., 10.);
                    
					uniform float resolutionX_Shader1;
					uniform float resolutionY_Shader1;
					uniform float posX_Shader1;

					vec2 resolution_Shader1 = vec2(scale(resolutionX_Shader1, resolutionX_Shader1_Range), scale(resolutionY_Shader1, resolutionY_Shader1_Range));
						
					vec4 mainImage_Shader1( vec3 O )
					{
						vec2 u = O.xy;
						float r = floor(30.0 * scale(posX_Shader1, posX_Shader1_Range)+1.0);
						vec2 R = resolution_Shader1, 
							 U = u+u-R,
							 p = vec2(log(length(U)/R.y)-.3*time, atan(U.y,U.x) ),
							
						s = .5+.5*cos( r * p );  // log-polar grid
						O.x = smoothstep(3.,0., (1.-max(s.x,s.y)) / length(fwidth(vec3(p.x,cos(p.y),sin(p.y)))));
						
						s = .5+.5*cos( r * p * mat2(1,-1,1,1) );
						O.y = smoothstep(3.,0., (1.-max(s.x,s.y)) / length(fwidth(vec3(p.x,cos(p.y),sin(p.y)))));
						return vec4(O, 1.);
					}

					void main_Shader1()
					{
						color_Shader1 = frag_color_Shader1;
						color_Shader1 += mainImage_Shader1(color_Shader1.xyz);
					}
                '''
