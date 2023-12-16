from flater.winforms.telerik.simple import *

root = MainWindow()
root.title("Hello World")
root.theme_use("win11dark")

root.size(500, 600)

button = Button(root, text="Light")
button.on_click(lambda sender, args: root.theme_use("win11"))
button.place(0, 0, 150, 40)

button2 = Button(root, text="Dark")
button2.on_click(lambda sender, args: root.theme_use("win11dark"))
button2.place(0, 50, 150, 40)

# root.create_control_spy_window()
root.mainloop()
