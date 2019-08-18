import tkinter

# Constants
APP_TITLE = "Editor PCB 6.0"

def fnClose():
    root.destroy() # Destroy window

# Tkinter window
root = tkinter.Tk()
root.title(APP_TITLE)
bit = root.iconbitmap("editor.ico")

posLeft = int((root.winfo_screenwidth() - 800) / 2 )
posTop = int((root.winfo_screenheight() - 660) / 2 )
root.wm_state("normal")
geo_param = "800x600+" + str(posLeft) +  "+" + str(posTop)
root.geometry(geo_param)

root.protocol("WM_DELETE_WINDOW", fnClose)
root.mainloop()
