from ShaderInterface import ShaderInterface

class Shader8(ShaderInterface):
	# source: http://glslsandbox.com/e#52847.0
    name = "Shader8"

    def params(self):
        return {"resolutionX_Shader8" : 1, "resolutionY_Shader8" : 1}
        
    def fragShader(self):
        return  '''
					vec4 frag_color_Shader8;
					vec4 color_Shader8;
					const vec2 resolutionX_Shader8_Range = vec2(screenWidth/4, screenWidth);
                    const vec2 resolutionY_Shader8_Range = vec2(screenHeight/4, screenHeight);

					uniform float resolutionX_Shader8;
					uniform float resolutionY_Shader8;
					vec2 resolution_Shader8 = vec2(scale(resolutionX_Shader8, resolutionX_Shader8_Range), scale(resolutionY_Shader8, resolutionY_Shader8_Range));
					
					mat2 rot_Shader8(float a) {
						float s = sin(a), c = cos(a);
						return mat2(c, s, -s, c);
					}

					vec2 kaleidoscope_Shader8(vec2 p, float m) {
						float l = 1. / m;
						float t = l * .2887;
						float f = 1.;
						float a = 0.;
						p.y += t * 2.;
						vec2 c = vec2(0., t * 2.);
						vec2 q = p * m;
						q.y *= 1.1547;
						q.x += .5 * q.y;
						vec2 r = fract(q);
						vec2 s = floor(q);
						p.y -= s.y * .866 * l;
						p.x -= (s.x - q.y * .5) * l + p.y * .577;
						a += mod(s.y, 3.) * 2.;
						a += mod(s.x, 3.) * 2.;
						if (r.x > r.y) {
							f *= -1.;
							a += 1.;
							p += vec2(-l * .5, t);
						}
						p.x *= f;
						p -= c;
						p *= rot_Shader8(a * 1.0472);
						p += c;
						p.y -= t * 2.;
						return p;
					}

					vec3 hsv2rgb_Shader8(vec3 c) {
						vec3 rgb = clamp( abs(mod(c.x*6.0+vec3(0.0,4.0,2.0),6.0)-3.0)-1.0, 0.0, 1.0 );
						rgb = rgb*rgb*(3.0-2.0*rgb);
						return c.z * mix( vec3(1.0), rgb, c.y);
					}

					vec2 brickTile_Shader8(vec2 _st, float _zoom){
						_st *= _zoom;

						// Here is where the offset is happening
						if (mod(time, 4.) > 2.0) {
							if (mod(time, 2.) > 1.0)
							_st.x += step(1., mod(_st.y,2.0)) * time;
							else
							_st.y += step(1., mod(_st.x,2.0)) * time;
						}
						else {
							if (mod(time, 2.) > 1.0)
							_st.x -= step(1., mod(_st.y,2.0)) * time;
							else
							_st.y -= step(1., mod(_st.x,2.0)) * time;
						}

						return fract(_st);
					}

					float box_Shader8(vec2 _st, vec2 _size){
						_size = vec2(0.5)-_size*0.5;
						vec2 uv = smoothstep(_size,_size+vec2(1e-4),_st);
						uv *= smoothstep(_size,_size+vec2(1e-4),vec2(1.0)-_st);
						return uv.x*uv.y;
					}

					void main_Shader8(void){
						vec2 uv = (frag_color_Shader8.xy/resolution_Shader8.y) - 0.5 * vec2(resolution_Shader8.x/resolution_Shader8.y, 1.0);
						uv *= rot_Shader8(time*0.05);
						uv = kaleidoscope_Shader8(uv, 3.+sin(time*0.06));
						uv *= rot_Shader8(time*0.03);
						uv.x += cos(time*0.03);
						uv = kaleidoscope_Shader8(uv, 6.+cos(time*0.04));
						uv *= rot_Shader8(time*0.02);
						uv = kaleidoscope_Shader8(uv, 12.+sin(time*0.04));
						uv *= rot_Shader8(time*0.04);
						uv.x += sin(time*0.01);
						vec3 color;

						uv = brickTile_Shader8(uv,6.0);

						color = vec3(box_Shader8(uv,vec2(0.9)));

						// Uncomment to see the space coordinates
						color = hsv2rgb_Shader8(reflect(vec3(uv.xy, uv.y/uv.x), 1.-color));

					    color_Shader8 = vec4(color,1.0);
						color_Shader8 += frag_color_Shader8;
					}
                '''
