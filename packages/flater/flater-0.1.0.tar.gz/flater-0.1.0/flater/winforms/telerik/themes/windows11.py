from flater.basic import Basic


class Windows11Theme(Basic):

    from Telerik.WinControls.Themes import Windows11Theme

    _type = Windows11Theme
    _name = "Windows11"

    def __init__(self):
        super().__init__()


class Windows11DarkTheme(Basic):

    from Telerik.WinControls.Themes import Windows11DarkTheme

    _type = Windows11DarkTheme
    _name = "Windows11Dark"

    def __init__(self):
        super().__init__()
