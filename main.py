import pygame as pg
import moderngl as mgl
import sys, time
from model import *
from camera import Camera
from mesh import Mesh
from scene import Scene

#Aliasing Probs

#1,000,000 TILES

class GraphicsEngine:
    def __init__(self, win_size=(640, 480)):
        # init pygame modules
        pg.init()
        # window size
        self.WIN_SIZE = glm.ivec2(win_size)
        # set opengl attr
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        # create opengl context
        pg.display.set_caption("Ninjine")
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE, vsync=1)
        # detect and use existing opengl context
        self.ctx = mgl.create_context()
        self.ctx.front_face = 'ccw'
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.BLEND | mgl.CULL_FACE)
        self.ctx.cull_face = "back"
        self.ctx.depth_func = "<="
        self.ctx.blend_func = (mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA)
        self.ctx.blend_equation = mgl.FUNC_ADD

        # create an object to help track time
        self.clock = pg.time.Clock()
        self.start_time = time.time()
        self.time = time.time()

        self.frames = 0
        self.delta_time = 0
        # camera
        self.camera = Camera(self)
        # mesh
        self.mesh = Mesh(self)
        # scene
        self.scene = Scene(self)

        # events
        self.events = []

    def check_events(self):
        self.events = pg.event.get()

        self.scene.event_manager.handle_events(self.events)

    def render(self):
        # clear framebuffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        # render scene
        self.scene.render()
        # swap buffers
        pg.display.flip()

    def get_time(self):
        self.time = time.time()

    def run(self):
        while True:
            self.frames += 1
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = time.time() - self.time
            try:
                print(1/self.delta_time, " FPS")
            except:
                print(self.delta_time, " Delta")

# Insane

if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()






























