#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
#import audio
import config


class Main(wx.Panel):

    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)
        sizer = wx.GridBagSizer(20, 20)

        header = wx.StaticText(self, -1, 'LASERWURFEL')
        font = wx.Font(35, wx.SWISS, wx.SLANT, wx.NORMAL)
        header.SetFont(font)
        header.SetForegroundColour('White')

        self.btn_main_menu = wx.Button(self, label='Campaign', size=(250, 50))
        self.btn_endless = wx.Button(self, label='Endless', size=(250, 50))
        self.btn_controls = wx.Button(self, label='Settings', size=(250, 50))
        self.btn_resume = wx.Button(self, label='Resume last saved game', size=(250, 50))
        self.btn_quit = wx.Button(self, label='Quit', size=(250, 50))

        sizer.Add(header, pos=(0,0), span=(1,5), flag=wx.LEFT|wx.TOP, border=10)
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


class Settings(wx.Panel):

    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)
        sizer = wx.GridBagSizer(20, 20)

        header = wx.StaticText(self, -1, 'Settings')
        font = wx.Font(30, wx.SWISS, wx.SLANT, wx.NORMAL)
        header.SetFont(font)
        header.SetForegroundColour('White')


        self.btn_audio = wx.Button(self, label='Audio', size=(250, 50))
        self.btn_controls = wx.Button(self, label='Controls', size=(250, 50))
        self.btn_reset = wx.Button(self, label='Reset Game', size=(250, 50))
        self.btn_credits = wx.Button(self, label='Credits', size=(250, 50))
        self.btn_return = wx.Button(self, label='Return to main menu', size=(250, 50))

        sizer.Add(header, pos=(0,0), span=(1,5), flag=wx.LEFT|wx.TOP, border=10)
        sizer.Add(self.btn_audio, pos=(1,0), span=(1,2), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)
        sizer.Add(self.btn_controls, pos = (2,0), span=(1,2), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)
        sizer.Add(self.btn_reset, pos = (3,0), span=(1,2), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)
        sizer.Add(self.btn_credits, pos = (4,0), span=(1,2), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)
        sizer.Add(self.btn_return, pos = (5,0), span=(1,2), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)

        sizer.AddGrowableRow(0)
        sizer.AddGrowableRow(1)
        sizer.AddGrowableRow(2)
        sizer.AddGrowableRow(3)
        sizer.AddGrowableRow(4)


        self.SetSizerAndFit(sizer) 

