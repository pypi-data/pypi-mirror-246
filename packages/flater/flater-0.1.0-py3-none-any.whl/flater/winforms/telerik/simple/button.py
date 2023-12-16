from flater.winforms.telerik.simple.widget import Widget


class Button(Widget):
    from flater.winforms.telerik.rad_button import RadButton

    _type = RadButton

    def __init__(self, *args, text: str = "", **kwargs):
        super().__init__(*args, **kwargs)

        self.configure(text=text)

    def configure(self, **kwargs):
        if "text" in kwargs:
            self._.Text = kwargs.pop("text")
