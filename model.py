import moderngl as mgl
import numpy as np
import pygame as pg
import json

import glm, sys, time


class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=(0, 0, 0), roll=0, scale=(1, 1)):
        self.app = app
        self.pos = pos
        self.roll = roll
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        m_model = glm.mat4()
        # translate
        m_model = glm.translate(m_model, self.pos)
        # rotate
        m_model = glm.rotate(m_model, glm.radians(self.roll), glm.vec3(0, 0, 1))
        # scale
        m_model = glm.scale(m_model, glm.vec3(self.scale, 0))
        return m_model

    def render(self):
        self.update()
        self.m_model = self.get_model_matrix()
        self.vao.render()


class Cube(BaseModel):
    def __init__(self, app, vao_name='cube', tex_id=0, pos=(0, 0, 0), rot=0, scale=(1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        self.texture.use()
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)


class EventManager():
    def __init__(self, app) -> None:
        self.app = app

    def handle_events(self, events):
        for event in events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.app.mesh.destroy()
                pg.quit()
                sys.exit()

            if event.type == pg.WINDOWSIZECHANGED:
                self.app.WIN_SIZE = glm.ivec2(event.x, event.y)
                self.app.ctx.viewport = (0, 0, event.x, event.y)


        
class Player(BaseModel):
    def __init__(self, app, vao_name='cube', tex_id='player', pos=glm.vec3(0, 0, 0), rot=0, scale=glm.vec2(14, 18)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()
        self.force = glm.vec2(0)

    def update(self):
        self.texture.use()
        self.program['u_texture_0'] = 0
        tss = time.time() - self.app.start_time
        anim_fps = 10
        self.program['frame'].write(glm.int8( round((tss * anim_fps) % 22) ))
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

        self.force += glm.vec2(0, -150) * self.app.delta_time

        self.pos   += glm.vec3(self.force, 0) * self.app.delta_time
        self.roll  += self.app.delta_time * 90

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.texture.use()
        self.program['u_texture_0'] = 0
        self.program['frame'].write(glm.float32(0))
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)


class Cat(BaseModel):
    def __init__(self, app, vao_name='cat', tex_id='cat',
                 pos=(0, 0, 0), rot=0, scale=(1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        self.texture.use()
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)




class ProcessRender():
    def __init__(self, app, vao_name='screener'):
        self.app = app
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program

    def render(self, output_texture):

        self.program['u_texture_0'] = 0
        output_texture.use(location=0)
        self.program['gsf'].write(self.maintain_aspect_ratio(self.app.WIN_SIZE))

        self.vao.render()


    def maintain_aspect_ratio(self, windu):
        current_ratio = windu.x / windu.y

        if current_ratio > 1.333:
            # Scale based on height to fit the 4:3 aspect ratio
            scaling_vector = glm.vec2(1.0, 1.333 / current_ratio)
        else:
            # Scale based on width to fit the 4:3 aspect ratio
            scaling_vector = glm.vec2(current_ratio / 1.333, 1.0)

        return scaling_vector
    


class Background():
    def __init__(self, app, vao_name='background', tex_id="background"):
        self.app = app
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program

        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0

    def render(self):
        self.texture.use(location=0)
        self.vao.render()


        
        

class NBaseVBO:
    def __init__(self, ctx, vbo):
        self.ctx = ctx
        self.vbo = vbo
        self.format: str = "3f /i"
        self.attribs: list = ["position"]

    def destroy(self):
        self.vbo.release()
        


class Tilemap:
    def __init__(self, app, tile_size=16):
        self.app = app
        self.ctx:mgl.Context = app.ctx
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        
        self.size = 1000

        self.block_arr = np.zeros((self.size*self.size, 3), dtype='f4')


        for i in range(self.size):
            for j in range(self.size):
                self.tilemap[f"{j-self.size/2};{i-self.size/2}"] = {'type': 'grass', 'varient': 1, 'position': (j-self.size/2, i-self.size/2)}

                self.block_arr[j+i*self.size] = [j-self.size/2, i-self.size/2, 0]

                #1,000,000 Tiles

            
        self.block_arr.reshape((self.size*self.size, 3))
        print(str(self.block_arr))
        self.buffer = self.ctx.buffer(self.block_arr)

        self.vao = app.mesh.vao.get_ins_vao(app.mesh.vao.program.programs['tilemap'], 
                                            app.mesh.vao.vbo.vbos['cube'], 
                                            NBaseVBO(self.ctx, self.buffer))
        
        app.mesh.vao.vaos["tiles"] = self.vao
        self.tex = app.mesh.texture.textures["texArr"]
        
        
        self.pos = glm.vec3(0)
        self.roll = 0
        self.scale = glm.vec2(16)

        self.m_model = self.get_model_matrix()
        self.program = self.vao.program
        self.camera = self.app.camera
        

    def update(self): 
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        
        self.program['Tiler'] = 0
        self.tex.use(location=0)

        

    def get_model_matrix(self):
        m_model = glm.mat4()
        # translate
        m_model = glm.translate(m_model, self.pos)
        # rotate
        m_model = glm.rotate(m_model, glm.radians(self.roll), glm.vec3(0, 0, 1))
        # scale
        m_model = glm.scale(m_model, glm.vec3(self.scale, 0))
        return m_model

    def render(self):
        self.m_model = self.get_model_matrix()
        self.update()
        self.vao.render(instances=self.size*self.size)
