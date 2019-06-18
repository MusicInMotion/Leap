from ShaderInterface import ShaderInterface

class Kaleidoscope(ShaderInterface):
	# source: http://glslsandbox.com/e#53913.2
    name = "Kaleidoscope"

    def params(self):
        return {"resolutionX_Kaleidoscope" : 1, "resolutionY_Kaleidoscope" : 1}
        
    def fragShader(self):
        return  '''
                    vec4 frag_color_Kaleidoscope;
					vec4 color_Kaleidoscope;
					const vec2 resolutionX_Kaleidoscope_Range = vec2(screenWidth/4, screenWidth);
                    const vec2 resolutionY_Kaleidoscope_Range = vec2(screenHeight/4, screenHeight);

					uniform float resolutionX_Kaleidoscope;
					uniform float resolutionY_Kaleidoscope;
					vec2 resolution_Kaleidoscope = vec2(scale(resolutionX_Kaleidoscope, resolutionX_Kaleidoscope_Range), scale(resolutionY_Kaleidoscope, resolutionY_Kaleidoscope_Range));

					mat2 rotate_Kaleidoscope(float a) {
						
						float c = cos(a);
						float s = sin(a);
						
						return mat2(c, s, -s, c);
					}

					vec3 camera_Kaleidoscope(vec2 uv, vec3 ro, vec3 cl, vec3 cu) {
						
						vec3 cw = normalize(cl - ro);
						vec3 cr = normalize(cross(cu, cw));
						cu = normalize(cross(cw, cr));
						
						return normalize(uv.x * cr + uv.y * cu + cw);
						
					}

					void main_Kaleidoscope() {
						vec2 uv = (2. * gl_FragCoord.xy - resolution_Kaleidoscope) / resolution_Kaleidoscope.y;
						
						vec3 col = vec3(0);
						
						vec3 ro = vec3(0.0, 0.0, -1);
						vec3 rd = camera_Kaleidoscope(uv, ro, vec3(0, sin(time / 40000.), 0), vec3(0.0, 1.0, 0.0));
						vec3 p = vec3(0);
						
						float d = 0.0;
						float t = 0.0;
						for (int i = 0; i < 100; i++) {
							p = ro + rd * t;
					  
							d = 10. -(length(p) - 1.);
							if (d < 0.001) break;
							t += 0.5 * d;
						}
						
						if (d < 0.001) {								
							float k = time / 100.;
							for (int i = 0; i < 3; i++) {
								k += .5;
								float s = .5;
								for (int i = 0; i < 16; i++) {
									p = abs(p) - s;
									p.xz *= rotate_Kaleidoscope(k);
									p.xy *= rotate_Kaleidoscope(k);
									p.yz *= rotate_Kaleidoscope(k);
									s *= .95;
								}
								col[i] = .1 / abs(sin(length(p.xz * 2.) * 4.)) * .33;
								col[i] += .1 / abs(sin(length(p.xy * 2.) * 4.)) * .33;
								col[i] += .1 / abs(sin(length(p.yz * 2.) * 4.)) * .33;
								}
						}		
						color_Kaleidoscope = vec4(col, 1.);
						color_Kaleidoscope += frag_color_Kaleidoscope;
					}
                '''
