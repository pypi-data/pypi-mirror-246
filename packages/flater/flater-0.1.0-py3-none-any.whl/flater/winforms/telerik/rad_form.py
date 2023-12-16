from flater.winforms.form import Form
from flater.winforms.telerik.rad_control import RadControl


class RadForm(RadControl, Form):

    from Telerik.WinControls.UI import RadForm

    _type = RadForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
