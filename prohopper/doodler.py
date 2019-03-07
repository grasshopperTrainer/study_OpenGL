import numpy as np
from glumpy import gloo
from tools import *

class Doodler:
    PROG_POINTS2D = None
    @classmethod
    def bake_shaders(cls):
        vertex = """
         uniform float size;

         attribute vec3 position;
         attribute vec4 color;

         varying vec3 v_position;
         varying vec4 v_color;

         void main() {
             v_position = position;
             v_color = color;
             gl_Position = vec4(position, 1);
             gl_PointSize = size;
         }
         """

        fragment = """
         varying vec3 v_position;
         varying vec4 v_color;
         uniform float size;

         float distance(vec2 P, vec2 center, float radius) {
             return length(P-center) - radius;
         }

         void main() {
             float d = distance(v_position.xy, vec2(0,0), size);
             if (d > 0) {
                 gl_FragColor = v_color;
             }   
         }
         """
        cls.PROG_POINTS2D = gloo.Program(vertex, fragment)

    def __init__(self):
        self.bake_shaders()
        print('___ Doodler initialized')

    # @classmethod
    # def remap2D_foreign(cls, coord: list):
    #     width = cls.CURRENTWINDOW.width
    #     height = cls.CURRENTWINDOW.height
    #     new_coord = cls.remap(coord, [[0, width], [0, height]], [0, 1])
    #     return new_coord
    #
    # @classmethod
    # def remap2D_native(cls, coord: list):
    #     width = cls.CURRENTWINDOW.width
    #     height = cls.CURRENTWINDOW.height
    #     new_coord = cls.remap(coord, [0, 1], [[0, width], [0, height]])
    #     return new_coord
    #
    # @classmethod
    # def remap_color(cls, color: list):
    #     return np.array(color) / 100
    #
    # @classmethod
    # def remap(cls, values: list, source: list = [0, 1], target: list = [0, 1]):
    #     new_lists = tls.list_longest(source, target)
    #
    #     source = new_lists[0];
    #     target = new_lists[1]
    #     print(source, target)
    #     source_dis = source[1] - source[0]
    #     target_dis = target[1] - target[0]
    #     result = [(i - source[0]) / source_dis * target_dis + target[0] for i in values]
    #     return result

    @property
    def windowwidth(self):
        return self.CURRENTWINDOW.width

    @property
    def windowheight(self):
        return self.CURRENTWINDOW.height

    def point(self, coord: list = [0, 0, 0], color: list = [1, 1, 1, 1], size: float = 10):
        area = rect.con_center(Point(*coord), size, size)

        window = rect.con_center(Point(), self.windowwidth, self.windowheight)
        # print(window.vertex())
        area_mapped = trans.rect_mapping(area, window, Rect())


    def set_antialize(self, level: int = 1, switch: bool = True):
        pass

    @classmethod
    def push_window(cls, window: object):
        # print('doodler: window pushed')
        cls.CURRENTWINDOW = window
        cls.WIN_SIZE = np.ndarray([cls.CURRENTWINDOW.width, cls.CURRENTWINDOW.height])

    def get_window(self):
        return self.CURRENTWINDOW
