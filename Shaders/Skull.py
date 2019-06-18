from ShaderInterface import ShaderInterface

class Skull(ShaderInterface):
    name = "Skull"
    
    def params(self):
        return {'resolutionX_Skull' : 1, 'resolutionY_Skull' : 1, 'chinWidth_Skull' : 1, 'faceStrength_Skull' : 1,
                'nostril_Skull' : 0.5, 'rotateRate_Skull' : 0.5, 'bloom_Skull' : 0.5, 'zoomRate_Skull' : .5}
        
    def fragShader(self):
        return '''
                    uniform float resolutionX_Skull;
                    uniform float resolutionY_Skull;
                    uniform float chinWidth_Skull;
                    uniform float faceStrength_Skull;
                    uniform float nostril_Skull;
                    uniform float rotateRate_Skull;
                    uniform float bloom_Skull;
                    uniform float zoomRate_Skull;
                    const vec2 resolutionX_Skull_Range = vec2(screenWidth/4, screenWidth);
                    const vec2 resolutionY_Skull_Range = vec2(screenHeight/4, screenHeight);

                    const vec2 chinWidth_Skull_Range = vec2(1, 15);
                    float chinWidth = scale(chinWidth_Skull, chinWidth_Skull_Range);

                    const vec2 faceStrength_Skull_Range = vec2(1, 15);
                    float faceStrength = scale(faceStrength_Skull, faceStrength_Skull_Range);

                    const vec2 nostril_Skull_Range = vec2(0.01, 0.1);
                    float nostril = scale(nostril_Skull, nostril_Skull_Range);                    

                    const vec2 bloom_Skull_Range = vec2(0, 1);
                    float bloom_Skull_Scaled = scale(bloom_Skull, bloom_Skull_Range);
                    
                    const vec2 rotateRate_Skull_Range = vec2(0, 10);
                    float rotateRate_Skull_Scaled = scale(rotateRate_Skull, rotateRate_Skull_Range);

                    const vec2 zoomRate_Skull_Range = vec2(0, 5);
                    float zoomRate_Skull_Scaled = scale(zoomRate_Skull, zoomRate_Skull_Range);

                    

                    
                    float resolutionX_Skull_Scaled = scale(resolutionX_Skull, resolutionX_Skull_Range);
                    float resolutionY_Skull_Scaled = scale(resolutionY_Skull, resolutionY_Skull_Range);
                    
                    vec2 resolution = vec2(resolutionX_Skull_Scaled, resolutionY_Skull_Scaled);
                    
                    vec4 frag_color_Skull;
                    vec4 color_Skull;

                    mat2 rotate_Skull(float a) {
                        float c = cos(a);
                        float s = sin(a);
                        return mat2(c, s, -s, c);
                    }

                    // exponential smooth min (k = 32);
                    float smin( float a, float b, float k )
                    {
                        float res = exp2( -k*a ) + exp2( -k*b );
                        return -log2( res )/k;
                    }

                    float smax(float a, float b, float k) {
                      return -smin(-a, -b, k);
                    }


                    float circle(vec2 uv, float r) {
                        return length(uv) - r;
                    }

                    float face_Skull(vec2 uv) {

                        float col = 0.;
                            float d = 1e9;
                        vec2 p = uv;
                        
                        // face_Skull
                        float r = .5;
                        d = smin(d, circle(p, r), chinWidth);
                        
                        // chin
                        p = uv;
                        p.y += .61 + .005 * sin(time * 5. + abs(p.x * 2.));
                        r = .2;
                        d = smin(d, circle(p, r), 15.);
                        
                        // eyes
                        p = uv;
                        p.x *= .7;
                        p.x = abs(p.x) - .14;
                        p.y += .12;
                        p.x = p.x - p.y * .2;
                        r = .1;
                        d = smax(d, -circle(p, r), faceStrength);
                            
                        // nostrils
                        p = uv;
                        p.y += .2;
                        p.x *= .7;
                        p.x = abs(p.x) - .02;
                        p.y += .12;
                        p.x = p.x - p.y * .2;
                        r = nostril;
                        d = smax(d, -circle(p, r), 32.);
                        
                        // mouth
                        p = uv;
                        
                        p.y += .5;
                        p.x *= .1;
                        p.x = abs(p.x);
                        p.x += -p.y * .1;
                        d = smax(d, -circle(p, r), 128.);
                        
                        d = smax(d, -circle(p, r), 128.);
                        
                        
                        
                        col += d;
                        return col;
                        
                    }

                    float faces_Skull(vec2 uv) {

                        uv *= rotate_Skull(time / 10.);
                        float col = 0.;
                            
                        
                        float a = atan(uv.x, uv.y) + 3.14/ 2.;
                        float m = 6.28 / 12.;
                        a = mod(a, m) - m / 2.;
                        float l = length(uv);
                        vec2 p = zoomRate_Skull_Scaled * l * vec2(cos(a), sin(a));
                        p.x -= 2.;
                            
                        
                        p *= rotate_Skull(-3.14 / 2.);
                        col = face_Skull(p);
                        
                        return col;
                    }

                    void main_Skull() {
                        vec2 uv = (2. * gl_FragCoord.xy - resolution) / resolution.y;
                        vec3 col = vec3(0.);
                        vec2 st = uv;

                        uv *= 20.;
                        float d = 0.;
                        uv *= rotate_Skull(rotateRate_Skull_Scaled * time / 10.);
                        for (float i = 0.; i < 1.; i += .1) {
                            float t = fract(time / 10. + i);
                            float s = smoothstep(.8, 0., t);
                            float fc =faces_Skull(uv * s);
                            d = smoothstep(bloom_Skull_Scaled + .05 * cos(time), .0, fc);
                            col += d;
                            col += abs(.09 /fc);
                            col *= .5 + .5 * cos(time + d * 5. + vec3(23, 21, 0));
                        }
                        col *= smoothstep(.07, .7, length(st));

                        color_Skull = vec4(col, 1.);
                        color_Skull += frag_color_Skull;
                    }
                '''