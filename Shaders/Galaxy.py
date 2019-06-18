from ShaderInterface import ShaderInterface

class Galaxy(ShaderInterface):
    name = "Galaxy"

    def params(self):
        return {'resolutionX_Galaxy' : 1, 'resolutionY_Galaxy' : 1, 'posX_Galaxy' : 0, 'posY_Galaxy' : 0, 'freq1_Galaxy' : 1, 'freq2_Galaxy' : 1, 'freq3_Galaxy' : 1, 'strength_Galaxy' : 1}
        
    def fragShader(self):
        return  '''
                    const vec2 resolutionX_Galaxy_Range = vec2(screenWidth/4, screenWidth);
                    const vec2 resolutionY_Galaxy_Range = vec2(screenHeight/4, screenHeight);
                    const vec2 posX_Galaxy_Range = vec2(0, 1000);
                    const vec2 posY_Galaxy_Range = vec2(0, 1000);
	       			uniform float posX_Galaxy;
	       			uniform float posY_Galaxy;
	       			uniform float resolutionX_Galaxy;
	       			uniform float resolutionY_Galaxy;
                                vec2 pos_Galaxy = vec2(scale(posX_Galaxy, posX_Galaxy_Range), scale(posY_Galaxy, posY_Galaxy_Range));
					vec4 frag_color_Galaxy;
					vec4 color_Galaxy;
					uniform float resolution_x_Galaxy;
					uniform float resolution_y_Galaxy;
					vec2 resolution_Galaxy = vec2(scale(resolutionX_Galaxy, resolutionX_Galaxy_Range), scale(resolutionY_Galaxy, resolutionY_Galaxy_Range));
					uniform float freq1_Galaxy;
					uniform float freq2_Galaxy;
					uniform float freq3_Galaxy;
                    uniform float strength_Galaxy;
					float mod289_Galaxy(float x){return x - floor(x * (1.0 / 289.0)) * 289.0;}
					vec4 mod289_Galaxy(vec4 x){return x - floor(x * (1.0 / 289.0)) * 289.0;}
					vec4 perm_Galaxy(vec4 x){return mod289_Galaxy(((x * 34.0) + 1.0) * x);}

					float noise_Galaxy(vec3 p){
						vec3 a = floor(p);
						vec3 d = p - a;
						d = d * d * (3.0 - 2.0 * d);

						vec4 b = a.xxyy + vec4(0.0, 1.0, 0.0, 1.0);
						vec4 k1 = perm_Galaxy(b.xyxy);
						vec4 k2 = perm_Galaxy(k1.xyxy + b.zzww);

						vec4 c = k2 + a.zzzz;
						vec4 k3 = perm_Galaxy(c);
						vec4 k4 = perm_Galaxy(c + 1.0);

						vec4 o1 = fract(k3 * (1.0 / 41.0));
						vec4 o2 = fract(k4 * (1.0 / 41.0));

						vec4 o3 = o2 * d.z + o1 * (1.0 - d.z);
						vec2 o4 = o3.yw * d.x + o3.xz * (1.0 - d.x);

						return o4.y * d.y + o4.x * (1.0 - d.y);
					}
					float field_Galaxy(in vec3 p,float s) {
						float strength = 7. + .03 * log(1.e-6 + fract(sin(time) * 4373.11));
						float accum = s/4.;
						float prev = 0.;
						float tw = 0.;
						for (int i = 0; i < 18; ++i) {
							float mag = dot(p, p);
							p = abs(p) / mag + vec3(-.5, -.4, -1.5);
							float w = exp(-float(i) / 7.);
							accum += w * exp(-strength * pow(abs(mag - prev), 2.2));
							tw += w;
							prev = mag;
						}
						return max(0., 5. * accum / tw - .7);
					}

					// Less iterations for second layer
					float field2_Galaxy(in vec3 p, float s) {
						float strength = 7. + .03 * log(1.e-6 + fract(sin(time) * 4373.11));
						float accum = s/4.;
						float prev = 0.;
						float tw = 0.;
						for (int i = 0; i < 26; ++i) {
							float mag = dot(p, p);
							p = abs(p) / mag + vec3(-.5, -.4, -1.5);
							float w = exp(-float(i) / 7.);
							accum += w * exp(-strength * pow(abs(mag - prev), 2.2));
							tw += w;
							prev = mag;
						}
						return max(0., 5. * accum / tw - .7);
					}

					vec3 nrand3_Galaxy( vec2 co )
					{
						vec3 a = fract( cos( co.x*8.3e-3 + co.y )*vec3(1.3e5, 4.7e5, 2.9e5) );
						vec3 b = fract( sin( co.x*0.3e-3 + co.y )*vec3(8.1e5, 1.0e5, 0.1e5) );
						vec3 c = mix(a, b, 0.5);
						return c;
					}


					void main_Galaxy( ) {
						vec2 uv = 2. * (gl_FragCoord.xy + pos_Galaxy.xy) / resolution_Galaxy.xy - 1.;
						vec2 uvs = uv * resolution_Galaxy.xy / max(resolution_Galaxy.x, resolution_Galaxy.y);
						vec3 p = vec3(uvs / 4., 0) + vec3(1., -1.3, 0.);
						p += .2 * vec3(sin(time / 16.), sin(time / 12.),  sin(time / 128.));
						
						float freqs[4];
						//Sound
						freqs[0] = noise_Galaxy(vec3( 0.01*100.0, 0.25 ,time/10.0) );
						freqs[1] = noise_Galaxy(vec3( 0.07*100.0, 0.25 ,time/10.0) );
						freqs[2] = noise_Galaxy(vec3( 0.15*100.0, 0.25 ,time/10.0) );
						freqs[3] = noise_Galaxy(vec3( 0.30*100.0, 0.25 ,time/10.0) );

						float t = field_Galaxy(p,freqs[2]);
						float v = (1. - exp((abs(uv.x) - 1.) * 6.)) * (1. - exp((abs(uv.y) - 1.) * 6.));
						
						//Second Layer
						vec3 p2 = vec3(uvs / (4.+sin(time*0.11)*0.2+0.2+sin(time*0.15)*0.3+0.4), 1.5) + vec3(2., -1.3, -1.);
						p2 += 0.25 * vec3(sin(time / 16.), sin(time / 12.),  sin(time / 128.));
						float t2 = field2_Galaxy(p2,freqs[3]);
						vec4 c2 = mix(.4, 1., v) * vec4(1.3 * t2 * t2 * t2 ,1.8  * t2 * t2 , t2* freqs[0], t2);
						
						
						//Let's add some stars
						//Thanks to http://glsl.heroku.com/e#6904.0
						vec2 seed = p.xy * 2.0;	
						seed = floor(seed * resolution_Galaxy.x);
						vec3 rnd = nrand3_Galaxy( seed );
						vec4 starcolor_Galaxy = vec4(pow(rnd.y,40.0));
						
						//Second Layer
						vec2 seed2 = p2.xy * 2.0;
						seed2 = floor(seed2 * resolution_Galaxy.x);
						vec3 rnd2 = nrand3_Galaxy( seed2 );
						starcolor_Galaxy += vec4(pow(rnd2.y,40.0));
						
						color_Galaxy = mix(freqs[3]-.3, 1., v) * vec4(1.5*freqs[2] * t * t* t , 1.2*freqs[1] * t * t, freqs[3]*t, 1.0)+c2+starcolor_Galaxy;
						color_Galaxy.x *= freq1_Galaxy;
						color_Galaxy.y *= freq2_Galaxy;
						color_Galaxy.z *= freq3_Galaxy;
						color_Galaxy *= strength_Galaxy * 1.5;
						color_Galaxy += frag_color_Galaxy;
					}
                '''
