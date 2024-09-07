import cairo
import math
import gi
import random
from numpy import linspace

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

# ~~edit me~~
#canvas "width" and "height"
width = 400
height = 400
#length of long notch
long_notch = 2.4
#length of short notch
short_notch = 2.2
#how often notches should show up
notch_interval = 25
#you know what this does
font_size = 30
#speedometer range (lowest speed, highest speed)
bounds = [0, 100]
#current speed of car (will change to can data later i guess)
current_speed = 30

#don't edit me
width_center = width / 2
height_center = height / 2
degree_offset = bounds[1] / 6
#for now, just assume number of notches is the highest speed
notch_count = bounds[1]


class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title = "Speedometer")

        self.darea = Gtk.DrawingArea()
        self.darea.connect("draw", self.on_draw)
        self.add(self.darea)
        GLib.timeout_add(10, self.interval)

    # def connect_darea(self):
    #     n = random.randint(0, 100)
    #     self.darea.connect("draw", self.on_draw, n)
    #     print(n)
    #     self.darea.queue_draw()
    #     self.darea.disconnect(self.darea)

    def interval(self):
        self.darea.queue_draw()
        GLib.timeout_add(10, self.interval)
        
    # def start_drawing(self):
    #     GLib.timeout_add(10, self.connect_darea)
        
            

    def on_draw(self, wid, cr):
        global current_speed
        current_speed = random.randint(0, 100)   
        #font settings
        cr.select_font_face("Courier", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(font_size)

        #draw outer circle
        cr.set_source_rgb(255, 255, 255)
        cr.arc((width / 2), (height / 2), (height / 2), 0, (2 * math.pi))
        cr.set_source_rgb(0, 0, 0)
        cr.fill_preserve()
        cr.set_source_rgb(255, 255, 255)
        cr.stroke()

        #draw inner circle
        cr.arc((width / 2), (height / 2), (height / 5), 0, (2 * math.pi))
        cr.stroke()

        #draw notches + notch text
        for notch_num, i in enumerate(linspace(bounds[0] - degree_offset, bounds[1] + degree_offset, num = notch_count)):
            cr.set_source_rgb(255, 255, 255)
            x, y = get_coordinates_from_speed(i, bounds)
            cr.move_to((x * width_center) + width_center, (y * -height_center) + height_center)    # set start position along circle
            #set end position based on whether notch should be long
            if (notch_num + 1) % notch_interval == 0 or notch_num == 0:    # long notch + text
                cr.set_line_width(3)
                cr.line_to(x * (width / long_notch) + width_center, y * (height / -long_notch) + height_center)
                cr.stroke()

                cr.set_source_rgb(255, 0, 0)
                cr.move_to(x * (width / long_notch) + width_center, y * (height / -long_notch) + height_center)
                cr.show_text(f"{notch_num}")
                cr.stroke()
            else:    # short notch
                cr.set_line_width(1)
                cr.line_to(x * (width / short_notch) + width_center, y * (height / -short_notch) + height_center)
                cr.stroke()
            
        #draw speed text
        cr.set_source_rgb(255, 0, 0)
        #that three should be character count
        #idk it doesn't center anyway lmao
        cr.move_to(width_center - (3 * font_size / 4), height_center + (font_size / 4))
        cr.show_text(str(current_speed))
        cr.stroke()

        #draw arc
        cr.set_source_rgb(255, 255, 0)
        cr.arc(width_center, height_center, height / 2.1, ((5 * math.pi) / 6), speed_to_angle(current_speed, bounds))
        cr.stroke()  

           

        
        #self.disconnect_by_func(self.on_draw)

    # def kys(self):
    #     print("k y and s")
    #     GLib.timeout_add(100, self.kys())


        
#given speed and boundaries (lowest speed at angle pi and highest speed at angle 0), output speedometer coordinates
#coordinates have a domain and range of [0, 1] so transformations can be easily applied later
def get_coordinates_from_speed(speed: int, bounds: tuple[int, int]):
    modifier = bounds[1] / math.pi
    midpoint = (bounds[0] + bounds[1]) / 2
    return (math.sin((speed - midpoint) / modifier), math.cos((speed - midpoint) / modifier))



def speed_to_angle(speed: int, bounds: tuple[int, int]): #outputs in radians
    angle_range = 240
    scalar = bounds[1] - bounds[0]
    return ((5 * math.pi) / 6) + (((angle_range / scalar) * speed) * (math.pi / 180))

print(speed_to_angle(50, bounds))

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
# win.kys()
# win.start_drawing()
Gtk.main()