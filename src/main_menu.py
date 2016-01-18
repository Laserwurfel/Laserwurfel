import wx


class MyFrame(wx.Frame):

    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(500, 600))

        self.initUI()
        self.Centre()
        self.Show()

    def initUI(self):
        box = wx.BoxSizer(wx.VERTICAL)

        gs = wx.GridSizer(4, 1, 5, 5)

        btn_main_menu = wx.Button(self, -1, 'Main Menu')
        btn_endless = wx.Button(self, -1, 'Endless Mode')
        btn_controls = wx.Button(self, -1, 'Controls')
        btn_credits = wx.Button(self, -1, 'Credits')

        gs.AddMany([
            (btn_main_menu, 0, wx.EXPAND),
            (btn_endless, 0, wx.EXPAND),
            (btn_controls, 0, wx.EXPAND),
            (btn_credits, 0, wx.EXPAND)
        ])

        box.Add(gs, 1, wx.EXPAND)
        self.SetSizer(box)

if __name__ == '__main__':
    app = wx.App()
    MyFrame(None, title='Laserwurfel')
    app.MainLoop()
