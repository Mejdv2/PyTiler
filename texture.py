import pygame as pg
import moderngl as mgl

import sys, time, os


class Texture:
    def __init__(self, ctx:mgl.Context):
        self.ctx = ctx
        self.textures = {}
        self.textures["background"] = self.get_texture("textures/background.png")
        self.textures["player"] = self.get_texture_array("textures/entities/player/idle/")
        self.textures["texArr"] = self.get_texture_array("textures/tiles/grass/")

    def get_depth_texture(self, size):
        depth_texture = self.ctx.depth_texture(size)
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture
    
    
    def get_render_texture(self, size):
        render_texture:mgl.Texture = self.ctx.texture(size, components=4)
        render_texture.repeat_x = False
        render_texture.repeat_y = False
        render_texture.filter = (mgl.NEAREST_MIPMAP_NEAREST, mgl.NEAREST)
        render_texture.build_mipmaps(0, 0)
        render_texture.filter = (mgl.NEAREST_MIPMAP_NEAREST, mgl.NEAREST)
        # AF
        render_texture.anisotropy = 1.0
        return render_texture


    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=4,
                                   data=pg.image.tostring(texture, 'RGBA'))
        # mipmaps
        texture.filter = (mgl.NEAREST_MIPMAP_NEAREST, mgl.NEAREST)
        texture.build_mipmaps(0, 0)
        texture.filter = (mgl.NEAREST_MIPMAP_NEAREST, mgl.NEAREST)
        # AF
        texture.anisotropy = 1.0
        return texture
    

    def get_texture_array(self, path):
        textures = []
        for texture in sorted(os.listdir(path)):
            textures.append(path + texture)
        
        t_size = pg.image.load(path + texture).get_size()
        tex_array = self.ctx.texture_array((t_size[0], t_size[1], len(textures)), 4)
            
        for index, texture_path in enumerate(textures):
            texture = pg.image.load(texture_path).convert()
            texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            texture = self.ctx.texture(size=texture.get_size(), components=4,
                                    data=pg.image.tostring(texture, 'RGBA'))
            # mipmaps
            texture.filter = (mgl.NEAREST_MIPMAP_NEAREST, mgl.NEAREST)
            texture.build_mipmaps(0, 0)
            texture.filter = (mgl.NEAREST_MIPMAP_NEAREST, mgl.NEAREST)
            # AF
            texture.anisotropy = 1.0

            tex_array.write(texture.read(), (0, 0, index, t_size[0], t_size[1], 1))

        tex_array.filter = (mgl.NEAREST_MIPMAP_NEAREST, mgl.NEAREST)
        tex_array.build_mipmaps(0, 0)
        tex_array.filter = (mgl.NEAREST_MIPMAP_NEAREST, mgl.NEAREST)



        return tex_array

    def destroy(self):
        [tex.release() for tex in self.textures.values()]