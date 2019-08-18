from tkinter import *
import os

# Constants
APP_TITLE = "Editor PCB 6.0"
MANAGER_EXE = "E:\PCB6\MANAGER.EXE"
EQ_PFK = "E:\PCB6\DBDAT\EQ022022.PKF"

def decToHex(number):
    return hex(number)[2:].upper()

managerSize = os.stat(MANAGER_EXE).st_size
eqPKFSize = os.stat(EQ_PFK).st_size

if managerSize == 2619392:
    if eqPKFSize == 1632501:
        # Right sizes
        print("Siguem-hi")
        eqPKF = open(EQ_PFK, "br")
        #line = eqPKF.readline()
        line = eqPKF.read(10)
        print(decToHex(line[1]))
    else:
        # Wrong Teams PKF size
        print("La mida del PFK d'equips és incorrecta")
else:
    # Wrong EXE size
    print("La mida de l'EXE és incorrecta")

exit()

##########################################################

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
