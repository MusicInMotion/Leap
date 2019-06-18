from ShaderInterface import ShaderInterface

class FeverDream(ShaderInterface):
    name = "FeverDream"

    def params(self):
        return {'resolutionX_FeverDream' : 1, 'resolutionY_FeverDream' : 1, 'speed_FeverDream' : 0, 'zoom_FeverDream' : 3.9, 'fieldStrength_FeverDream' : 1, 'cloud_FeverDream' : 0.1, 'transverseSpeed_FeverDream' : 1.1, 'strength_FeverDream' : 1}
        
    def fragShader(self):
        return  '''
                    #ifdef GL_ES
                    precision highp float;
                    #endif
                    vec4 color_FeverDream;
                    vec4 frag_color_FeverDream;
      
                    const vec2 strength_FeverDream_Range = vec2(0, 1);
                    const vec2 resolutionX_FeverDream_Range = vec2(screenWidth/4, screenWidth);
                    const vec2 resolutionY_FeverDream_Range = vec2(screenHeight/4, screenHeight);
                    uniform float resolutionX_FeverDream;
                    uniform float resolutionY_FeverDream;
                    vec2 resolution_FeverDream = vec2(scale(resolutionX_FeverDream, resolutionX_FeverDream_Range), scale(resolutionY_FeverDream, resolutionY_FeverDream_Range));

                    uniform float speed_FeverDream;
                    uniform float fieldStrength_FeverDream;
                    uniform float cloud_FeverDream;
                    uniform float strength_FeverDream;

                    float strength_FeverDream_Scaled = scale(strength_FeverDream, strength_FeverDream_Range);

                    #define iterations 4
                    #define formuparam2 0.89
                     
                    #define volsteps 10
                    #define stepsize 0.190
                     
                    uniform float zoom_FeverDream;
                    #define tile   0.450
                    #define base_speed  0.010
                     
                    #define brightness 4.4
                    #define darkmatter 0.400
                    #define distfading 0.560
                    #define saturation 0.400


                    uniform float transverseSpeed_FeverDream;
                    #define cloud 0.1
                     
                    float triangle_FeverDream(float x, float a)
                    {
                     
                     
                    float output2 = 2.0*abs(  2.0*  ( (x/a) - floor( (x/a) + 0.5) ) ) - 1.0;
                    return output2;
                    }
                     

                    float field_FeverDream(in vec3 p) {
                        
                        float strength = (7. + .03 * log(1.e-6 + fract(sin(time) * 4373.11))) * fieldStrength_FeverDream;
                        float accum = 0.;
                        float prev = 0.;
                        float tw = 0.;
                        

                        for (int i = 0; i < 6; ++i) {
                            float mag = dot(p, p);
                            p = abs(p) / mag + vec3(-.5, -.8 + 0.1*sin(time*0.2 + 2.0), -1.1+0.3*cos(time*0.15));
                            float w = exp(-float(i) / 7.);
                            accum += w * exp(-strength * pow(abs(mag - prev), 2.3));
                            tw += w;
                            prev = mag;
                        }
                        return max(0., 5. * accum / tw - .7);
                    }



                    void main_FeverDream()
                    {
                       
                            vec2 uv2 = 2. * gl_FragCoord.xy / resolution_FeverDream.xy - 1.;
                        vec2 uvs = uv2 * resolution_FeverDream.xy / max(resolution_FeverDream.x, resolution_FeverDream.y);
                        

                        
                        float time2 = time*1.9;
                                   
                            float speed = base_speed;
                            speed = 0.005 * (cos(time2*0.02 + 3.1415926/4.0) + speed_FeverDream);
                              
                        //speed = 0.0;

                        
                            float formuparam = formuparam2;

                        
                        
                        //get coords and direction

                        vec2 uv = uvs;
                        
                        
                                   
                        //mouse rotation
                        float a_xz = 0.9;
                        float a_yz = -.6;
                        float a_xy = 0.9 + time*0.04;
                        
                        
                        mat2 rot_xz = mat2(cos(a_xz),sin(a_xz),-sin(a_xz),cos(a_xz));
                        
                        mat2 rot_yz = mat2(cos(a_yz),sin(a_yz),-sin(a_yz),cos(a_yz));
                            
                        mat2 rot_xy = mat2(cos(a_xy),sin(a_xy),-sin(a_xy),cos(a_xy));
                        

                        float v2 =1.0;
                        
                        vec3 dir=vec3(uv*zoom_FeverDream,1.);
                     
                        vec3 from=vec3(0.0, 0.0,0.0);
                     
                                                   
                            from.x -= .5*(-0.5);
                            from.y -= .5*(-0.5);
                                   
                                   
                        vec3 forward = vec3(0.,1.,1.);
                                   
                        
                        from.x += transverseSpeed_FeverDream*(1.0)*cos(0.01*time) + 0.001*time;
                        from.y += transverseSpeed_FeverDream*(1.0)*sin(0.01*time) + 0.001*time;
                        from.z += 0.003*time;
                        
                        
                        dir.xy*=rot_xy;
                        forward.xy *= rot_xy;

                        dir.xz*=rot_xz;
                        forward.xz *= rot_xz;
                            
                        
                        dir.yz*= rot_yz;
                        forward.yz *= rot_yz;
                         

                        
                        from.xy*=-rot_xy;
                        from.xz*=rot_xz;
                        from.yz*= rot_yz;
                         
                        
                        //zoom_FeverDream
                        float zooom = (time2-3311.)*speed;
                        from += forward* zooom;
                        float sampleShift = mod( zooom, stepsize );
                         
                        float zoffset = -sampleShift;
                        sampleShift /= stepsize; // make from 0 to 1


                        
                        //volumetric rendering
                        float s=0.24;
                        float s3 = s + stepsize/2.0;
                        vec3 v=vec3(0.);
                        float t3 = 0.0;
                        
                        
                        vec3 backCol2 = vec3(0.);
                        for (int r=0; r<volsteps; r++) {
                            vec3 p2=from+(s+zoffset)*dir;// + vec3(0.,0.,zoffset);
                            vec3 p3=(from+(s3+zoffset)*dir )* (1.9/zoom_FeverDream);// + vec3(0.,0.,zoffset);
                            
                            p2 = abs(vec3(tile)-mod(p2,vec3(tile*2.))); // tiling fold
                            p3 = abs(vec3(tile)-mod(p3,vec3(tile*2.))); // tiling fold
                            
                            #ifdef cloud
                            t3 = field_FeverDream(p3);
                            #endif
                            
                            float pa,a=pa=0.;
                            for (int i=0; i<iterations; i++) {
                                p2=abs(p2)/dot(p2,p2)-formuparam; // the magic formula
                                //p2=abs(p)/max(dot(p,p),0.05)-formuparam; // another interesting way to reduce noise
                                float D = abs(length(p2)-pa); // absolute sum of average change
                                
                                if (i > 2)
                                {
                                a += i > 7 ? min( 12., D) : D;
                                }
                                    pa=length(p2);
                            }
                            
                            
                            //float dm=max(0.,darkmatter-a*a*.001); //dark matter
                            a*=a*a; // add contrast
                            //if (r>3) fade*=1.-dm; // dark matter, don't render near
                            // brightens stuff up a bit
                            float s1 = s+zoffset;
                            // need closed form expression for this, now that we shift samples
                            float fade = pow(distfading,max(0.,float(r)-sampleShift));
                            
                            
                            //t3 += fade;
                            
                            v+=fade;
                                    //backCol2 -= fade;

                            // fade out samples as they approach the camera
                            if( r == 0 )
                                fade *= (1. - (sampleShift));
                            // fade in samples as they approach from the distance
                            if( r == volsteps-1 )
                                fade *= sampleShift;
                            v+=vec3(s1,s1*s1,s1*s1*s1*s1)*a*brightness*fade; // coloring based on distance
                            
                            backCol2 += mix(.9, 2., v2) * vec3(0.20 * t3 * t3 * t3, 0.4 * t3 * t3, t3 * 0.7) * fade;

                            
                            s+=stepsize;
                            s3 += stepsize;
                            
                            
                            
                            }
                                   
                        v=mix(vec3(length(v)),v,saturation); //color adjust
                         
                        
                        

                        vec4 forCol2 = vec4(v*.01,1.);
                        
                        #ifdef cloud
                        backCol2 *= cloud_FeverDream;
                        #endif
                        
                        backCol2.r *= 0.60;
                        backCol2.g *= 1.05;
                        backCol2.b *= 0.00;
                        

                        
                    //  backCol2.b = 0.5*mix(backCol2.b, backCol2.g, 0.2);
                    //  backCol2.g = 0.0;
                    //
                    //  backCol2.bg = mix(backCol2.gb, backCol2.bg, 0.5*(cos(time*0.01) + 1.0));
                        
                        color_FeverDream = vec4(backCol2, 1.0) * strength_FeverDream_Scaled;
                        color_FeverDream += frag_color_FeverDream;
                    }
                '''
