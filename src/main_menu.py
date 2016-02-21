import wx
import wx.lib.agw.gradientbutton as gb



class MyFrame(wx.Frame):

    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(600, 600))

        self.createMain()
        self.Center()
        self.Show()

        #audio.play('../assets/music/OGG files/menu.ogg')

    def createMain(self):

        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(5, 4)

        self.btn_main_menu = gb.GradientButton(panel, -1, label='Campaign', size=(250, 20))
        self.btn_endless = gb.GradientButton(panel, -1, label='Endless', size=(250, 20))
        self.btn_controls = gb.GradientButton(panel, -1, label='Settings', size=(250, 20))
        self.btn_resume = gb.GradientButton(panel, -1, label='Resume last saved game', size=(250, 20))
        self.btn_quit = gb.GradientButton(panel, -1, label='Quit', size=(250, 20))

        #self.btn_main_menu.SetTopStartColour('blue') 


        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn_main_menu)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn_endless)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn_controls)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn_resume)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn_quit)

        sizer.Add(self.btn_main_menu, pos=(0,0), span=(1,3), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)
        sizer.Add(self.btn_endless, pos = (1,0), span=(1,3), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)
        sizer.Add(self.btn_controls, pos = (2,0), span=(1,3), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)
        sizer.Add(self.btn_resume, pos = (3,0), span=(1,3), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)
        sizer.Add(self.btn_quit, pos = (4,0), span=(1,3), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=10)

        sizer.AddGrowableRow(0)
        sizer.AddGrowableRow(1)
        sizer.AddGrowableRow(2)
        sizer.AddGrowableRow(3)
        sizer.AddGrowableRow(4)

        panel.SetSizerAndFit(sizer)

    def createOptions(self):
        box = wx.BoxSizer(wx.VERTICAL)

        gs = wx.GridSizer(3, 1, 5, 5)

        self.btn_audio = wx.Button(self, -1, 'Audio')
        self.btn_controls  = wx.Button(self, -1, 'Controls')
        self.btn_reset = wx.Button(self, -1, 'Reset Game')

        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn_audio)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn_controls)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn_reset)

        gs.AddMany([
            (self.btn_audio, 0, wx.EXPAND),
            (self.btn_controls, 0, wx.EXPAND),
            (self.btn_reset, 0, wx.EXPAND)
        ])

        box.Add(gs, 1, wx.EXPAND)
        self.SetSizer(box)

    def OnButton(self, event):
     #   if event.GetEventObject() is self.btn_credits:
      #      audio.play('../assets/music/OGG files/credits.ogg')
       # else:
        #    audio.stop()
        x = 1


if __name__ == '__main__':
    app = wx.App()
    MyFrame(None, title='Laserwurfel')
    app.MainLoop()
