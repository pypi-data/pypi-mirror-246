class Basic(object):
    """
    基础类

    Attributes:
        _type (Class): 被初始化的类
    """

    _type = None

    def __init__(self):
        self._ = self._type()

    def Bind(self, Name: str, Func=None):
        """
        绑定事件

        Args:
            Name (str): 事件名称（请参见对应组件事件文档）
            Func (Callback): 事件函数（一般包括两个返回参数）

        Example:
            func1 = lambda e1, e2: print("Hello1")
            func2 = lambda e1=None, e2=None: print("Hello2")
            func3 = lambda e1, e2: print("Hello3")

            control.Bind("Click", func1)
            control.Bind("Click", func2)
            control.Bind("Click", func3)
            control.UnBind("Click", func2)

            # Hello1
            # Hello3
        """
        _ = getattr(self._, Name)
        _ += Func
        setattr(self._, Name, _)

    @property
    def Myself(self):
        return self._

    @Myself.setter
    def Myself(self, Class):
        self._ = Class

    def UnBind(self, Name: str, Func=None):
        """
        取消绑定事件

        Args:
            Name (str): 事件名称（请参见对应组件事件文档）
            Func (Callback): 事件函数
        """
        _ = getattr(self._, Name)
        _ -= Func
        setattr(self._, Name, _)
