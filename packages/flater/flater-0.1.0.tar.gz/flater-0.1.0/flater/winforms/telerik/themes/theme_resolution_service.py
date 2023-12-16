from flater.basic import Basic


def SetDefaultTheme(_ThemeName_Or_Theme):
    ThemeResolutionService().ApplicationThemeName = _ThemeName_Or_Theme


def GetDefaultTheme():
    return ThemeResolutionService().ApplicationThemeName


class ThemeResolutionService(Basic):
    from Telerik.WinControls import ThemeResolutionService

    _type = ThemeResolutionService

    def __init__(self):
        super().__init__()

    @property
    def ApplicationThemeName(self):
        return self._.ApplicationThemeName

    @ApplicationThemeName.setter
    def ApplicationThemeName(self, _ThemeName_Or_Theme):
        if isinstance(_ThemeName_Or_Theme, str):
            self._.ApplicationThemeName = _ThemeName_Or_Theme
        else:
            self._.ApplicationThemeName = _ThemeName_Or_Theme._name

    @property
    def SystemThemeName(self):
        return self._.SystemThemeName
