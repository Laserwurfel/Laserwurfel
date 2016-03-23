from __future__ import unicode_literals, print_function

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

ASSET = "../assets/"


class Laserwurfel(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # self.render.set_antialias(p.AntialiasAttrib.M_auto)
        self.disableMouse()

        self.cube = self.loader.loadModel(ASSET + 'models/game_elements/cannon')
        self.cube.set_name('Cannon')
        self.cube.set_pos(0, 10, -2)
        self.cube.set_hpr(-90, 0, 0)
        self.cube.reparent_to(self.render)

        ambient = DirectionalLight('sun')
        ambient.set_color((1.0, 1.0, 1.0, 1.0))
        self.ambient = self.render.attach_new_node(ambient)
        self.ambient.set_hpr(0, -20, 0)
        self.render.set_light(self.ambient)

        self.music = self.loader.loadSfx(ASSET + 'music/menu.ogg')
        self.music.set_loop(True)
        self.music.play()
