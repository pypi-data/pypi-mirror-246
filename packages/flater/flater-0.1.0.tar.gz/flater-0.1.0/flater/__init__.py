from flater.library import libs1, libs2, libs3

# ---

from clr import AddReference

AddReference("System.Drawing")
AddReference("System.Windows")
AddReference("System.Windows.Forms")
AddReference("System.Runtime.InteropServices")


from System.Runtime.InteropServices import RuntimeInformation


# print("运行框架为", RuntimeInformation.FrameworkDescription)

def LoadTelerik():
    for lib in libs1:
        AddReference(libs1[lib])


def LoadMetro():
    for lib in libs2:
        AddReference(libs2[lib])


def LoadSkinSharp():
    for lib in libs3:
        AddReference(libs3[lib])

# ---

from flater.winforms import *
