""" Captures a list of points which typically represents a mouse path which
is decoded as a stroke or gesture.

Algorithm was originally created by me on 2005/06/25 in APR_StrogesturekeDecoder.m
for Objective-C drawing program.

Changed it slightly to remove the sqrt(). Ignoring the debug grid, it now 
avoids the use of floats or divides making it faster in other languages.

Anthony Reinberger
(c) Copyright 2022

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

class Stroke:
    """ Captures a list of points which typically represents a mouse path which
    is decoded as a stroke or gesture.

    Based on the following grid, a path can be represented as a number.

                 1  |  2  |  3
               -----------------
                 4  |  5  |  6
               -----------------
                 7  |  8  |  9

    Quadrant 5 is actually a circle/ellipse which overlaps the others.
    This simplifies the math and makes transitions from the corners to the
    centre clean, reducing the risk of hitting 2, 4, 6 or 8 along the way.
    """
    def __init__(self):
        self.is_stroking = False
        self.debug_grid = None
        self.path = []
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0

    def start_path(self, point_x: int, point_y: int):
        """ Call this with a mouse down event while providing the mouse position.
        Could use special button or modifier key trigger as well.
        """
        self.is_stroking = True
        self.debug_grid = None
        self.path = [(point_x, point_y)]
        # Initializing the min and max values with the first point.
        self.min_x = point_x
        self.min_y = point_y
        self.max_x = point_x
        self.max_y = point_y

    def append_path(self, point_x: int, point_y: int):
        """ Call this with a mouse moved event while providing the mouse position."""
        if not self.is_stroking:
            return  # Method shouldn't have been called but if it was, return early.
        self.path.append((point_x, point_y))
        # Updating the min and max values now will save looping through the path later.
        if point_x < self.min_x:
            self.min_x = point_x
        if point_x > self.max_x:
            self.max_x = point_x
        if point_y < self.min_y:
            self.min_y = point_y
        if point_y > self.max_y:
            self.max_y = point_y

    def decode_path(self) -> int:
        """ Call this with a mouse up event or mouse leave event.
        """
        if not self.is_stroking:
            return 0  # Method shouldn't have been called but if it was, return early.
        self.is_stroking = False
        centre_x = (self.min_x+self.max_x) >> 1  # Integer divide by 2.
        centre_y = (self.min_y+self.max_y) >> 1  # Integer divide by 2.
        width = 1+self.max_x-self.min_x  # 1 added to account for straight lines.
        height = 1+self.max_y-self.min_y  # 1 added to account for straight lines.
        # Improve single line detection by limiting width:height ratios.
        if 4*width < height:
            width = height
        if 4*height < width:
            height = width
        # A scale_factor of 6 causes the squares to be proportional
        # when using +/-width and +/-height limits.
        # Smaller numbers will widen the middle column.
        # Larger numbers will narrow the middle column.
        scale_factor = 6  # All grid squares are equal size with a value of 6.
        radius_factor = 2  # Should be between 1.4142 and 3 AKA scale_factor/2
        previous_quadrant = 0
        stroke = 0
        for point_x, point_y in self.path:
            spoint_x = scale_factor*(point_x-centre_x)
            spoint_y = scale_factor*(point_y-centre_y)
            quadrant = 5  # Quadrant 5 is a circle at the centre which overlaps the others.
            # Use 64 bit integer math in other languages here.
            if (height*spoint_x)**2+(width*spoint_y)**2 >= (width*height*radius_factor)**2:
                if spoint_x < -width:
                    quadrant -= 1
                if spoint_x > width:
                    quadrant += 1
                if spoint_y < -height:
                    quadrant -= 3  # Positive sign for bottom origin systems.
                if spoint_y > height:
                    quadrant += 3  # Negative sign for bottom origin systems.
            if quadrant != previous_quadrant:
                previous_quadrant = quadrant
                # Other languages should make sure the stroke value doesn't overflow.
                stroke = stroke*10 + quadrant
        self._make_debug_grid((centre_x, centre_y), (width, height), scale_factor, radius_factor)
        return stroke

    def _make_debug_grid(self, point, rect, scale_factor, radius_factor):
        """ Creates the reference grid for testing or training."""
        centre_x, centre_y = point
        width, height = rect
        hline_1 = (centre_x-width/2, centre_y-height/scale_factor,
                   centre_x+width/2, centre_y-height/scale_factor)
        hline_2 = (centre_x-width/2, centre_y+height/scale_factor,
                   centre_x+width/2, centre_y+height/scale_factor)
        vline_1 = (centre_x-width/scale_factor, centre_y+height/2,
                   centre_x-width/scale_factor, centre_y-height/2)
        vline_2 = (centre_x+width/scale_factor, centre_y+height/2,
                   centre_x+width/scale_factor, centre_y-height/2)
        x_radius = width*radius_factor/scale_factor
        y_radius = height*radius_factor/scale_factor
        ellipse = (centre_x-x_radius, centre_y-y_radius, x_radius*2, y_radius*2)
        self.debug_grid = (hline_1, hline_2, vline_1, vline_2, ellipse)

    def get_debug_grid(self) -> tuple:
        """ Return the reference grid for testing or training.
        It consists of points for two horizontal lines, two vertical lines
        and centre, width and height for an ellipse identifying coordinate 5.
        """
        return self.debug_grid
