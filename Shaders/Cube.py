from ShaderInterface import ShaderInterface

class Cube(ShaderInterface):
    name = "Cube"

    def params(self):
        return {'resolutionX_Cube' : 1, 'resolutionY_Cube' : 1, 'rate_Cube' : 1, 'strength_Cube' : 1}
        
    def fragShader(self):
        return  '''
                    #ifdef GL_ES
                    precision mediump float;
                    #endif
                    uniform float resolutionX_Cube;
                    uniform float resolutionY_Cube;
                    uniform float rate_Cube;
                    uniform float strength_Cube;
                    vec4 frag_color_Cube;
                    vec4 color_Cube;
                    vec3 l=normalize(vec3(1,1,0.5));
                    vec3 l2=normalize(vec3(-8,-1,-0.3));

                const vec2 resolutionX_Cube_Range = vec2(screenWidth/4, screenWidth);
                const vec2 resolutionY_Cube_Range = vec2(screenHeight/4, screenHeight); 
                const vec2 strength_Cube_Range = vec2(0, 1);
                vec2 resolution_Cube = vec2(scale(resolutionX_Cube, resolutionX_Cube_Range), scale(resolutionY_Cube, resolutionY_Cube_Range));

                float strength_Cube_Scaled = scale(strength_Cube, strength_Cube_Range);

                    float ball(vec3 p){ 
                        return length(p)-0.79;
                    }
                    float maxx(vec3 p){
                        return max(p.x,max(p.y,p.z));
                    }

                    float c2(vec3 p){
                        vec3 d = abs(p) - 0.6;//vec3(0.2,0.2,0.2);
                        return length(max(d,0.0)) + min(max(d.x,max(d.y,d.z)),0.0);
                        }

                    float cube(vec3 p){
                        return abs(c2(p))-0.02;
                    }
                    float f(vec3 p){
                        return max(cube(p), -ball(p));
                    }


                    // camera rotation : pitch, yaw
                    mat3 rotationXY( vec2 angle ) {
                        vec2 c = cos( angle );
                        vec2 s = sin( angle );
                        
                        return mat3(
                            c.y      ,  0.0, -s.y,
                            s.y * s.x,  c.x,  c.y * s.x,
                            s.y * c.x, -s.x,  c.y * c.x
                        );
                    }
                    void main_Cube(){
                        vec2 p=(gl_FragCoord.xy*2.-resolution_Cube.xy)/min( resolution_Cube.x,resolution_Cube.y);
                        vec3 g=vec3(0,0,18);//eye pos
                        vec3 eye=vec3(p.x,p.y,7);//eye target plane
                        float angl=time*rate_Cube;
                        mat3 v=rotationXY(vec2(time*rate_Cube*0.6,time*rate_Cube*0.6));
                        vec3 e=vec3(0);//color
                        vec3 r=normalize( vec3(eye-g));//eye direction
                        r = v * r;
                        g = v * g;
                        vec3 c=g;
                        float s=1.;
                        float d=0.;
                        float isobj=0.0;
                        
                        vec3 c1;
                        vec3 c2;
                        vec3 c3;
                        float c1g,c2g,c3g;
                        
                        for(int i=0;i<30;i++){
                            d=f(c);
                            
                            if(d<.001){ 
                                break;
                            }
                            if(d<0.)d/=2.;
                            c+=r*d;
                        }
                        if(d<0.5) isobj=1.0;
                        //isobj=1.0-min(min(min(min(abs(d),abs(c1g)),abs(c2g)),abs(c3g)));
                        c1g=1.0/abs(c1g);
                        c2g=1.0/abs(c2g);
                        c3g=1.0/abs(c3g);
                        float cg=1.0/abs(d);
                        //isobj=max(1.0,d*(-100.));
                        //c=(c*cg+c1*c1g+c2*c2g+c3*c3g)/(cg+c1g+c2g+c3g);
                        float fc=f(c);
                        vec3 n=(vec3(   fc-f(vec3(c.x-d,c.y,c.z)),
                                    fc-f(vec3(c.x,c.y-d,c.z)),
                                    fc-f(vec3(c.x,c.y,c.z-d))
                                             ));
                        n=normalize(abs(n));
                        //n = v * n;
                        //n2 = v * n2;

                        float f=(dot(n,l));
                        //f+=dot(n,l2);
                        e=n*isobj*0.5;
                            
                    color_Cube = vec4(e, 1.0) * strength_Cube_Scaled;
                    color_Cube += frag_color_Cube;
                    }   

                '''
