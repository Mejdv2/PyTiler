from model import *


class Scene:
    def __init__(self, app):
        self.app = app
        self.mesh = app.mesh
        self.ctx:mgl.Context = app.ctx
        self.opaque_objects = []
        self.tp_objects = []
        self.load()
        self.bg = Background(app)
        self.pr = ProcessRender(app)
        self.event_manager = EventManager(app)
        
        self.mesh.texture.textures['depth_texture']  = self.mesh.texture.get_depth_texture(glm.ivec2(2480, 1920))
        self.mesh.texture.textures['render_texture'] = self.mesh.texture.get_render_texture(glm.ivec2(2480, 1920))

        self.depth_texture = self.mesh.texture.textures['depth_texture']
        self.render_texture = self.mesh.texture.textures['render_texture']
        self.pre_process_fbo = self.ctx.framebuffer(depth_attachment=self.depth_texture, color_attachments=self.render_texture)

    def add_opaque_object(self, obj):
        self.opaque_objects.append(obj)

    def add_tp_object(self, obj):
        self.tp_objects.append(obj)

    def load(self):
        add = self.add_opaque_object
        add(Tilemap(self.app))

    def render(self):
        self.pre_process_fbo.clear()
        self.pre_process_fbo.use()
        for obj in self.opaque_objects:
            obj.render()

        self.bg.render()
        
        for obj in self.tp_objects:
            obj.render()

        self.ctx.screen.use()
        self.pr.render(self.render_texture)

        
