import os

dir = os.path.abspath(os.path.dirname(__file__))

dir_telerik = os.path.join(dir, "telerik")
dir_telerik_net40 = os.path.join(dir_telerik, "net40")
dir_telerik_netcore = os.path.join(dir_telerik, "netcore")

dir_metro = os.path.join(dir, "metro")
dir_metro_net40 = os.path.join(dir_metro, "net40")

dir_skinsharp = os.path.join(dir, "skinsharp")
dir_skinsharp_2005_2008 = os.path.join(dir_metro, "Bin-2005-2008")

if "WINFORMS_RUNTIME" == os.environ:
    if os.environ["WINFORMS_RUNTIME"].lower() == "netcore":
        dir_telerik_default = dir_telerik_netcore
    else:
        dir_telerik_default = dir_telerik_net40
else:
    dir_telerik_default = dir_telerik_net40

# ---

libs1 = {}

if os.path.exists(dir_telerik_default):
    for lib in os.listdir(dir_telerik_default):
        path = os.path.join(dir_telerik_default, lib)
        if os.path.isfile(path):
            if os.path.splitext(path)[1] == ".dll":  # 判断文件扩展名是否为“.dll”
                libs1[lib] = path

libs2 = {}

if os.path.exists(dir_metro_net40):
    for lib in os.listdir(dir_metro_net40):
        path = os.path.join(dir_metro_net40, lib)
        if os.path.isfile(path):
            if os.path.splitext(path)[1] == ".dll":  # 判断文件扩展名是否为“.dll”
                libs2[lib] = path

libs3 = {}

if os.path.exists(dir_skinsharp_2005_2008):
    for lib in os.listdir(dir_skinsharp_2005_2008):
        path = os.path.join(dir_skinsharp_2005_2008, lib)
        if os.path.isfile(path):
            if os.path.splitext(path)[1] == ".dll":  # 判断文件扩展名是否为“.dll”
                libs3[lib] = path

"""
libs = {
    "RadControlSpy.dll":
        os.path.join(path, "RadControlSpy.dll"),
    "Telerik.WinControls.dll":
        os.path.join(path, "Telerik.WinControls.dll"),
    "Telerik.WinControls.Themes.Windows11.dll":
        os.path.join(path, "Telerik.WinControls.Themes.Windows11.dll"),
    "Telerik.WinControls.UI.dll":
        os.path.join(path, "Telerik.WinControls.UI.dll"),
}
"""
