from flater.basic import Basic


class Form(Basic):

    from System.Windows.Forms import Form

    _type = Form

    def __init__(self):
        super().__init__()

        self._app = None

    def Close(self):
        self._.Close()

    def AppRun(self):
        from flater.winforms.application import Application
        self._app = Application()
        self._app.Run(self)

    def AppClose(self):
        if self._app:
            self._app.Close()
