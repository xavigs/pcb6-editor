from tkinter import *

# Constants
APP_TITLE = "Editor PCB 6.0"

def fnClose():
    root.destroy() # Destroy window

def fnProcessMenu():
    topWindow = Toplevel()
    button = Button(topWindow, text = "Siguemarén")
    button.pack()

# Tkinter window
root = Tk()
root.title(APP_TITLE)
bit = root.iconbitmap("editor.ico")

posLeft = int((root.winfo_screenwidth() - 800) / 2 )
posTop = int((root.winfo_screenheight() - 660) / 2 )
root.wm_state("normal")
geoParam = "800x600+" + str(posLeft) +  "+" + str(posTop)
root.geometry(geoParam)

# Menu
menubar = Menu(root)
filemenu = Menu(menubar, tearoff = 0)

# Menu options
filemenu.add_command(label = "Crear", command = fnProcessMenu)
#filemenu.add_separator()

# Add menu to bar
menubar.add_cascade(label = "File", menu = filemenu)

# Add menu to window
root.config(menu = menubar)

# Show window
root.protocol("WM_DELETE_WINDOW", fnClose)
root.mainloop()
