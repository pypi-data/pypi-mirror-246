from flater.winforms.control import Control


class RadControl(Control):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def ThemeName(self):
        return self._.ThemeName

    @ThemeName.setter
    def ThemeName(self, Name: str):
        self._.ThemeName = Name
