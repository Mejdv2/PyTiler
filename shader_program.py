

class ShaderProgram:
    def __init__(self, ctx):
        self.ctx = ctx
        self.programs = {}
        self.programs['default']    = self.get_program('default')
        self.programs['tilemap']    = self.get_program('tilemap')
        self.programs['background'] = self.get_program('background')
        self.programs['resizer']    = self.get_program('resizer')

    def get_program(self, shader_program_name):
        with open(f'shaders/{shader_program_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_program_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    def destroy(self):
        [program.release() for program in self.programs.values()]
