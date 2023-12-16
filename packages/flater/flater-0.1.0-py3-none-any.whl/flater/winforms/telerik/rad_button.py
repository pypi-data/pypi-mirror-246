from flater.winforms.telerik.rad_control import RadControl
from flater.winforms.button import Button


class RadButton(RadControl, Button):

    from Telerik.WinControls.UI import RadButton

    _type = RadButton

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)