#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
# import audio
import config
import wx.lib.agw.gradientbutton as GB



class Main(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        sizer = wx.GridBagSizer(20, 20)

        btn_bgcolor = wx.Colour(255,255,255)
        btn_fgcolor = wx.Colour(0,0,0)

        header = wx.StaticText(self, -1, 'LASERWURFEL')
        font = wx.Font(35, wx.SWISS, wx.SLANT, wx.NORMAL)
        header.SetFont(font)
        header.SetForegroundColour('White')

        self.btn_main_menu = GB.GradientButton(self, label="Campaign", size=(350, 50))
        self.btn_endless = GB.GradientButton(self, label="Endless", size=(350, 50))
        self.btn_controls = GB.GradientButton(self, label="Settings", size=(350, 50))
        self.btn_resume = GB.GradientButton(self, label="Resume last saved game", size=(350, 50))
        self.btn_quit = GB.GradientButton(self, label="Quit", size=(350, 50))

        self.setColor(self.btn_main_menu, btn_bgcolor, btn_fgcolor)
        self.setColor(self.btn_endless, btn_bgcolor, btn_fgcolor)
        self.setColor(self.btn_controls, btn_bgcolor, btn_fgcolor)
        self.setColor(self.btn_resume, btn_bgcolor, btn_fgcolor)
        self.setColor(self.btn_quit, btn_bgcolor, btn_fgcolor)

        sizer.Add(header, pos=(0,0), span=(1,5), flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=10)
        sizer.Add(self.btn_main_menu, pos=(1,0), span=(1,2), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)
        sizer.Add(self.btn_endless, pos = (2,0), span=(1,2), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)
        sizer.Add(self.btn_controls, pos = (3,0), span=(1,2), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)
        sizer.Add(self.btn_resume, pos = (4,0), span=(1,2), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)
        sizer.Add(self.btn_quit, pos = (5,0), span=(1,2), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)

        sizer.AddGrowableRow(0)
        sizer.AddGrowableRow(1)
        sizer.AddGrowableRow(2)
        sizer.AddGrowableRow(3)
        sizer.AddGrowableRow(4)

        self.SetSizerAndFit(sizer)

    @staticmethod
    def setColor(button, bg_color, fg_color):
        button.SetBottomEndColour(bg_color)
        button.SetBottomStartColour(bg_color)
        button.SetTopEndColour(bg_color)
        button.SetTopStartColour(bg_color)
        button.SetForegroundColour(fg_color)
        # button.SetFont(wx.Font(25, wx.DEFAULT, wx.NORMAL,0))
        button.SetPressedBottomColour(bg_color)
        button.SetPressedTopColour(bg_color)


class Settings(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        sizer = wx.GridBagSizer(20, 20)

        btn_bgcolor = wx.Colour(255,255,255)
        btn_fgcolor = wx.Colour(0,0,0)
        btn_font_size = 25

        header = wx.StaticText(self, -1, 'Settings')
        font = wx.Font(30, wx.SWISS, wx.SLANT, wx.NORMAL)
        header.SetFont(font)
        header.SetForegroundColour('White')


        self.btn_audio = GB.GradientButton(self, label="Audio", size=(350, 50))
        self.btn_controls = GB.GradientButton(self, label="Controls", size=(350, 50))
        self.btn_reset = GB.GradientButton(self, label="Reset Game", size=(350, 50))
        self.btn_credits = GB.GradientButton(self, label="Credits", size=(350, 50))
        self.btn_return = GB.GradientButton(self, label="Return to main menu", size=(350, 50))

        sizer.Add(header, pos=(0,0), span=(1,5), flag=wx.LEFT|wx.TOP, border=10)
        sizer.Add(self.btn_audio, pos=(1,0), span=(1,2), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)
        sizer.Add(self.btn_controls, pos = (2,0), span=(1,2), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)
        sizer.Add(self.btn_reset, pos = (3,0), span=(1,2), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)
        sizer.Add(self.btn_credits, pos = (4,0), span=(1,2), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)
        sizer.Add(self.btn_return, pos = (5,0), span=(1,2), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)

        self.setColor(self.btn_audio, btn_bgcolor, btn_fgcolor)
        self.setColor(self.btn_controls, btn_bgcolor, btn_fgcolor)
        self.setColor(self.btn_reset, btn_bgcolor, btn_fgcolor)
        self.setColor(self.btn_credits, btn_bgcolor, btn_fgcolor)
        self.setColor(self.btn_return, btn_bgcolor, btn_fgcolor)

        sizer.AddGrowableRow(0)
        sizer.AddGrowableRow(1)
        sizer.AddGrowableRow(2)
        sizer.AddGrowableRow(3)
        sizer.AddGrowableRow(4)

        self.SetSizerAndFit(sizer) 

    @staticmethod
    def setColor(button, bg_color, fg_color):
        button.SetBottomEndColour(bg_color)
        button.SetBottomStartColour(bg_color)
        button.SetTopEndColour(bg_color)
        button.SetTopStartColour(bg_color)
        button.SetForegroundColour(fg_color)
        # button.SetFont(wx.Font(25, wx.DEFAULT, wx.NORMAL,0))
        button.SetPressedBottomColour(bg_color)
        button.SetPressedTopColour(bg_color)


class AudioSettings(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        btn_bgcolor = wx.Colour(255,255,255)
        btn_fgcolor = wx.Colour(0,0,0)

        header = wx.StaticText(self, -1, 'Audio')
        font = wx.Font(30, wx.SWISS, wx.SLANT, wx.NORMAL)
        header.SetFont(font)
        header.SetForegroundColour('White')

        volume = wx.StaticText(self, label="Volume")
        music = wx.StaticText(self, label="Music")
        volume.SetForegroundColour('White')
        music.SetForegroundColour('White')

        self.volumeSlider = wx.Slider(
            self, -1, 100, 0, 100,
            style=wx.SL_HORIZONTAL)

        self.btn_music_switch = GB.GradientButton(self, label="Turn Music Off", size=(350, 50))

        self.setColor(self.btn_music_switch, btn_bgcolor, btn_fgcolor)

        vbox.Add(header, 1, wx.ALL, 10)
        vbox.Add(volume, 1, wx.ALL, 2)
        vbox.Add(self.volumeSlider, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(music, 1, wx.ALL, 2)
        vbox.Add(self.btn_music_switch, 1, wx.EXPAND | wx.ALL, 2)

        self.SetSizerAndFit(vbox)

    @staticmethod
    def setColor(button, bg_color, fg_color):
        button.SetBottomEndColour(bg_color)
        button.SetBottomStartColour(bg_color)
        button.SetTopEndColour(bg_color)
        button.SetTopStartColour(bg_color)
        button.SetForegroundColour(fg_color)
        # button.SetFont(wx.Font(25, wx.DEFAULT, wx.NORMAL,0))
        button.SetPressedBottomColour(bg_color)
        button.SetPressedTopColour(bg_color)


class Keymapping(wx.ScrolledWindow):
    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent=parent, style=wx.VSCROLL)
        self.SetScrollRate(100, 100)

        self.bg_color = (0, 0, 55)
        self.SetBackgroundColour(self.bg_color)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        header = wx.StaticText(self, -1, 'Controls')
        btn_back = wx.Button(self, label="Back")
        self.Bind(wx.EVT_BUTTON, self.OnBack, btn_back)
        header_sz = wx.BoxSizer(wx.HORIZONTAL)
        header_sz.Add(header, 0, wx.ALL | wx.EXPAND, 10)
        header_sz.AddStretchSpacer(1)
        header_sz.Add(btn_back, 0, wx.ALL, 10)

        font = wx.Font(30, wx.SWISS, wx.SLANT, wx.NORMAL)
        header.SetFont(font)
        header.SetForegroundColour('White')
        self.buttons = []

        self.sizer.Add(header_sz, 1, wx.EXPAND)

        text = wx.StaticText(
            self,
            label=("Hier kann die Tastenbelegung eingestellt werden. "
                   "Erlaubt sind alle alphanumerischen Werte (A-Z, 1-9). \n"
                   "Felder mit zwei Buttons können zwei verschiedene "
                   "Zuweisungen haben, es handelt sich NICHT um eine \n"
                   "Tastenkombination.")
        )
        text.SetForegroundColour('White')
        self.sizer.Add(
            text,
            0,
            wx.LEFT,
            border=10
        )

        buttons = [
            ["TOPLEFT", "Selects the top left node."],
            ["TOPCENTER", "Selects the top center node."],
            ["TOPRIGHT", "Selects the top right node."],
            ["MIDDLELEFT", "Selects the middle left node."],
            ["MIDDLERIGHT", "Selects the middle right node."],
            ["BOTTOMLEFT", "Selects the bottom left node."],
            ["BOTTOMCENTER", "Selects the bottom center node."],
            ["BOTTOMRIGHT", "Selects the bottom right node."],
            ["ROTLEFT", "Rotate the cube left."],
            ["ROTRIGHT", "Rotate the cube right."],
            ["ROTUP", "Rotate the cube up."],
            ["ROTDOWN", "Rotate the cube down."],
            ["ROTCLOCK", "Rotate the camera clockwise."],
            ["ROTCOUNTERCLOCK", "Rotate the camera counter-clockwise."],
        ]
        self.AddButtons(buttons)
        self.UpdateButtons()
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.SetSizerAndFit(self.sizer)
        self.Layout()

    def OnSize(self, event):
        size = self.GetSize()
        vsize = self.GetVirtualSize()
        self.SetVirtualSize((size[0], vsize[1]))

    def OnBack(self, event):
        self.ResetButtons()
        self.Hide()
        self.GetParent().settingsMenu.Show()

    def AddButton(self, function, description):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        txt_desc = wx.StaticText(
            self,
            label=description,
            style=wx.ALIGN_CENTER_VERTICAL,
        )
        txt_desc.SetForegroundColour("White")
        button_pn = KeyButton(self, function=function)
        for button in button_pn.GetButtons():
            self.buttons.append(button)
        hbox.Add(
            button_pn,
            0,
            wx.EXPAND | wx.ALL,
            border=10,
        )
        hbox.Add(
            txt_desc,
            1,
            wx.TOP,
            border=20
        )
        self.sizer.Add(hbox, 1, wx.EXPAND | wx.ALL, 10)

    def AddButtons(self, buttons):
        for button in buttons:
            self.AddButton(button[0], button[1])

    def UpdateButtons(self):
        duplicates = {}
        for button in self.buttons:
            key = button.GetLabelText()
            if key not in duplicates:
                duplicates[key] = [button]
            else:
                duplicates[key].append(button)

        for key, buttons in duplicates.iteritems():
            if len(buttons) > 1:
                for button in buttons:
                    button.SetBackgroundColour("red")
                    button.SetForegroundColour("white")
            else:
                for button in buttons:
                    button.SetBackgroundColour("white")
                    button.SetForegroundColour("black")

    def ResetButtons(self):
        print "yo"
        for button in self.buttons:
            button.GetParent().ResetButtons()


class KeyButton(wx.Panel):
    def __init__(self, parent, function=None):

        wx.Panel.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetBackgroundColour(self.GetParent().bg_color)

        self.function = function
        self.keys = config.parser.get("Controls", function).split(",")

        for key in self.keys:
            btn = wx.Button(self, size=(100, 50), label=key.upper())
            self.Bind(wx.EVT_BUTTON, self.OnPressed, btn)
            sizer.Add(btn, 0, wx.ALL, 5)

        self.edit_btn = None
        self.SetSizerAndFit(sizer)

    def OnPressed(self, event):
        self.GetParent().ResetButtons()
        btn = event.GetEventObject()
        self.edit_key = btn.GetLabelText()
        btn.SetLabel("Press key...")
        self.edit_btn = btn
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyPressed, btn)

    def OnKeyPressed(self, event):

        if self.edit_btn is None:
            return

        try:
            code = event.GetKeyCode()
            char = str(unichr(event.GetUniChar())).lower()

            if not char.isalnum():
                self.ResetButtons()
                return

            if code in [375, 331]:
                key = "7"

            elif code in [377, 332]:
                key = "8"

            elif code in [380, 333]:
                key = "9"

            elif code in [376, 328]:
                key = "4"

            elif code in [383, 329]:
                key = "5"

            elif code in [378, 330]:
                key = "6"

            elif code in [382, 325]:
                key = "1"

            elif code in [379, 326]:
                key = "2"

            elif code in [382, 327]:
                key = "3"

            else:
                key = char

        except:
            return

        self.edit_btn.SetLabel(key.upper())

        self.UpdateKeys()
        config.parser.set("Controls", self.function, ",".join(self.keys))
        config.write()
        self.GetParent().UpdateButtons()
        self.edit_btn = None

    def GetKeys(self):
        return self.keys

    def GetButtons(self):
        return self.GetChildren()

    def UpdateKeys(self):
        del self.keys
        self.keys = []

        for btn in self.GetButtons():
            self.keys.append(btn.GetLabelText().lower())

    def ResetButtons(self):
        if self.edit_btn:
            self.edit_btn.SetLabel(self.edit_key)
            self.edit_btn = None


class Credits(wx.Panel):

    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)

        header = wx.StaticText(self, -1, 'Demo Credits')
        font = wx.Font(30, wx.SWISS, wx.NORMAL, wx.NORMAL)
        header.SetFont(font)
        header.SetForegroundColour('White')


        vbox = wx.BoxSizer(wx.VERTICAL)

        self.btn_return = wx.Button(self, label='Return to Settings', size=(250, 50))
        vbox.Add(header, 1, wx.ALL, 10)
        vbox.Add(self.btn_return, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizerAndFit(vbox)
        self.Centre()

class Levelselection(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)

        gridSizer = wx.GridBagSizer(10, 10)

        sizer = wx.FlexGridSizer(6, 5, 20, 50)

        btn_bgcolor = wx.Colour(255,255,255)
        btn_fgcolor = wx.Colour(0,0,0)

        header = wx.StaticText(self, -1, 'Campaign')
        font = wx.Font(30, wx.SWISS, wx.NORMAL, wx.NORMAL)
        header.SetFont(font)
        header.SetForegroundColour('White')

        self.btn_level = []
        gridSizer.Add(header, pos=(0,0), span=(1,1), flag=wx.LEFT|wx.TOP, border=10)
        for x in range(0,20):
            self.btn_level.append(GB.GradientButton(self, label='Level ' + str(x+1), size=(100, 100)))
            sizer.Add(self.btn_level[x], 1, wx.EXPAND)

            self.btn_level[x].SetBottomEndColour(btn_bgcolor)
            self.btn_level[x].SetBottomStartColour(btn_bgcolor)
            self.btn_level[x].SetTopEndColour(btn_bgcolor)
            self.btn_level[x].SetTopStartColour(btn_bgcolor)
            self.btn_level[x].SetForegroundColour(btn_fgcolor)
            # self.btn_level[x].SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL,0))
            self.btn_level[x].SetPressedBottomColour(btn_bgcolor)
            self.btn_level[x].SetPressedTopColour(btn_bgcolor)

            if x > 3:
                self.btn_level[x].Enable(False)
                btn_bgcolor = wx.Colour(128,128,128)
                btn_fgcolor = wx.Colour(255,255,255)

        self.btn_return = wx.Button(self, label='Return to main menu', size=(50, 50))

        gridSizer.Add(sizer, pos=(2,0), span=(1,1), flag=wx.LEFT|wx.BOTTOM, border=10) 
        gridSizer.Add(self.btn_return, pos=(3,0), span=(1,1), flag=wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)    


        self.SetSizerAndFit(gridSizer)


class MyFrame(wx.Frame):

    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(800, 700))

        self.SetBackgroundColour((0, 0, 55))
        self.mainMenu = Main(self)
        self.settingsMenu = Settings(self)
        self.audioMenu = AudioSettings(self)
        self.keyMenu = Keymapping(self)
        self.credits = Credits(self)
        self.levelList = Levelselection(self)
        self.keyMenu.Hide()
        self.levelList.Hide()
        self.settingsMenu.Hide()
        self.audioMenu.Hide()
        self.credits.Hide()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.settingsMenu, 1)
        self.sizer.Add(self.audioMenu, 1)
        self.sizer.Add(self.keyMenu, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        # Eventbindings for the Buttons in the Main tab
        self.Bind(wx.EVT_BUTTON, self.OnCampaign, self.mainMenu.btn_main_menu)
        # Binding for the Endless Mode  TODO Implement Endlessmode
        # self.Bind(wx.EVT_BUTTON, self.OnEndless, self.mainMenu.btn_endless)
        self.Bind(wx.EVT_BUTTON, self.OnSettings, self.mainMenu.btn_controls)
        # Binding to resume the last saved game
        # self.Bind(wx.EVT_BUTTON, self.OnResumse, self.mainMenu.btn_resume)
        self.Bind(wx.EVT_BUTTON, self.OnQuit, self.mainMenu.btn_quit)

        # Eventbindings for the Buttons in the settings tab
        self.Bind(wx.EVT_BUTTON, self.OnAudio, self.settingsMenu.btn_audio)
        self.Bind(wx.EVT_BUTTON, self.OnControls, self.settingsMenu.btn_controls)
        self.Bind(wx.EVT_BUTTON, self.OnCredits, self.settingsMenu.btn_credits)
        self.Bind(wx.EVT_BUTTON, self.OnReturn, self.settingsMenu.btn_return)
        self.Bind(wx.EVT_BUTTON, self.OnReset, self.settingsMenu.btn_reset)

        # Eventbindings for the Buttons in the audio settings
        self.Bind(wx.EVT_BUTTON, self.OnSwitch, self.audioMenu.btn_music_switch)

        # Eventbinding for the Credits
        self.Bind(wx.EVT_BUTTON, self.OnQuitCredits, self.credits.btn_return)

        # Eventbinding for the Levelselection
        self.Bind(wx.EVT_BUTTON, self.OnReturnMain, self.levelList.btn_return)

    def OnCampaign(self, event):
        self.mainMenu.Hide()
        self.levelList.Show()

    def OnSettings(self, event):
        self.mainMenu.Hide()
        self.settingsMenu.Show()

    def OnQuit(self, event):
        self.Close()

    def OnSwitch(self, event):
        # if event.GetEventObject() is self.btn_credits:
        #   audio.play('../assets/music/OGG files/menu.ogg')
        # else:
        #    audio.stop()
        x = 1

    def OnReturn(self, event):
        self.settingsMenu.Hide()
        self.audioMenu.Hide()
        self.keyMenu.Hide()
        self.mainMenu.Show()

    def OnAudio(self, event):
        self.audioMenu.Show()
        self.keyMenu.Hide()

    def OnControls(self, event):
        self.keyMenu.Show()
        self.settingsMenu.Hide()
        self.Layout()
        self.Refresh()

    def OnCredits(self, event):
        self.settingsMenu.Hide()
        self.audioMenu.Hide()
        self.credits.Show()
        # audio.play('../assets/music/OGG files/credits.ogg') 

    def OnQuitCredits(self, event):
        self.credits.Hide()
        self.settingsMenu.Show()
        # audio.stop()
        # audio.play('../assets/music/OGG files/menu.ogg')

    def OnReset(self, event):
        dial = wx.MessageDialog(None, 'Erase your progress?', 'Question',
                                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        dial.ShowModal()

    def OnReturnMain(self, event):
        self.mainMenu.Show()
        self.levelList.Hide()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, title='Laserwurfel')
    frame.Show()
    # audio.play('../assets/music/OGG files/menu.ogg')
    # import wx.lib.inspection
    # wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
