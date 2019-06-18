from ShaderInterface import ShaderInterface

class Shader7(ShaderInterface):
	# source: http://glslsandbox.com/e#53878.0
    name = "Shader7"

    def params(self):
        return {"resolutionX_Shader7" : 1, "resolutionY_Shader7" : 1}
        
    def fragShader(self): 
        return  '''
					vec4 frag_color_Shader7;
					vec4 color_Shader7;
					const vec2 resolutionX_Shader7_Range = vec2(screenWidth/4, screenWidth);
                    const vec2 resolutionY_Shader7_Range = vec2(screenHeight/4, screenHeight);

					uniform float resolutionX_Shader7;
					uniform float resolutionY_Shader7;
					vec2 resolution_Shader7 = vec2(scale(resolutionX_Shader7, resolutionX_Shader7_Range), scale(resolutionY_Shader7, resolutionY_Shader7_Range));

					// shadertoy globals
					#define iTime time
					#define iResolution resolution_Shader7
					const vec4 iMouse = vec4(0.0);

					// --------[ Original ShaderToy begins here ]---------- //
					#define R iResolution

					mat2 rot_Shader7(float a)
					{
						float s = sin(a);
						float c = cos(a);
						return mat2(s, c, -c, s);
					}

					mat3 camera_Shader7(vec3 ro, vec3 ta)
					{
						const vec3 up = vec3(0, 1, 0);
						vec3 cw = normalize(ta - ro);
						vec3 cu = normalize(cross(cw, up));
						vec3 cv = normalize(cross(cu, cw));
						return mat3(cu, cv, cw);
					}

					float map_Shader7_Shader7(vec3 p)
					{
						mat2 rm = rot_Shader7(-iTime / 3.0 + length(p));
						p.xy *= rm;
						p.zy *= rm;
						
						vec3 q = abs(p) - iTime * 0.1;
						q = abs(q - floor(q + 0.5));
						
						float d1 = min(length(q.xy), length(q.yz));
						float d2 = min(d1, length(q.xz));
						return min(d1, d2);
					}

					vec4 mainImage_Shader7( vec2 fragCoord )
					{
						vec2 uv = (fragCoord * 2.0 - R.xy) / R.y;

						vec3 ro = vec3(iMouse.xy / R.xy, 5);
						vec3 ta = vec3(0, 0, 0);
						
						vec3 ray = camera_Shader7(ro, ta) * normalize(vec3(uv, 1.5));
						
						float d = 0.0;
						
						float dist = 0.0;
						for (int i = 0; i < 200; i++)
						{
							dist = map_Shader7_Shader7(ro + ray * d) / 2.0;
									
							d += dist;
						}
						
						
						vec3 col = vec3(d * 0.03);   

						d *= 0.03;
						return vec4(1.0 - d, exp(-d), 2.0 * exp(-d / 4.0 - 1.0), 1.0);
					}
					// --------[ Original ShaderToy ends here ]---------- //

					void main_Shader7(void)
					{
						color_Shader7 = mainImage_Shader7(frag_color_Shader7.xy);
					}
                '''
