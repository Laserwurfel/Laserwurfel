from __future__ import print_function
from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, MouseButton

import config


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()

        self.scene = self.loader.loadModel("environment")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.taskMgr.add(self.mouseDragTask, "MouseDragTask")

        self.pandaActor = Actor("panda-model",
                                {"walk": "panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        self.pandaActor.loop("walk")

        pandaPosInterval1 = self.pandaActor.posInterval(
            13,
            Point3(0, -10, 0),
            startPos=Point3(0, 10, 0))

        pandaPosInterval2 = self.pandaActor.posInterval(
            13,
            Point3(0, 10, 0),
            startPos=Point3(0, -10, 0))

        pandaHprInterval1 = self.pandaActor.hprInterval(
            3,
            Point3(180, 0, 0),
            startHpr=Point3(0, 0, 0))

        pandaHprInterval2 = self.pandaActor.hprInterval(
            3,
            Point3(0, 0, 0),
            startHpr=Point3(180, 0, 0))

        self.pandaPace = Sequence(
            pandaPosInterval1,
            pandaHprInterval1,
            pandaPosInterval2,
            pandaHprInterval2,
            name="pandaPace"
        )

        self.pandaPace.loop()
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

        items = config.parser.items("Controls")
        for item in items:
            for button in item[1].split(","):
                self.accept(button, actions[item[0]])

        # Mouse
        self.accept("mouse1", self.OnLeftDown)
        self.accept("mouse3", self.OnRightDown)

    def mouseDragTask(self, task):
        mw = self.mouseWatcherNode
        if mw.hasMouse():
            x = mw.getMouseX()
            y = mw.getMouseY()
            if mw.isButtonDown(MouseButton.one()):
                self.OnMouseMotion(x, y)
        return Task.cont

    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(
            20 * sin(angleRadians),
            -20.0 * cos(angleRadians),
            3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

    def OnTopLeft(self):
        print("OnTopLeft")

    def OnTopCenter(self):
        print("OnTopCenter")

    def OnTopRight(self):
        print("OnTopRight")

    def OnMiddleLeft(self):
        print("OnMiddleLeft")

    def OnMiddleRight(self):
        print("OnMiddleRight")

    def OnBottomLeft(self):
        print("OnBottomLeft")

    def OnBottomCenter(self):
        print("OnBottomCenter")

    def OnBottomRight(self):
        print("OnBottomRight")

    def OnRotLeft(self):
        print("OnRotLeft")

    def OnRotRight(self):
        print("OnRotRight")

    def OnRotUp(self):
        print("OnRotUp")

    def OnRotDown(self):
        print("OnRotDown")

    def OnRotClock(self):
        print("OnRotClock")

    def OnRotCounterClock(self):
        print("OnRotCounterClock")

    def OnLeftDown(self):
        print("OnLeftDown")

    def OnRightDown(self):
        print("OnRightDown")

    def OnMouseMotion(self, x, y):
        print("OnMouseMotion", x, y)


app = MyApp()
app.run()
