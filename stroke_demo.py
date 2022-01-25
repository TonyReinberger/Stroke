#!/usr/bin/env python3
""" Creates a simple GUI to demonstrate and test the stroke algorithm."""
import wx
import stroke
import stroke_decode

class MyFrame(wx.Frame):
    """ Top window for stroke demo."""
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((400, 300))
        self.SetTitle("Stroke Demo")
        self.panel = wx.Panel(self, wx.ID_ANY)
        sizer = wx.StaticBoxSizer(wx.StaticBox(self.panel, wx.ID_ANY, ""), wx.VERTICAL)
        sizer.Add((20, 20), 1, 0, 0)
        self.text_ctrl_stroke = wx.TextCtrl(self.panel, wx.ID_ANY, "")
        sizer.Add(self.text_ctrl_stroke, 0, wx.EXPAND, 0)
        self.panel.SetSizer(sizer)
        self.Layout()

        self.panel.Bind(wx.EVT_MOUSE_EVENTS, self._handle_mouse_events)
        self.Bind(wx.EVT_PAINT, self._handle_paint)
        self.stroke = stroke.Stroke()  # Stroke class for capture and decoding.
        self.points = []  # Saves points for drawing. Initialize for first use.

    def _handle_mouse_events(self, event):
        """ Use various mouse events to start, trace and finish a stroke path. """
        event_type = event.GetEventType()
        if event_type == wx.EVT_LEFT_DOWN.evtType[0]:
            point_x, point_y = event.GetPosition().Get()
            self.points = [wx.Point(point_x, point_y)]  # Initialize points for drawing.
            self.stroke.start_path(point_x, point_y)  # Initialize stroke path.
            self.Refresh()  # Clear the lines since there's no points to plot.
        if self.stroke.is_stroking:
            if event_type == wx.EVT_MOTION.evtType[0]:
                point_x, point_y = event.GetPosition().Get()
                self.points.append(wx.Point(point_x, point_y))  # Add point to draw lines.
                self.stroke.append_path(point_x, point_y)  # Add the position to the stroke path.
                self.Refresh()  # Update the window with the path lines.
            if event_type in (wx.EVT_LEAVE_WINDOW.evtType[0], wx.EVT_LEFT_UP.evtType[0]):
                stroke_code = self.stroke.decode_path()  # Decode the path and display it.
                stroke_name = stroke_decode.name(stroke_code)
                self.text_ctrl_stroke.SetValue(f"{stroke_code}: {stroke_name}")
                self.Refresh()  # Update the window to add the grid if there is one.
        event.Skip()

    def _handle_paint(self, event):
        """ Draw a line showing the mouse path and add points to the line ends.
        A boundary grid may have been created to draw as well.
        """
        paint_dc = wx.PaintDC(self)
        if len(self.points) > 1:
            paint_dc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 5))
            paint_dc.DrawLines(self.points)
            paint_dc.SetPen(wx.Pen(wx.Colour(255, 255, 255), 1))
            paint_dc.DrawPointList(self.points)
        grid = self.stroke.get_debug_grid()
        if grid:
            paint_dc.SetPen(wx.Pen(wx.Colour(255, 0, 0), 1))
            paint_dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0), wx.BRUSHSTYLE_TRANSPARENT))
            for index, (cord_1, cord_2, cord_3, cord_4) in enumerate(grid):
                if index == 4:
                    paint_dc.DrawEllipse(int(cord_1), int(cord_2), int(cord_3), int(cord_4))
                else:
                    paint_dc.DrawLine(int(cord_1), int(cord_2), int(cord_3), int(cord_4))
        event.Skip()

class MyApp(wx.App):
    """ Application for stroke demo."""
    def OnInit(self):
        """ Instantiate and show top window."""
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
