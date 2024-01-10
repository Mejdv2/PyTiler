from vbo import VBO
from shader_program import ShaderProgram


class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        # cube vao
        self.vaos['cube'] = self.get_vao(
            program=self.program.programs['default'],
            vbo = self.vbo.vbos['cube'])
        
        
        # background vao
        self.vaos['background'] = self.get_vao(
            program=self.program.programs['background'],
            vbo=self.vbo.vbos['cube'])
        
        
        # screen resizer vao
        self.vaos['screener'] = self.get_vao(
            program=self.program.programs['resizer'],
            vbo=self.vbo.vbos['cube'])
        

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)])
        return vao
    
    def get_ins_vao(self, program, vbo, ibo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs),
                                              (ibo.vbo, ibo.format, *ibo.attribs)])
        return vao


    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()