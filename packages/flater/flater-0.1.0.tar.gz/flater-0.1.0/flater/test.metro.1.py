from flater.winforms.metro import *
from flater import *

window = MetroForm()
window.StyleManager.Style = "Red"

button3 = MetroButton(Parent=window)
button3.Text = "System"
button3.Bind("Click", lambda e1, e2: window.StyleManager.SetTheme("System"))
button3.Pack(Dock="Top")

button2 = MetroButton(Parent=window)
button2.Text = "Dark"
button2.Bind("Click", lambda e1, e2: window.StyleManager.SetTheme("Dark"))
button2.Pack(Dock="Top")

button = MetroButton(Parent=window)
button.Text = "Light"
button.Bind("Click", lambda e1, e2: window.StyleManager.SetTheme("Light"))
button.Pack(Dock="Top", Margin=10)

window.AppRun()