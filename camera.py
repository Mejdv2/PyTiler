import glm
import pygame as pg

FOV = 50  # deg
NEAR = 0.1
FAR = 100
SPEED = 320
SENSITIVITY = 0.04


class Camera:
    def __init__(self, app, position=(0, 0, 4), roll=0):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.roll = roll
        # view matrix
        self.m_view = self.get_view_matrix()
        # projection matrix
        self.m_proj = self.get_projection_matrix()

    def update_camera_vectors(self):
        roll = glm.radians(self.roll)

        self.up = glm.normalize(glm.vec3(glm.sin(roll), glm.cos(roll), 0))
        self.right = glm.normalize(self.up.yxz * glm.vec3(1, -1, 0))



    def update(self):
        self.move()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()


    def move(self):
        velocity = SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.position += glm.vec3(0, 1, 0) * velocity
        if keys[pg.K_s]:
            self.position -= glm.vec3(0, 1, 0) * velocity
        if keys[pg.K_a]:
            self.position -= glm.vec3(1, 0, 0) * velocity
        if keys[pg.K_d]:
            self.position += glm.vec3(1, 0, 0) * velocity
        if keys[pg.K_q]:
            self.position += glm.vec3(0, 0, -1) * velocity
        if keys[pg.K_e]:
            self.position -= glm.vec3(0, 0, -1) * velocity


    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + glm.vec3(0, 0, -1), self.up)

    def get_projection_matrix(self):
        return glm.ortho(-320, 320, -240, 240, 0, 100)




















