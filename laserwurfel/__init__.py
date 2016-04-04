from __future__ import unicode_literals, print_function

from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import *
from direct.interval.LerpInterval import LerpHprInterval
from direct.task import Task
from panda3d.core import *

import config

ASSET = "../assets/"


class Laserwurfel(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # self.render.set_antialias(p.AntialiasAttrib.M_auto)
        self.disableMouse()

        self.cube = self.loader.loadModel(ASSET + 'models/game_elements/cube')
        self.cube.set_name('Planet')
        self.cube.reparent_to(self.render)

        ambient = DirectionalLight('sun')
        ambient.set_color((1.0, 1.0, 1.0, 1.0))
        self.ambient = self.render.attach_new_node(ambient)
        self.ambient.set_hpr(0, -20, 0)
        self.render.set_light(self.ambient)

        self.music = self.loader.loadSfx(ASSET + 'music/menu.ogg')
        self.music.set_loop(True)
        # self.music.play() TODO enable

        self.pivot = self.render.attach_new_node("pivot")
        self.pivot_target = self.render.attach_new_node("pivot-target")
        self.camera.reparent_to(self.pivot)
        self.camera.set_pos(0, -50, 0)
        self.move_camera_lerp = None

        # Mouse
        self.accept("mouse1", self.OnLeftDown)
        self.accept("mouse3", self.OnRightDown)
        self.last_click = None
        self.taskMgr.add(self.mouse_drag_task, "MouseDragTask")

        self.SetKeybindings()

    def SetKeybindings(self):

        # Keyboard
        actions = {
            "topleft": self.OnTopLeft,
            "topcenter": self.OnTopCenter,
            "topright": self.OnTopRight,
            "middleleft": self.OnMiddleLeft,
            "middleright": self.OnMiddleRight,
            "bottomleft": self.OnBottomLeft,
            "bottomcenter": self.OnBottomCenter,
            "bottomright": self.OnBottomRight,
            "rotleft": self.OnRotLeft,
            "rotright": self.OnRotRight,
            "rotup": self.OnRotUp,
            "rotdown": self.OnRotDown,
            "rotclock": self.OnRotClock,
            "rotcounterclock": self.OnRotCounterClock
        }

        keys = []
        duplicates = []
        items = config.parser.items("Controls")
        for item in items:
            for key in item[1].split(","):
                if key in keys:
                    duplicates.append(key)
                keys.append(key)

        for item in items:
            for key in item[1].split(","):
                if key not in duplicates:
                    self.accept(
                        key,
                        self.move_camera(actions[item[0]])
                    )

    def move_camera(self, movement):
        def _move():
            # stop ongoing lerp
            if self.move_camera_lerp:
                if self.move_camera_lerp.is_finished():
                    # normalize hpr
                    for node in [self.pivot_target, self.pivot]:
                        hpr = node.get_hpr()
                        for i in hpr:
                            if i >= 360:
                                i %= 360
                        node.set_hpr(hpr)
                else:
                    self.move_camera_lerp.finish()

            hpr = self.pivot_target.get_hpr()
            if hpr[0] % 90 != 0 or hpr[1] % 90 != 0 or hpr[2] % 90 != 0:
                # snap camera to nearest right angle
                for i in range(3):
                    hpr[i] = round(hpr[i] / 90.0) * 90
                self.pivot_target.set_hpr(hpr)
            else:
                # perform movement on target
                self.pivot_target.set_hpr(hpr + movement() * 90)

            # lerp camera to target
            self.move_camera_lerp = LerpHprInterval(
                self.pivot,
                1,
                self.pivot_target.get_hpr(),
                blendType="easeOut",
            ).start()

        return _move

    def get_pivot_h(self, d):
        p = self.pivot_target.get_p() % 360 / 90
        r = self.pivot_target.get_r() % 360 / 90
        if p % 2 != 0:
            if r % 2 == 0:
                return Vec3(-d, -d, 0)
            else:
                return Vec3(2*d, -d, 2*d)  # FIXME?
        elif r == 0:
            return Vec3((1 - p), 0, 0)
        elif r == 1:
            return Vec3(0, (p - 1), 0)
        elif r == 2:
            return Vec3((p - 1), 0, 0)
        elif r == 3:
            return Vec3(0, (1 - p), 0)

    def get_pivot_p(self, d):
        p = self.pivot_target.get_p() % 360 / 90
        r = self.pivot_target.get_r() % 360 / 90
        if r == 0:
            return Vec3(0, -d, 0)
        elif r == 1:
            if p % 2 == 0:
                return Vec3(d, 0, 0)
            else:
                return Vec3(d, (p - 2), d)
        elif r == 2:
            return Vec3(0, d, 0)
        elif r == 3:
            if p % 2 == 0:
                return Vec3(-d, 0, 0)
            else:
                return Vec3(-d, (p - 2), -d)

    def get_pivot_r(self, d):
        return Vec3(0, 0, d)

    def OnRotLeft(self):
        return self.get_pivot_h(-1)

    def OnRotRight(self):
        return self.get_pivot_h(1)

    def OnRotUp(self):
        return self.get_pivot_p(1)

    def OnRotDown(self):
        return self.get_pivot_p(-1)

    def OnRotClock(self):
        return self.get_pivot_r(1)

    def OnRotCounterClock(self):
        return self.get_pivot_r(-1)

    def OnTopLeft(self):
        pass

    def OnTopCenter(self):
        pass

    def OnTopRight(self):
        pass

    def OnMiddleLeft(self):
        pass

    def OnMiddleRight(self):
        pass
    def OnBottomLeft(self):
        pass

    def OnBottomCenter(self):
        pass

    def OnBottomRight(self):
        pass

    def mouse_drag_task(self, task):
        mw = self.mouseWatcherNode
        if mw.hasMouse():
            x = mw.getMouseX()
            y = mw.getMouseY()
            if mw.isButtonDown(MouseButton.one()):
                self.OnMouseMotion(x, y)
        return Task.cont

    def OnLeftDown(self):
        self.last_click = None

    def OnRightDown(self):
        print("OnRightDown")

    def OnMouseMotion(self, x, y):
        if self.last_click is None:
            self.last_click = Vec2(x, y)
        else:
            here = Vec2(x, y)
            diff = here - self.last_click
            self.last_click = here

            if diff.x > 0:
                dh = 1
            elif diff.x < 0:
                dh = -1
            else:
                dh = 0

            if diff.y > 0:
                dp = 1
            elif diff.y < 0:
                dp = -1
            else:
                dp = 0

            self.pivot_target.set_hpr(
                self.pivot_target.get_hpr() +
                Vec3(
                    -diff.x,
                    diff.y,
                    0,
                ) * 50
            )
            self.pivot.set_hpr(self.pivot_target.get_hpr())
