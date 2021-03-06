from __future__ import unicode_literals, print_function

import math
import operator
import random
import config
from os import path
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase, DirectObject
from direct.interval.IntervalGlobal import *
from direct.interval.LerpInterval import LerpQuatInterval
from direct.task import Task
from panda3d.core import *
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.gui.DirectGui import DirectFrame
import sys
import level

ASSET = "../assets/"
LEVELS = path.join("assets", "levels")


class Laserwurfel(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.drawMain()
        # global music
        global music
        music = base.loader.loadSfx(ASSET + "music/menu.ogg")
        music.setLoop(True)
        music.setVolume(0.5)
        print(music.getVolume())
        music.play()
        base.setBackgroundColor(0.1, 0.1, 0.1)
        global playMusic
        playMusic = True

    def startGame(self, num):
        # self.render.set_antialias(p.AntialiasAttrib.M_auto)
        self.disableMouse()
        self.mouse_picker = Picker(self)
        self.initial_node = None
        self.end_node = None
        self.level = level.Level()

        self.cube = self.loader.loadModel(ASSET + 'models/game_elements/cube')
        self.cube.set_name('Planet')
        self.cube.reparent_to(self.render)
        self.nodes = [
            [
                [
                    Node(x, y, z, self)
                    if [x, y, z].count(0) < 2 else None
                    for z in [-1, 0, 1]
                ]
            for x in [-1, 0, 1]]
        for y in [-1, 0, 1]]

        sun = DirectionalLight('sun')
        sun.set_color(VBase4(0.8, 0.8, 0.5, 1.0))
        self.sun = self.render.attach_new_node(sun)
        self.sun.set_hpr(-45, -45, 0)
        self.render.set_light(self.sun)

        fill = DirectionalLight('fill')
        fill.set_color(VBase4(0.5, 0.5, 0.8, 1.0))
        self.fill_light = self.render.attach_new_node(fill)
        self.fill_light.set_hpr(135, 45, 0)
        self.render.set_light(self.fill_light)

        ambient = AmbientLight("ambient")
        ambient.set_color(VBase4(0.2, 0.2, 0.2, 1.0))
        self.ambient = self.render.attach_new_node(ambient)
        self.render.set_light(self.ambient)

        self.camera_target = self.render.attach_new_node('camera-target')
        self.camera_pivot = self.render.attach_new_node("camera-pivot")
        self.camera.reparent_to(self.camera_pivot)
        self.camera.set_pos(0, -50, 0)
        self.camera_lerp = None

        def _place_facing_helper(x, z):
            helper = self.camera_pivot.attach_new_node('facing-helper')
            helper.set_pos(x, -1, z)
            return helper

        self.facing_helper = [
            [
                _place_facing_helper(x, z)
            for x in [-1, 0, 1]]
        for z in [-1, 0, 1]]

        # Mouse
        self.accept("mouse1", self.OnLeftDown)
        self.last_click = None
        self.taskMgr.add(self.mouse_drag_task, "MouseDragTask")

        self.SetKeybindings()
        # TODO: Do not hard code level number
        self.LoadLevel(num)
        self.introDialoge(num)

    def drawMain(self):
        myFrame = DirectFrame(frameColor=(0, 0, 0.30, 1),
                          frameSize=(-1.75, 1.75, -1, 1),
                          pos=(0,0,0))

        v = [0]
        bk_text = "LASERWURFEL"
        textObject = OnscreenText(text = bk_text, pos = (0,0.8), 
        scale = 0.2,fg=(1,1,1,1),align=TextNode.ACenter,mayChange=1, parent=myFrame)

        def switchCamp():
            self.drawCampaign()
            myFrame.destroy()

        def switchSettings():
            self.drawSettings()
            myFrame.destroy()   

        def quit():
            sys.exit()  

        #resume = DirectButton(text = ("Resume last saved game"), scale=.05, command=switchCamp, pos=(0,0,0.5), parent=myFrame, frameSize=(-20, 20, -1.5, 1.9))
        campaign = DirectButton(text = ("Campaign"), scale=.05, command=switchCamp, pos=(0,0,0.25), parent=myFrame, frameSize=(-20, 20, -1.5, 1.9))
        settings = DirectButton(text = ("Settings"), scale=.05, command=switchSettings, pos=(0,0,0), parent=myFrame, frameSize=(-20, 20, -1.5, 1.9))
        quit = DirectButton(text = ("Quit"), scale=.05, command=quit, pos=(0,0,-0.25), parent=myFrame, frameSize=(-20, 20, -1.5, 1.9))

    def drawCampaign(self):
        v = [0]
        yPos = 0.5
        xDivider = 0;
        myFrame = DirectFrame(frameColor=(0, 0, 0.30, 1),
                          frameSize=(-1.75, 1.75, -1, 1)
                          ,pos=(0,0,0))

        bk_text = "Campaign"
        textObject = OnscreenText(text = bk_text, pos = (0,0.8), 
        scale = 0.2,fg=(1,1,1,1),align=TextNode.ACenter,mayChange=1, parent=myFrame)        

        def chooseLevel(num):
            self.current_level = num
            self.startGame(num)
            music.stop()
            myFrame.destroy()

        def switchMain():
            self.drawMain()
            myFrame.destroy()

        for x in range(1, 21):
            if(x % 9 == 0 and x > 0):
                yPos -= 0.5
                xDivider = 0
            xPos = -1 + (xDivider/4.0)
            xDivider += 1

            available = int(config.parser.items("Levels")[0][1])
            if x <= available:
                state = DGG.NORMAL
                color = (0, 1, 0, 1)
            else:
                state = DGG.DISABLED
                color = (1, 0, 0, 1)

            DirectButton(
                text=("Level " + repr(x)),
                scale=.05,
                command=chooseLevel,
                extraArgs=[x],
                pos=(xPos, 0, yPos),
                parent=myFrame,
                frameSize=(-2, 2, -1.5, 1.9),
                frameColor=color,
                state=state
            )


        returnToMenu = DirectButton(text = ("Return to main menu"), scale=.05, command=switchMain, pos=(0,0,-0.8), parent=myFrame, frameSize=(-22, 22, -1.5, 1.9))  

    def introDialoge(self, num):
        dsf1=self.mkdsf()
        dsf1.setPos(0,0,0)
        t1=OnscreenText(parent=dsf1.getCanvas(), pos=(1,0), scale=.05, wordwrap=35)
        t1['text'] = self.LoadStory(num)['intro']
        def closeWindow():
            dsf1.destroy()

        btn_continue = DirectButton(text = ("Continue"), scale=.05,  parent=dsf1.getCanvas(), frameSize=(-3, 3, -1.5, 1.9), pos=(1,0,-2.7), command=closeWindow)

    def outroDialoge(self):
        dsf1 = self.mkdsf()
        dsf1.setPos(0, 0, 0)
        t1 = OnscreenText(
            parent=dsf1.getCanvas(),
            pos=(1, 0),
            scale=.05,
            wordwrap=35
        )
        t1['text'] = self.LoadStory(1)['outro']

        def closeWindow():
            dsf1.destroy()
            available = int(config.parser.items("Levels")[0][1])
            if available == self.current_level:
                config.parser.set("Levels", "available", str(available + 1))
                config.write()
            self.closeLevel()

        DirectButton(
            text=("Continue"),
            scale=.05,
            parent=dsf1.getCanvas(),
            frameSize=(-3, 3, -1.5, 1.9),
            pos=(1, 0, -2.7),
            command=closeWindow
        )

    def mkdsf(self):
        size = (0.15, 0.15)
        bgcol=(.2, .2, .2, .5)
        scrollbarw=0.05
        borderw=(0.01,0.01)
        return DirectScrolledFrame(
            frameSize=(-1 ,1,-1,1),
            canvasSize=(-0, 0, -3, .1),
            borderWidth=borderw,
            scrollBarWidth=scrollbarw,
            scale=1,
        ) 

    def drawSettings(self):
        myFrame = DirectFrame(frameColor=(0, 0, 0.30, 1),
                          frameSize=(-1.75, 1.75, -1, 1)
                          ,pos=(0,0,0))


        bk_text = "Settings"
        textObject = OnscreenText(text = bk_text, pos = (0,0.8), 
        scale = 0.2,fg=(1,1,1,1),align=TextNode.ACenter,mayChange=1, parent=myFrame)

        def switchMain():
            self.drawMain()
            myFrame.destroy()   

        def switchAudio():
            self.drawAudio()
            myFrame.destroy()

        def reset():
            self.drawReset()
            myFrame.destroy()
                 
        def drawButtons():      
            audio = DirectButton(text = ("Audio"), scale=.05, command=switchAudio, pos=(0,0,0.5), parent=myFrame, frameSize=(-20, 20, -1.5, 1.9))
            controls = DirectButton(text = ("Controls"), scale=.05, command=reset, pos=(0,0,0.25), parent=myFrame, frameSize=(-20, 20, -1.5, 1.9))
            resetGame = DirectButton(text = ("Reset game"), scale=.05, command=reset, pos=(0,0,0), parent=myFrame, frameSize=(-20, 20, -1.5, 1.9))
            credits = DirectButton(text = ("Credits"), scale=.05, command=reset, pos=(0,0,-0.25), parent=myFrame, frameSize=(-20, 20, -1.5, 1.9))
            returnToMenu = DirectButton(text = ("Return to main menu"), scale=.05, command=switchMain, pos=(0,0,-0.5), parent=myFrame, frameSize=(-20, 20, -1.5, 1.9))      
        drawButtons()

    def drawReset(self):
        myFrame = DirectFrame(frameColor=(0, 0, 0.30, 1),
                          frameSize=(-1.75, 1.75, -1, 1)
                          ,pos=(0,0,0))

        def resetGame(arg):
            if(arg):
                print('reset')
            else:
                print('nothing')
            myFrame.destroy()
            self.drawSettings()

        dialog = YesNoDialog(dialogName="YesNoCancelDialog", text="Erase your progress?", command=resetGame, parent=myFrame)

    def drawAudio(self):
        myFrame = DirectFrame(frameColor=(0, 0, 0.30, 1),
                          frameSize=(-1.75, 1.75, -1, 1)
                          ,pos=(0,0,0))


        bk_text = "Audio Settings"
        textObject = OnscreenText(text = bk_text, pos = (0,0.8), 
        scale = 0.2,fg=(1,1,1,1),align=TextNode.ACenter,mayChange=1, parent=myFrame)

        def switchSettings():
            self.drawSettings()
            myFrame.destroy()   

        def setVolume():
            music.setVolume(volume['value'])
            print(volume['value'])
            print('Volume set')

        def turnAudio():
            global playMusic
            if(turnAudioControl['text'] == "Turn Music Off"):
                turnAudioControl['text'] = "Turn Music On"
                print('Audio turned off')
                music.stop()
                global playMusic
                playMusic = False
            else:
                turnAudioControl['text'] = "Turn Music Off" 
                music.setLoop(True)
                music.play()
                playMusic = True

            print('Audio turn')
            '''
            if sound.status() == sound.PLAYING:
                print('Audio turned off')
                sound.stop()
            else:
                sound.setLoop(True)
                sound.play()
            ''' 


        volume = DirectSlider(range=(0,1), value=.5, pageSize=3, command=setVolume, pos=(0,0,0.5), parent=myFrame)
        turnAudioControl = DirectButton(text = ("Turn Music Off"), scale=.05, command=turnAudio, pos=(0,0,0.25), parent=myFrame, frameSize=(-20, 20, -1.5, 1.9))
        returnToMenu = DirectButton(text = ("Return to main menu"), scale=.05, command=switchSettings, pos=(0,0,-0.5), parent=myFrame, frameSize=(-20, 20, -1.5, 1.9))

    def quit(self, event=None):
        self.onDestroy(event)
        try:
            base
        except NameError:
            sys.exit()
        base.userExit()

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
                    action = actions[item[0]]()
                    if item[0].startswith('rot'):
                        action = self.move_camera(action)
                    else:
                        action = self.select_node(action)
                    self.accept(key, action)

        self.accept("escape", self.closeLevel)

    def move_camera(self, movement):
        def _move():
            if self.camera_lerp:
                self.camera_lerp.pause()

            # perform movement on target
            self.camera_target.set_quat(
                self.camera_target,
                movement,
            )

            # round to nearest right angle
            self.camera_target.set_hpr(*[
                round(axis / 90.0) * 90
                for axis in self.camera_target.get_hpr()
            ])

            # start lerping
            self.camera_lerp = LerpQuatInterval(
                self.camera_pivot,
                1.0,
                self.camera_target.get_quat(),
                blendType='easeOut',
            )
            self.camera_lerp.start()

        return _move

    def select_node(self, position):
        def _select():
            if False in [a % 90 == 0 for a in self.camera_pivot.get_hpr()]:
                return

            helper = self.facing_helper[position[1]+1][position[0]+1]

            [x, y, z] = [
                int(round(i)) for i in
                helper.get_pos(self.render)
            ]

            node = self.nodes[x+1][y+1][z+1]
            if node.is_disabled:
                return

            self.OnNodeSelected(node)

        return _select

    def OnRotLeft(self):
        return Quat(
            +math.sqrt(0.5),
            +0,
            +0,
            -math.sqrt(0.5),
        )

    def OnRotRight(self):
        return Quat(
            +math.sqrt(0.5),
            +0,
            +0,
            +math.sqrt(0.5),
        )

    def OnRotUp(self):
        return Quat(
            +math.sqrt(0.5),
            -math.sqrt(0.5),
            +0,
            +0,
        )

    def OnRotDown(self):
        return Quat(
            +math.sqrt(0.5),
            +math.sqrt(0.5),
            +0,
            +0,
        )

    def OnRotClock(self):
        return Quat(
            +math.sqrt(0.5),
            +0,
            +math.sqrt(0.5),
            +0,
        )

    def OnRotCounterClock(self):
        return Quat(
            +math.sqrt(0.5),
            +0,
            -math.sqrt(0.5),
            +0,
        )

    def OnTopLeft(self):
        return (-1, 1)

    def OnTopCenter(self):
        return (0, 1)

    def OnTopRight(self):
        return (1, 1)

    def OnMiddleLeft(self):
        return (-1, 0)

    def OnMiddleRight(self):
        return (1, 0)

    def OnBottomLeft(self):
        return (-1, -1)

    def OnBottomCenter(self):
        return (0, -1)

    def OnBottomRight(self):
        return (1, -1)

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
            return

        here = Vec2(x, y)
        diff = self.last_click - here
        diff *= 50
        self.last_click = here

        rotation = Quat()
        rotation.set_hpr(
            Vec3(diff.x, -diff.y, 0),
            CS_default,
        )

        self.camera_target.set_quat(
            self.camera_target,
            rotation,
        )
        self.camera_pivot.set_quat(self.camera_target.get_quat())

    def closeLevel(self):
        print("CLOSE")
        self.music_lvl.stop()
        for node in self.render.getChildren():
            node.removeNode()
        self.render.clearLight()
        self.drawCampaign()

    def SetInitialNode(self, node):
        self.initial_node = node

    def GetCurrentNode(self):
        node = self.initial_node
        while node and node.get_next():
            node = node.get_next()
        return node

    def UpdateCurrentNode(self):
        for y in self.nodes:
            for x in y:
                for node in x:
                    if node:
                        node.set_current(current=False)

        node = self.initial_node
        while node and node.get_next():
            node.set_current(current=False)
            print("NODE", node)
            node = node.get_next()
        if not node.is_destination:
            node.set_current()

    def OnNodeSelected(self, obj, select=True):

        if not isinstance(obj, Node):
            pos = []
            for v in obj.getName().split("|")[1].split(","):
                pos.append(int(v) + 1)
            node = self.nodes[pos[0]][pos[1]][pos[2]]
        else:
            node = obj
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

        # Actual algorithm
        if node.is_selected() == select:
            if not select and node.get_prev():
                self.ConnectNodes(node.get_prev(), node, connect=False)
                node.select(False)
            else:
                return

        if not current_node:
            print("ERROR: No current node!")
            return

        if node is current_node and node.get_is_editable():
            if node.get_prev():
                self.ConnectNodes(node.get_prev(), node, connect=False)
                node.select(select)
        else:
            print("Cliked", node.is_selected(), node.get_is_editable())
            if node.is_selected():
                if node.get_is_editable():
                    self.ConnectNodes(node.get_prev(), node, connect=False)
                    node.select(select)
            elif select:
                if self.ConnectNodes(current_node, node):
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

        self.UpdateCurrentNode()
        self.CheckWin()

    def CheckWin(self):
        win = True
        for w in self.nodes:
            for x in w:
                for y in x:
                    if y and y.model:
                        if not y.is_selected():
                            win = False
        if win:
            self.OnWin()

    def OnWin(self):
        print("~~~~~~ YOU WON THE LEVEL ~~~~~~~")
        self.outroDialoge()

    def ConnectNodes(self, node1, node2, connect=True):
        print("Connect", node1, node2, connect)
        if not connect:
            node2 = None

        else:
            for grid in node1.grids:
                if node2 in grid.nodes:
                    return False

            if node1.is_destination:
                return False

            string_info = self.NodeInLooseString(node2)
            print(string_info)

            if node2.is_destination:
                if node2.get_prev():
                    return False

            if string_info["between"]:
                return False

            if string_info["last"]:
                self.ReverseString(node2)

            if node2.teleport_to:
                node1.connect_to(node2)
                node2.connect_to(node2.teleport_to)
                return True

        node1.connect_to(node2)

        if node1.teleport_to and not node2:
            self.ConnectNodes(node1.get_prev(), node1, connect=False)

        # TODO: Prevent illegal connections
        return True

    def ReverseString(self, node):
        while node:
            prev_node = node.get_prev()

            if node.laser:
                node.laser.removeNode()

            node.prev_node = node.next_node
            node.next_node = prev_node

            node = prev_node

    def NodeInLooseString(self, node):

        if not node:
            return False

        goes_to_end = False
        goes_to_start = False
        is_first = False
        is_last = False
        is_between = False
        next_node = node.get_next()
        prev_node = node.get_prev()

        if not next_node:
            is_last = True

        if not prev_node:
            is_first = True

        if not (is_first or is_last):
            is_between = True

        while next_node:
            if next_node is self.end_node:
                goes_to_end = True
            next_node = next_node.get_next()

        while prev_node:
            if prev_node is self.initial_node:
                goes_to_start = True
            prev_node = prev_node.get_prev()

        if (next_node or prev_node):
            string = True
        else:
            string = False

        return {
            "loose": not (goes_to_start or goes_to_end),
            "first": is_first,
            "last": is_last,
            "between": is_between,
            "string": string
        }

    def LoadStory(self, number):
        level_path_intro = path.join(LEVELS, "level" + str(number), "intro") 
        level_path_outro = path.join(LEVELS, "level" + str(number), "outro")
        print(level_path_intro)
        intro = open(level_path_intro).read()
        outro = open(level_path_outro).read()

        return {
            "intro": intro,
            "outro": outro
        } 

    def LoadLevel(self, number):
        level_path = path.join(LEVELS, "level" + str(number), "full")
        self.level.parse(level_path)

        # Structure
        for line in self.level.structure:
            # print(line[0].__name__)
            if line[0].__name__ == "path":
                initial_node = self.GetNode(line[1])
                initial_node.select(True)
                initial_node.is_editable = False
                initial_node.set_current()
                self.initial_node = initial_node

                end_node = self.GetNode(line[2])
                end_node.setup_model('game_elements/cannon')
                end_node.is_destination = True
                self.end_node = end_node

            elif (line[0].__name__ == "deactivate" and
                  type(line[1][0]) is not str):

                node = self.GetNode(line[1])
                node.model.removeNode()
                node.is_disabled = True

            elif line[0].__name__ == "wall":
                node1 = self.GetNode(line[1])
                node2 = self.GetNode(line[2])
                grid = Grid(node1, node2, self)
                switches = []
                for i in range(len(line)):
                    if i <= 2 or i % 2 != 1:
                        continue

                    j = i + 1
                    switch = Switch(
                        self.GetNode(line[i]), self.GetNode(line[i+1]), self)
                    switches.append(switch)

                grid.switches.append(switches)
                node1.grids.append(grid)
                node2.grids.append(grid)

            elif line[0].__name__ == "teleporter":
                node1 = self.GetNode(line[1])
                node2 = self.GetNode(line[2])
                node1.setup_model('game_elements/teleporter')
                node2.setup_model('game_elements/teleporter')
                node1.teleport_to = node2
                node2.teleport_to = node1

        # Decorations
        i = 1
        j = 1

        def flip():
            flip = random.randint(0, 1)
            if flip == 1:
                return True
            else:
                return False

        sides = ["front", "left", "back", "right", "top", "bottom"]
        for side in sides:

            animal = "dog"
            if flip():
                animal = "rabbit"

            for line in self.level.detail[side]:
                for element in line:
                    model_name = None

                    version = "a"
                    if flip():
                        version = "b"

                    if element == "@@":
                        model_name = "tree_" + version
                    elif element == "##":
                        model_name = "wheat"
                    elif element == "%%":
                        model_name = animal + "_" + version
                    elif element == "[]":
                        model_name = "house_" + version
                    if model_name:
                        model = self.loader.loadModel(
                            ASSET + "models/decorations/" + model_name)

                        # TODO: Random orientation
                        d = 0

                        if side == "front":
                            model.set_hpr(d, 90, 0)
                            model.set_pos(j - 5, -4.5, i - 5)
                        elif side == "left":
                            model.set_hpr(d, -90, -90)
                            model.set_pos(-4.5, j - 5, i - 5)
                        elif side == "back":
                            model.set_hpr(d, -90, 0)
                            model.set_pos(i - 5, 4.5, j - 5)
                        elif side == "right":
                            model.set_hpr(d, -90, 90)
                            model.set_pos(4.5, j - 5, i - 5)
                        elif side == "top":
                            model.set_pos(j - 5, i - 5, 4.5)
                        elif side == "bottom":
                            model.set_hpr(d, -180, 0)
                            model.set_pos(j - 5, i - 5, -4.5)

                        model.reparent_to(self.cube)

                    if j < 9:
                        j += 1
                    else:
                        j = 1
                if i < 9:
                    i += 1
                else:
                    i = 1

        # Meta
        self.music_lvl = self.loader.loadSfx(
            ASSET + 'music/' + self.level.meta["track"][1])
        self.music_lvl.setLoop(True)
        print(music.getVolume())
        self.music_lvl.setVolume(music.getVolume())
        if playMusic:
            self.music_lvl.play()

    def GetNode(self, pos):
        node = self.nodes[pos[0] + 1][pos[1] + 1][pos[2] + 1]
        return node

    def GetPositionBetweenNodes(self, node1, node2):
        vecA = [n * 4.5 for n in node1.position]
        vecB = [n * 4.5 for n in node2.position]
        vecAB = [n / 2 for n in map(operator.sub, vecB, vecA)]
        return [map(operator.add, vecA, vecAB), vecA]


class Grid():
    def __init__(self, node1, node2, cube):
        self.model = cube.loader.loadModel(
            ASSET + 'models/game_elements/grid')
        self.nodes = (node1, node2)
        self.switches = []

        pos = cube.GetPositionBetweenNodes(node1, node2)
        vecC = pos[0]
        vecA = pos[1]
        # TODO: Find correct position for grid
        self.model.set_pos(vecC[0], vecC[1], vecC[2])

        self.model.look_at(vecA[0], vecA[1], vecA[2])
        r3 = [0, 0, 0]
        r4 = self.model.get_hpr()
        r3[0] = r4[0]
        r3[1] = 0
        if vecC[2] < 4.5 and vecC[2] > -4.5:
            r3[1] = 90
        elif vecC[2] == -4.5:
            r3[1] = 180

        # r3[2] = 0
        if (abs(vecC[0]) == 4.5 and abs(vecC[1]) == 4.5 or
            abs(vecC[0]) == 4.5 and abs(vecC[2]) == 4.5 or
                abs(vecC[1]) == 4.5 and abs(vecC[2]) == 4.5):
            r3[2] = -45
        elif abs(vecC[0]) == 4.5:
            r3[2] = 90 * (vecC[0] / 4.5)
            r3[1] = r4[1]
        elif abs(vecC[1]) == 4.5:
            r3[2] = -90 * (vecC[1] / 4.5)
            r3[1] = r4[1]
        elif abs(vecC[2]) == 4.5:
            r3[2] = -90 * (vecC[2] / 4.5)
            r3[1] = r4[1]

        # self.model.look_at(vecA[0], vecA[1], vecA[2])
        self.model.set_hpr(r3[0], r3[1], r3[2])
        self.model.reparent_to(cube.cube)


class Switch():
    def __init__(self, node1, node2, cube):
        self.model = cube.loader.loadModel(
            ASSET + 'models/game_elements/switch')
        self.nodes = (node1, node2)

        pos = cube.GetPositionBetweenNodes(node1, node2)
        vecC = pos[0]
        vecA = pos[1]
        # TODO: Find correct position for grid
        self.model.set_pos(vecC[0], vecC[1], vecC[2])

        self.model.look_at(vecA[0], vecA[1], vecA[2])
        r3 = [0, 0, 0]
        r4 = self.model.get_hpr()
        r3[0] = r4[0]
        r3[1] = 0
        if vecC[2] < 4.5 and vecC[2] > -4.5:
            r3[1] = 90
        elif vecC[2] == -4.5:
            r3[1] = 180

        # r3[2] = 0
        if (abs(vecC[0]) == 4.5 and abs(vecC[1]) == 4.5 or
            abs(vecC[0]) == 4.5 and abs(vecC[2]) == 4.5 or
                abs(vecC[1]) == 4.5 and abs(vecC[2]) == 4.5):
            r3[2] = -45
        elif abs(vecC[0]) == 4.5:
            r3[2] = -90 * (vecC[0] / 4.5)
            r3[1] = r4[1]
        elif abs(vecC[1]) == 4.5:
            r3[2] = -90 * (vecC[1] / 4.5)
            r3[1] = r4[1]
        elif abs(vecC[2]) == 4.5:
            r3[2] = -90 * (vecC[2] / 4.5)
            r3[1] = r4[1]

        print("R3", vecC)
        print("R4", r4)

        # self.model.look_at(vecA[0], vecA[1], vecA[2])
        self.model.set_hpr(r3[0], r3[1], r3[2])
        self.model.reparent_to(cube.cube)


class Node():
    def __init__(self, x, y, z, cube):

        self.position = (y, x, z)
        self.selected = False
        self.is_destination = False
        self.is_editable = True
        self.is_disabled = False
        self.next_node = None
        self.prev_node = None
        self.laser = None
        self.grids = []
        self.cube = cube
        self.indicator = None
        self.teleport_to = None

        self.setup_model("game_elements/node")

        light = PointLight('node_light')
        light.setColor(VBase4(1, 0, 0, 0.5))
        self.lnp = self.model.attachNewNode(light)
        self.lnp.set_pos(y, x, z)

    def setup_model(self, element):
        self.model = self.cube.loader.loadModel(ASSET + "models/" + element)
        self.model.setName(
            "Node|" +
            str(self.position[0]) + "," +
            str(self.position[1]) + "," +
            str(self.position[2]))
        self.model.reparent_to(self.cube.cube)
        self.model.set_pos(
            4 * self.position[0],
            4 * self.position[1],
            4 * self.position[2])
        self.model.look_at(0, 0, 0)
        self.model.set_hpr(
            self.model,
            (0, 90, 0),
        )
        self.cube.mouse_picker.makePickable(self.model)

    def set_current(self, current=True):
        if current:
            self.indicator = self.cube.loader.loadModel(
                ASSET + "models/game_elements/indicator")
            self.indicator.reparent_to(self.cube.cube)
            self.indicator.set_pos(
                4 * self.position[0],
                4 * self.position[1],
                4 * self.position[2])
            self.indicator.look_at(0, 0, 0)
            self.indicator.set_hpr(
                self.indicator,
                (0, 90, 0),
            )
        elif self.indicator:
            self.indicator.removeNode()
            self.indicator = None

    def get_tip(self):
        d = 5.2
        return (
            self.position[0] * d,
            self.position[1] * d,
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

        if node:
            node.prev_node = self

            # Draw the line
            line = LineSegs("laser")
            line.setColor(1, 0, 0)
            line.setThickness(1)
            line.moveTo(self.get_tip())
            line.drawTo(node.get_tip())
            self.laser = render.attachNewNode(line.create(False))

            next_node = node

            # Redraw Laser in red
            while next_node.get_next():
                if next_node.laser:
                    next_node.laser.removeNode()

                line = LineSegs("laser")
                line.setColor(1, 0, 0)
                line.setThickness(1)
                line.moveTo(next_node.get_tip())
                line.drawTo(next_node.get_next().get_tip())
                next_node.laser = render.attachNewNode(line.create(False))

                next_node.select(True)
                next_node = next_node.get_next()

        elif self.laser:
            self.laser.removeNode()
            next_node = self.get_next()
            next_node.select(False)

            # Redraw Laser in blue
            while next_node.get_next():
                if next_node.laser:
                    next_node.laser.removeNode()

                line = LineSegs("laser")
                line.setColor(0, 0, 1)
                line.setThickness(1)
                line.moveTo(next_node.get_tip())
                line.drawTo(next_node.get_next().get_tip())
                next_node.laser = render.attachNewNode(line.create(False))

                next_node = next_node.get_next()
                if next_node:
                    next_node.select(False)

            self.next_node.prev_node = None

        self.next_node = node

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
        self.accept('mouse1-up', self.OnReleasedLeft)
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
        mouse = base.mouseWatcherNode.getMouse()
        self.last_click = (mouse.getX(), mouse.getY())

    def OnReleasedLeft(self):
        try:
            mouse = base.mouseWatcherNode.getMouse()
            if self.last_click != (mouse.getX(), mouse.getY()):
                return
            self.getObjectHit(mouse)
            if self.picked_obj:
                self.cube.OnNodeSelected(self.picked_obj)
        except:
            pass

    def OnClickedRight(self):
        self.getObjectHit(base.mouseWatcherNode.getMouse())
        if self.picked_obj:
            self.cube.OnNodeSelected(self.picked_obj, select=False)
