from ShaderInterface import ShaderInterface

class Empty(ShaderInterface):
    name = "Empty"

    def params(self):
        return {}
        
    def fragShader(self):
        return  '''
                    vec4 frag_color_Empty;
                    vec4 color_Empty;

                    void main_Empty( ) {
                        color_Empty = vec4(0, 0, 0, sin(time)*0.001);
					}
                '''