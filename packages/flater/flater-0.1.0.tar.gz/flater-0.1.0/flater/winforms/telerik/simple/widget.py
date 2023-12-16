from typing import Callable


class Widget(object):

    _type = None

    def __init__(self, master=None):
        self._ = self._type()
        self.master = master
        if master:
            self.master._.Add(self._)

    def on_click(self, func: Callable):
        self._.Bind("Click", func)

    def place(self, x=None, y=None, width=None, height=None):
        self.pos(x, y)
        self.size(width, height)

    def pos(self, x=None, y=None):
        if x is None and y is None:
            return self._.Pos
        else:
            if x is None:
                x = self._.Pos[0]
            elif y is None:
                y = self._.Pos[1]
            self._.Pos = (x, y)
            print(x, y)

    def size(self, width=None, height=None):
        if width is None and height is None:
            return self._.Size
        else:
            if width is None:
                width = self._.Size[0]
            elif height is None:
                height = self._.Size[1]
        self._.Size = (width, height)