class AudioSettings(wx.Panel):

    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        header = wx.StaticText(self, -1, 'Audio')
        font = wx.Font(30, wx.SWISS, wx.SLANT, wx.NORMAL)
        header.SetFont(font)
        header.SetForegroundColour('White')


        volume = wx.StaticText(self, label="Volume")
        music = wx.StaticText(self, label="Music")
        volume.SetForegroundColour('White')
        music.SetForegroundColour('White')


        self.volumeSlider = wx.Slider(self, -1, 100, 0, 100,
            style = wx.SL_HORIZONTAL)
        self.btn_musicSwitch = wx.Button(self, label='Turn Music Off', size=(250,50))

        vbox.Add(header, 1, wx.ALL, 10)
        vbox.Add(volume, 1, wx.ALL, 2)
        vbox.Add(self.volumeSlider, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(music, 1, wx.ALL, 2)
        vbox.Add(self.btn_musicSwitch, 1, wx.EXPAND | wx.ALL, 2)

        self.SetSizerAndFit(vbox)


# TODO: Add support for multiple key bindings
class Keymapping(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundColour(((0, 0, 55)))

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        header = wx.StaticText(self, -1, 'Controls')
        font = wx.Font(30, wx.SWISS, wx.SLANT, wx.NORMAL)
        header.SetFont(font)
        header.SetForegroundColour('White')
        self.buttons = []

        self.sizer.Add(header, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)

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

        self.SetSizerAndFit(self.sizer)

    def AddButton(self, function, description):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        txt_desc = wx.StaticText(
            self,
            label=description,
            style=wx.ALIGN_CENTER_VERTICAL,
        )
        txt_desc.SetForegroundColour("White")
        button = KeyButton(self, function=function)
        self.buttons.append(button)
        hbox.Add(
            button,
            0,
            wx.EXPAND | wx.ALL,
            border=10,
        )
        hbox.Add(
            txt_desc,
            1,
        )
        self.sizer.Add(hbox, 1, wx.EXPAND | wx.ALL, 10)

    def AddButtons(self, buttons):
        for button in buttons:
            self.AddButton(button[0], button[1])

    def UpdateButtons(self):
        duplicates = {}
        for button in self.buttons:
            key = button.GetKey()
            if key not in duplicates:
                duplicates[key] = [button]
            else:
                duplicates[key].append(button)

        for key, buttons in duplicates.iteritems():
            if len(buttons) > 1:
                for button in buttons:
                    button.SetBackgroundColour("red")
            else:
                for button in buttons:
                    button.SetBackgroundColour("white")


class KeyButton(wx.Button):
    def __init__(self, parent, size=(100, 50), function=None):
        wx.Button.__init__(self, parent=parent, size=size)

        self.function = function
        self.key = config.parser.get("Controls", function)
        self.SetLabel(self.key)
        self.changing_key = False

        self.Bind(wx.EVT_BUTTON, self.OnPressed)

    def OnPressed(self, event):
        self.SetLabel("Press key...")
        self.changing_key = True
        self.Bind(wx.EVT_CHAR, self.OnKeyPressed)

    def OnKeyPressed(self, event):
        if not self.changing_key:
            return

        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.changing_key = False
            self.SetLabel(self.key)
            return

        try:
            self.key = str(chr(event.GetUniChar())).upper()
        except:
            return

        self.GetParent().UpdateButtons()

        self.SetLabel(self.key)
        config.parser.set("Controls", self.function, self.key)
        config.write()
        self.changing_key = False

    def GetKey(self):
        return self.key


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

        header = wx.StaticText(self, -1, 'Campaign')
        font = wx.Font(30, wx.SWISS, wx.NORMAL, wx.NORMAL)
        header.SetFont(font)
        header.SetForegroundColour('White')

        self.btn_level = []
        gridSizer.Add(header, pos=(0,0), span=(1,1), flag=wx.LEFT|wx.TOP, border=10)
        for x in range(0,20):
            self.btn_level.append(wx.Button(self, label='Level ' + str(x+1), size=(100, 100)))
            sizer.Add(self.btn_level[x], 1, wx.EXPAND)
            if x > 3:
                self.btn_level[x].Enable(False)

        self.btn_return = wx.Button(self, label='Return to main menu', size=(50, 50))

        gridSizer.Add(sizer, pos=(2,0), span=(1,1), flag=wx.LEFT|wx.BOTTOM, border=10) 
        gridSizer.Add(self.btn_return, pos=(3,0), span=(1,1), flag=wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)    


        self.SetSizerAndFit(gridSizer)



class MyFrame(wx.Frame):

    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(800, 700))

        self.panel = wx.Panel(self, wx.ID_ANY)
        self.panel.SetBackgroundColour(((0,0,55)))
        self.SetBackgroundColour((0,0,55))

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

        self.sizer = wx.GridSizer(1, 2, 5, 5)
        self.sizer.Add(self.settingsMenu, 1)
        self.sizer.Add(self.audioMenu, 1)
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
        self.Bind(wx.EVT_BUTTON, self.OnSwitch, self.audioMenu.btn_musicSwitch)

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
        #if event.GetEventObject() is self.btn_credits:
        #   audio.play('../assets/music/OGG files/menu.ogg')
        #else:
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

    def OnCredits(self, event):
        self.settingsMenu.Hide()
        self.audioMenu.Hide()
        self.credits.Show()
        #audio.play('../assets/music/OGG files/credits.ogg') 

    def OnQuitCredits(self, event):
        self.credits.Hide()
        self.settingsMenu.Show()
        #audio.stop()
        #audio.play('../assets/music/OGG files/menu.ogg')

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
    #audio.play('../assets/music/OGG files/menu.ogg')
    app.MainLoop()
