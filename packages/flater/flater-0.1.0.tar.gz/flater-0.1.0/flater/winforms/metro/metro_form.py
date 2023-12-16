from flater.winforms.form import Form

from flater.winforms.metro.metro_control import MetroControl


class MetroForm(Form, MetroControl):
    from MetroFramework.Forms import MetroForm

    _type = MetroForm

    from enum import Enum

    class WindowButtons(Enum):
        Close = 0,
        Maximize = 1,
        Minimize = 2,

    def __init__(self, StyleManager: bool = True):
        super().__init__()

        from flater.winforms.metro.metro_style_manager import MetroStyleManager

        if StyleManager:
            self.StyleManager = MetroStyleManager()  # 全局设置主题
            self.StyleManager.Owner = self
            self.StyleManager.Theme = "Dark"
            self.StyleManager.Style = "Blue"

    @property
    def Movable(self):
        """
        是否可以移动

        Returns:
            bool: 返回布尔值

        """
        return self._.Movable

    @Movable.setter
    def Movable(self, Enable: bool):
        """
        是否可以移动

        Args:
            Enable (bool): 是否启用

        Returns:
            bool: 不返回

        """
        self._.Movable = Enable

    def RemoveCloseButton(self):
        self._.RemoveCloseButton()

    from flater.winforms.metro.metro_style_manager import MetroStyleManager
