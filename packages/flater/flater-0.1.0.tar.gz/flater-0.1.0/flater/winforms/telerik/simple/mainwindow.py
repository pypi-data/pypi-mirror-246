from flater.winforms.telerik.simple.widget import Widget


class MainWindow(Widget):

    from flater.winforms.telerik.rad_form import RadForm

    _type = RadForm

    def __init__(self, master=None):
        super().__init__(master)
        from flater.winforms.application import Application
        from flater.winforms.telerik.themes.theme_resolution_service import ThemeResolutionService
        self.theme = None
        self.app = Application()
        self.theme_control = ThemeResolutionService()

    def add_to_titlebar_buttons(self, button: Widget):
        self._.AddToTitleBarButtons(button)

    def insert_to_titlebar_buttons(self, index: int, button: Widget):
        self._.InsertToTitleBarButtons(index, button)

    def create_control_spy_window(self):
        from flater.winforms.telerik.rad_control_spy_form import RadControlSpyForm
        self._control_spy = RadControlSpyForm()
        self._control_spy.Show()
        return self._control_spy

    def mainloop(self):
        self.app.Run(self._)

    def quit(self):
        self.app.Close(self._)

    def theme_names(self):
        return ["win11", "win11dark"]

    def theme_use(self, theme_name):
        if theme_name == "win11":
            from flater.winforms.telerik.themes.windows11 import Windows11Theme
            self.theme = Windows11Theme()
        elif theme_name == "win11dark":
            from flater.winforms.telerik.themes.windows11 import Windows11DarkTheme
            self.theme = Windows11DarkTheme()
        self.theme_control.ApplicationThemeName = self.theme

    def title(self, text: str = None):
        if text:
            self._.Text = text
        else:
            return self._.Text

