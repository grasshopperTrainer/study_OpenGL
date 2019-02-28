from glumpy import app
import doodler as do

class Screen:
    WINDOWS = {}

    @classmethod
    def __init__(cls):
        # inithialization of doodler
        cls.doo = do.Doodler()
        cls._framerate = 60
        print('___ Screen initialized')
        pass

    @classmethod
    def get_doodler(cls):
        return cls.doo

    @classmethod
    def add_window(cls, width: int = 500, height: int = 500, title: str = None, color: list = [1, 1, 1, 1]):

        # make title of the window
        if title is None:
            title = 'window' + str(len(cls.WINDOWS) + 1)
        else:
            title = title
        new_window = app.Window(width=width, height=height, title=title, color=color)

        # run default initiation
        @new_window.event
        def on_init():
            pass

        @new_window.event
        def on_resize(width: int, height: int):
            pass

        # insert window to the window dictionary(self.WINDOWS)
        cls.WINDOWS[title] = new_window
        print(f'___ new window {title} MADE')

    @classmethod
    def event(cls, func):
        # decorator for describing window actions
        window = object
        title = func.__name__
        try:
            window = cls.WINDOWS[title]
            print(f'___ add action to window{title}')

            @window.event
            def on_draw(dt):
                # push window into doodler
                # so Doodler function could retrive Window info
                do.Doodler.push_window(window)
                window.clear()
                func(dt)

            return on_draw
        except KeyError:
            print(f'___ unable to add action to "{title}"\n'
                  f'    no such window titled "{title}"')

    @classmethod
    def run(cls):
        # routine for every window
        # for window in Screen.WINDOWS.values():
        #     window
        app.run(framerate=cls._framerate)

    @classmethod
    def set_framerate(cls, framerate: int):
        cls._framerate = framerate
