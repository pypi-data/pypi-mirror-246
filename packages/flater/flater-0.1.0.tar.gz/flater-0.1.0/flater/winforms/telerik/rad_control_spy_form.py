from flater.winforms.telerik.rad_form import RadForm


class RadControlSpyForm(RadForm):

    from Telerik.WinControls.RadControlSpy import RadControlSpyForm

    _type = RadControlSpyForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
