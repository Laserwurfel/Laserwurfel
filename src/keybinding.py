#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import config


def get_acctable(actions, self):

    items = config.parser.items("Controls")
    print items
    keys = {}

    i = 5001
    for action in actions:
        for item in items:
            if item[0] == action[0]:
                key_chars = item[1].split(",")

        key_codes = []
        for char in key_chars:
            if char.startswith("NP_"):
                if char == "NP_7":
                    key = [375, 331]

                elif char == "NP_8":
                    key = [377, 332]

                elif char == "NP_9":
                    key = [380, 333]

                elif char == "NP_4":
                    key = [376, 328]

                elif char == "NP_5":
                    key = [383, 329]

                elif char == "NP_6":
                    key = [378, 330]

                elif char == "NP_1":
                    key = [382, 325]

                elif char == "NP_2":
                    key = [379, 326]

                elif char == "NP_3":
                    key = [382, 327]
            else:
                key = [ord(char)]

            key_codes.append(key)

        keys[action[0]] = [key_codes, i, action[1]]
        i += 1

    table_contents = []
    for action, values in keys.iteritems():
        self.Bind(wx.EVT_MENU, values[2], id=values[1])
        for key_codes in values[0]:
            for key_code in key_codes:
                table_contents.append(
                    (wx.ACCEL_NORMAL, key_code, values[1])
                )

    print table_contents
    acctable = wx.AcceleratorTable(table_contents)
    return acctable


class TestPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, size=(300, 300))

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)

        actions = [
            ["topleft", self.OnTopLeft],
            ["topcenter", self.OnTopCenter],
            ["topright", self.OnTopRight],
            ["middleleft", self.OnMiddleLeft],
            ["middleright", self.OnMiddleRight],
            ["bottomleft", self.OnBottomLeft],
            ["bottomcenter", self.OnBottomCenter],
            ["bottomright", self.OnBottomRight],
            ["rotleft", self.OnRotLeft],
            ["rotright", self.OnRotRight],
            ["rotup", self.OnRotUp],
            ["rotdown", self.OnRotDown],
            ["rotclock", self.OnRotClock],
            ["rotcounterclock", self.OnRotCounterClock]
        ]

        # FIXME: Why doesn't anything work?
        # acctable = get_acctable(actions, self)
        self.Bind(wx.EVT_MENU, self.OnTopLeft, id=5001)
        acctable = wx.AcceleratorTable([
            (wx.ACCEL_NORMAL, ord('t'), 5001)
        ])
        self.SetAcceleratorTable(acctable)
        self.SetFocus()

    def OnTopLeft(self, event):
        print "OnTopLeft"

    def OnTopCenter(self, event):
        print "OnTopCenter"

    def OnTopRight(self, event):
        print "OnTopRight"

    def OnMiddleLeft(self, event):
        print "OnMiddleLeft"

    def OnMiddleRight(self, event):
        print "OnMiddleRight"

    def OnBottomLeft(self, event):
        print "OnBottomLeft"

    def OnBottomCenter(self, event):
        print "OnBottomCenter"

    def OnBottomRight(self, event):
        print "OnBottomRight"

    def OnRotLeft(self, event):
        print "OnRotLeft"

    def OnRotRight(self, event):
        print "OnRotRight"

    def OnRotUp(self, event):
        print "OnRotUp"

    def OnRotDown(self, event):
        print "OnRotDown"

    def OnRotClock(self, event):
        print "OnRotClock"

    def OnRotCounterClock(self, event):
        print "OnRotCounterClock"

    def OnLeftDown(self, event):
        print "OnLeftDown"

    def OnRightDown(self, event):
        print "OnRightDown"

    def OnMouseMotion(self, event):
        if not event.LeftIsDown():
            return

        print "OnMouseMotion"
