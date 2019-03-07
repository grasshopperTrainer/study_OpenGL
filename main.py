# from prohopper import Screen
# from prohopper import Doodler as doo
from prohopper import *

sc = Screen();
sc.add_window()
@sc.event
def window1(dt):
    sc.set_framerate(30)
    draw.point(size=30)
    pass
sc.run()
