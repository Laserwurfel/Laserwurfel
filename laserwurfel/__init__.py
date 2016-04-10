from __future__ import unicode_literals, print_function

from direct.showbase.ShowBase import ShowBase, DirectObject
from direct.interval.IntervalGlobal import *
from direct.interval.LerpInterval import LerpHprInterval
from direct.task import Task
from panda3d.core import *
from pandac.PandaModules import *

import config

ASSET = "../assets/"


class Laserwurfel(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # self.render.set_antialias(p.AntialiasAttrib.M_auto)
        self.disableMouse()
        self.mouse_picker = Picker(self)
        self.initial_node = None

        self.cube = self.loader.loadModel(ASSET + 'models/game_elements/cube')
        self.cube.set_name('Planet')
        self.cube.reparent_to(self.render)

        self.nodes = [[
            [[
                [
                    Node(x, y, z, self)
                    if [x, y, z].count(0) < 2 else None
                    for z in [-1, 0, 1]
                ]
            ] for x in [-1, 0, 1]]
        ] for y in [-1, 0, 1]]

        sun = DirectionalLight('sun')
        sun.set_color((1.0, 1.0, 1.0, 1.0))
        self.sun = self.render.attach_new_node(sun)
        self.sun.set_hpr(0, -20, 0)
        self.cube.set_light(self.sun)

        ambient = AmbientLight("ambient")
        ambient.set_color((0.4, 0.4, 0.4, 1.0))
        self.ambient = self.render.attach_new_node(ambient)
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
                    if item[0].startswith("rot"):
                        self.accept(
                            key,
                            self.move_camera(actions[item[0]])
                        )
                    else:
                        self.accept(
                            key, actions[item[0]]
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

            # perform movement on target
            self.pivot_target.set_hpr(
                self.pivot_target.get_hpr() +
                movement() * 90
            )

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
                return Vec3(2 * d, -d, 2 * d)  # FIXME?
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

    def SetInitialNode(self, node):
        self.initial_node = node

    def GetCurrentNode(self):
        node = self.initial_node
        while node and node.get_next():
            node = node.get_next()
        return node

    def OnNodeSelected(self, obj, select=True):

        pos = []
        for v in obj.getName().split("|")[1].split(","):
            pos.append(int(v)+1)
        node = self.nodes[pos[0]][0][pos[1]][0][pos[2]]
        current_node = self.GetCurrentNode()

        # Debug information
        print("----")
        print("Clicked node:", node.get_position())
        if current_node:
            print("Current:", current_node.get_position())
        if node.get_prev():
            print("Prev:", node.get_prev().get_position())
        print(node.get_next())
        if node.get_next():
            print("Next:", node.get_next().get_position())
        print("Selected:", node.is_selected())

        if node.is_selected() == select:
            return

        if current_node:
            if node is current_node and node.get_is_editable():
                if node.get_prev():
                    self.ConnectNodes(node.get_prev(), node, connect=False)
            else:
                print("Cliked", node.is_selected(), node.get_is_editable())
                if node.is_selected():
                    if node.get_is_editable():
                        self.ConnectNodes(node.get_prev(), node, connect=False)
                else:
                    self.ConnectNodes(current_node, node)

        node.select(select)

        # Debug information
        print("~~ NEW ~~")
        current_node = self.GetCurrentNode()
        if current_node:
            print("Current:", current_node.get_position())
        if node.get_prev():
            print("Prev:", node.get_prev().get_position())
        if node.get_next():
            print("Next:", node.get_next().get_position())
        print("Selected:", node.is_selected())

    def ConnectNodes(self, node1, node2, connect=True):
        print("Connect", node1, node2, connect)
        if not connect:
            node = node2
            if node.get_next():
                node.get_next().select(False)
                if node.laser:
                    node.laser[1].setColor(0, 0, 1)
            while node.get_next():
                node = node.get_next()
                if node.laser:
                    node.laser[1].setColor(0, 0, 1)
                node.select(False)

            node2 = None
        if node2 and node2.get_prev():
            return False

        node1.connect_to(node2)

        # TODO: Prevent illegal connections
        # TODO: Updated lasers lines (also dotted)
        return True


class Node():
    def __init__(self, x, y, z, cube):
        self.model = cube.loader.loadModel(ASSET + 'models/game_elements/node')
        self.model.setName("Node|"+str(x)+","+str(y)+","+str(z))
        self.position = (x, y, z)
        self.selected = False
        self.is_destination = False
        self.is_editable = True
        self.next_node = None
        self.prev_node = None
        self.laser = None

        self.model.reparent_to(cube.cube)
        self.model.set_pos(4 * x, 4 * y, 4 * z)
        self.model.look_at(0, 0, 0)
        self.model.set_hpr(
            self.model,
            (0, 90, 0),
        )
        cube.mouse_picker.makePickable(self.model)

        light = PointLight('node_light')
        light.setColor(VBase4(1, 0, 0, 0.5))
        self.lnp = render.attachNewNode(light)
        self.lnp.set_pos(5 * y, 5 * x, 5 * z)

        # Only for testing:
        if self.position == (-1, -1, 1):
            self.select(True)
            self.is_editable = False
            cube.SetInitialNode(self)

    def get_tip(self):
        d = 5.2
        return (
            self.position[1] * d,
            self.position[0] * d,
            self.position[2] * d,
        )

    def get_position(self):
        return self.position

    def select(self, selected):
        self.selected = selected
        if selected:
            render.setLight(self.lnp)
        else:
            render.clearLight(self.lnp)

    def is_selected(self):
        return self.selected

    def get_is_editable(self):
        return self.is_editable

    def connect_to(self, node):
        self.next_node = node
        if node:
            node.prev_node = self

            # Draw the line
            line = LineSegs("laser")
            line.setColor(1, 0, 0)
            line.setThickness(1)
            line.moveTo(self.get_tip())
            line.drawTo(node.get_tip())
            self.laser = [render.attachNewNode(line.create(False)), line]
            print("Line:", line, line.getVertices())

        elif self.laser:
            self.laser[0].removeNode()

    def get_next(self):
        return self.next_node

    def get_prev(self):
        return self.prev_node


# For making nodes clickable
class Picker(DirectObject.DirectObject):
    def __init__(self, cube):
        self.cube = cube

        # Collision setup
        self.picker = CollisionTraverser()
        self.queue = CollisionHandlerQueue()

        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.picker.addCollider(self.pickerNP, self.queue)
        self.picked_obj = None
        self.accept('mouse1', self.OnClickedLeft)
        self.accept('mouse3', self.OnClickedRight)

    # Sets the pickable tag on objects
    def makePickable(self, obj):
        obj.setTag('pickable', 'true')

    # Returns picked object closest to the camera
    def getObjectHit(self, mpos):
        self.picked_obj = None
        self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
        self.picker.traverse(render)
        if self.queue.getNumEntries() > 0:
            self.queue.sortEntries()
            self.picked_obj = self.queue.getEntry(0).getIntoNodePath()
            parent = self.picked_obj.getParent()
            self.picked_obj = None

            while parent != render:
                if parent.getTag('pickable') == 'true':
                    self.picked_obj = parent
                    return parent
                else:
                    parent = parent.getParent()
        return None

    def getPickedObject(self):
        return self.picked_obj

    def OnClickedLeft(self):
        self.getObjectHit(base.mouseWatcherNode.getMouse())
        if self.picked_obj:
            self.cube.OnNodeSelected(self.picked_obj)

    def OnClickedRight(self):
        self.getObjectHit(base.mouseWatcherNode.getMouse())
        if self.picked_obj:
            self.cube.OnNodeSelected(self.picked_obj, select=False)
