#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx


class TestFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1280, 720))
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel = PauseMenu(self)
        sizer.Add(panel, 1, wx.EXPAND)

        self.Layout()
        self.Show(True)


class PauseMenu(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        sz_buttons = wx.BoxSizer(wx.HORIZONTAL)

        # Text
        self.txt_level = wx.StaticText(
            self,
            label="Level ",
        )
        sizer.Add(
            self.txt_level,
            2,
            wx.ALL | wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL,
            border=10
        )
        self.txt_time = wx.StaticText(
            self,
            label="Time played: "
        )
        sizer.Add(
            self.txt_time,
            2,
            wx.ALL | wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL,
            border=10
        )

        # Empty
        sizer.Add(wx.Panel(self), 3)

        # Buttons
        btn_quit = wx.Button(
            self,
            label="Quit",
        )
        sz_buttons.Add(btn_quit, 1)
        btn_main_menu = wx.Button(
            self,
            label="Main menu",
        )
        sz_buttons.Add(btn_main_menu, 1)
        btn_levels = wx.Button(
            self,
            label="Levels",
        )
        sz_buttons.Add(btn_levels, 1)
        btn_resume = wx.Button(
            self,
            label="Resume",
        )
        sz_buttons.Add(btn_resume, 1)
        sizer.Add(
            sz_buttons,
            2,
            wx.ALL | wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL,
            border=10
        )

app = wx.App(False)
frame = TestFrame(None, "Test Frame")
app.MainLoop()
