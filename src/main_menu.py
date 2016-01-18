import wx

import audio


class MyFrame(wx.Frame):

    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(500, 600))

        self.initUI()
        self.Centre()
        self.Show()

        audio.play('../assets/music/OGG files/menu.ogg')

    def initUI(self):
        box = wx.BoxSizer(wx.VERTICAL)

        gs = wx.GridSizer(4, 1, 5, 5)

        self.btn_main_menu = wx.Button(self, -1, 'Main Menu')
        self.btn_endless = wx.Button(self, -1, 'Endless Mode')
        self.btn_controls = wx.Button(self, -1, 'Settings')
        self.btn_credits = wx.Button(self, -1, 'Credits')

        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn_main_menu)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn_endless)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn_controls)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn_credits)

        gs.AddMany([
            (self.btn_main_menu, 0, wx.EXPAND),
            (self.btn_endless, 0, wx.EXPAND),
            (self.btn_controls, 0, wx.EXPAND),
            (self.btn_credits, 0, wx.EXPAND)
        ])

        box.Add(gs, 1, wx.EXPAND)
        self.SetSizer(box)

    def OnButton(self, event):
        if event.GetEventObject() is self.btn_credits:
            audio.play('../assets/music/OGG files/credits.ogg')
        else:
            audio.stop()


if __name__ == '__main__':
    app = wx.App()
    MyFrame(None, title='Laserwurfel')
    app.MainLoop()
