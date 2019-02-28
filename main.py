from prohopper import Screen
from prohopper import Doodler as doo

sc = Screen();
sc.add_window()
@sc.event
def window1(dt):
    sc.set_framerate(30)
    doo.point(size = 30)
    pass
sc.run()
