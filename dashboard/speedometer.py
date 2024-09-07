import cairo
import math
import gi
from numpy import linspace

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

width = 400
height = 400

bounds = [0, 100]
degree_offset = bounds[1] / 6
notch_interval = bounds[1]

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title = "Speedometer")

        self.darea = Gtk.DrawingArea()
        self.darea.connect("draw", self.on_draw)
        self.add(self.darea)

    def on_draw(self, wid, cr):
        #draw circle
        cr.set_source_rgb(255, 255, 255)
        cr.arc((width / 2), (height / 2), (height / 2), 0, (2 * math.pi))
        cr.set_source_rgb(0, 0, 0)
        cr.fill_preserve()
        cr.set_source_rgb(255, 255, 255)

        #draw notches
        for notch_num, i in enumerate(linspace(bounds[0] - degree_offset, bounds[1] + degree_offset, num = notch_interval)):
            coords = get_coordinates_from_speed(i, bounds)
            cr.move_to(coords[0] * (width / 2) + (width / 2), coords[1] * (height / -2) + (height / 2))
            if (notch_num + 1) % 25 == 0 or notch_num == 0: 
                cr.line_to(coords[0] * (width / 3) + (width / 2), coords[1] * (height / -3) + (height / 2))
            else:
                cr.line_to(coords[0] * (width / 2.5) + (width / 2), coords[1] * (height / -2.5) + (height / 2))

        #finalize draw
        cr.stroke()

#given speed and boundaries (lowest speed at angle pi and highest speed at angle 0), output speedometer coordinates
def get_coordinates_from_speed(speed: int, bounds: tuple[int, int]):
    modifier = bounds[1] / math.pi
    midpoint = (bounds[0] + bounds[1]) / 2
    return (math.sin((speed - midpoint) / modifier), math.cos((speed - midpoint) / modifier))




win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()