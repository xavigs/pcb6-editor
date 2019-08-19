import sys
sys.path.append(r'utils')
from constants import *

from tkinter import *
from tkinter import ttk, filedialog, messagebox
import os
import binascii

# Variables
DB = []
DBCs = []
PCB6Folder = ""
maxFolder = -1

def decToHex(number):
    return hex(number)[2:].upper().rjust(2, "0")

def fnOnClickSelectFolder():
    PCB6FolderShow = filedialog.askdirectory(initialdir = "/", title = "Selecciona la carpeta de instalación del PC Basket 6.0:")
    PCB6Folder = PCB6FolderShow.replace("/", "\\")
    txtFolder.configure(state = "normal")
    txtFolder.delete(first = 0, last = 500)
    txtFolder.insert(0, PCB6FolderShow)
    txtFolder.configure(state = "readonly")

    # Load data
    try:
        # Global variables
        global MANAGER_EXE
        global EQ_PKF
        global COUNTRIES_ALL
        global COUNTRIES_PLAYERS
        global maxFolder

        # Load files and test sizes
        MANAGER_EXE = PCB6Folder + "\\" + MANAGER_EXE
        EQ_PKF = PCB6Folder + "\\" + EQ_PKF
        COUNTRIES_ALL = PCB6Folder + "\\" + COUNTRIES_ALL
        COUNTRIES_PLAYERS = PCB6Folder + "\\" + COUNTRIES_PLAYERS
        managerSize = os.stat(MANAGER_EXE).st_size
        eqPKFSize = os.stat(EQ_PKF).st_size
        lblImgLoading.place(x = 368, y = 271)
        lblLoading.place(x = (800 - 128) / 2, y = 346)
        lblImgLoading.update()
        lblLoading.update()

        if managerSize == 2619392:
            if eqPKFSize == 1632501:
                # Right sizes
                # Read Countries
                countriesPlayers = open(COUNTRIES_PLAYERS, "rb")
                countryName = ""
                currentByte = 0
                numCharsName = 0
                nextCountry = 18
                firstByte = nextCountry + 2
                inCountry = False
                country = {}

                for byte in countriesPlayers.read():
                    if currentByte == nextCountry:
                        # Country found
                        inCountry = True
                        numCharsName = byte
                        lastByte = nextCountry + byte + 1
                        pointerByte = lastByte + 1
                    else:
                        if inCountry and currentByte >= firstByte:
                            if currentByte <= lastByte:
                                countryName += HEX_STRING[decToHex(byte)]

                                if currentByte == lastByte:
                                    country['name'] = countryName
                            else:
                                if currentByte == pointerByte:
                                    country['pointer'] = byte
                                    inCountry = False
                                    nextCountry = lastByte + 5
                                    firstByte = nextCountry + 2
                                    countryName = ""
                                    DB.append(country)
                                    country = {}

                    currentByte += 1

                for index, country in enumerate(DB):
                    root.listbox.insert((index + 1), country['name'])

                lblCountries.place(x = 10, y = 50)
                lblCountries.update()
                root.listbox.place(x = 10, y = 60 + lblCountries.winfo_height(), height = 500)
                root.listbox.update()
                scrollbar.place(x = 10 + root.listbox.winfo_width(), y = 60 + lblCountries.winfo_height(), height = 500)
                root.listbox.configure(yscrollcommand = scrollbar.set)
                '''
                eqPKF = open(EQ_PKF, "rb")
                foundFirst = False
                foundSecond = False
                foundTeam = False
                currentTeam = ""

                for byte in eqPKF.read():
                    if foundTeam:
                        currentTeam += decToHex(byte)

                    if decToHex(byte) == "43":
                        foundFirst = True
                    else:
                        if decToHex(byte) == "6F" and foundFirst:
                            foundSecond = True
                        else:
                            if decToHex(byte) == "70" and foundSecond:
                                # Found team
                                if foundTeam:
                                    currentTeam = currentTeam[:-6]
                                    DBCs.insert(len(DBCs), currentTeam)

                                foundTeam = True
                                foundFirst = False
                                foundSecond = False
                                currentTeam = "436F70"
                            else:
                                # Team not found
                                foundFirst = False
                                foundSecond = False

                eqPKF.close()

                # Find last folder in patches
                for root, dirs, files in os.walk("patches"):
                    for folder in dirs:
                        if folder.isnumeric():
                            if int(folder) > maxFolder:
                                maxFolder = int(folder)

                # Create new folder in patches
                if maxFolder == -1:
                    newFolder = "000"
                else:
                    newFolder = str(maxFolder + 1).rjust(3, "0")

                os.mkdir("patches\\" + newFolder)

                # Save the DBCs of the teams
                for index, DBC in enumerate(DBCs):
                    numCharsShortName = int(DBC[84:86], 16)
                    currentChar = 88
                    numChars = 0
                    shortName = ""

                    while numChars < numCharsShortName:
                        shortName += HEX_STRING[DBC[currentChar:(currentChar + 2)]]
                        numChars += 1
                        currentChar += 2

                    #print(shortName)

                    newDBC = open("patches\\" + newFolder + "\\EQBA" + str(POINTERS[index]).rjust(4, "0") + ".DBC", "wb")
                    newDBC.write(binascii.unhexlify(DBC))
                    newDBC.close()
                '''

                # Hide Loading image and text
                lblImgLoading.place_forget()
                lblLoading.place_forget()
            else:
                # Wrong Teams PKF size
                messagebox.showerror("PKF incorrecto", "ERROR: El tamaño del PKF de equipos es incorrecto.")
        else:
            # Wrong EXE size
            messagebox.showerror("MANAGER.EXE incorrecto", "ERROR: El tamaño del MANAGER.EXE es incorrecto.")
    except FileNotFoundError as e:
        print(e)
        messagebox.showerror("Directorio incorrecto", "ERROR: No se han encontrado los archivos adecuados en el directorio seleccionado. Seleccione otro directorio, por favor.")

def fnClose():
    root.destroy() # Destroy window

# Tkinter window
root = Tk()
root.title(APP_TITLE)
bit = root.iconbitmap("editor.ico")

# Fonts
fntTahoma10 = ("Tahoma", 10)
fntTahomaBold10 = ("Tahoma", 10, "bold")

# Menu
menubar = Menu(root)
filemenu = Menu(menubar, tearoff = 0)

# Menu options
filemenu.add_command(label = "Salir", command = fnClose)
#filemenu.add_separator()

# Add menu to bar
menubar.add_cascade(label = "Archivo", menu = filemenu)

# Add menu to window
root.config(menu = menubar)

# Folder selector
lblSelectFolder = Label(root, text = "Selecciona la carpeta donde tienes instalado el PC Basket 6.0:", font = fntTahoma10)
lblSelectFolder.place(x = 5, y = 7)
lblSelectFolder.update()

# Folder textbox
txtFolder = Entry(root, font = fntTahoma10, relief = SOLID, borderwidth = 1, width = 40)
txtFolder.configure(state = "readonly")
txtFolder.place(x = 10 + lblSelectFolder.winfo_width(), y = 7)

# Folder selection Button
btnSelectFolder = Button(root, text = "Examinar...", font = fntTahoma10, command = fnOnClickSelectFolder, relief = SOLID, borderwidth = 1, width = 15)
btnSelectFolder.place(x = 800 - 113 - 10, y = 5)
btnSelectFolder.update()

# Separator
separator1 = ttk.Separator(root, orient = HORIZONTAL)
separator1.place(x = 0, y = 12 + btnSelectFolder.winfo_height(), relwidth = 1.0)

# Loading image
imgLoading = PhotoImage(file = "img/loading.png")
lblImgLoading = Label(root, image = imgLoading, bg = "#F0F0F0")

# Loading Label
lblLoading = Label(root, text = "Cargando los datos...", font = fntTahoma10)
lblLoading.update()

# Countries label
lblCountries = Label(root, text = "Países:", font = fntTahomaBold10)

# Countries listbox
root.listbox = Listbox(root, exportselection = 0, highlightcolor = "#808080", selectbackground = "#FF4000", selectmode = SINGLE, activestyle = NONE, font = fntTahoma10)

# Scrollbar for countries Listbox
scrollbar = ttk.Scrollbar(root, orient = VERTICAL, command = root.listbox.yview)

# Show window
posLeft = int((root.winfo_screenwidth() - 800) / 2 )
posTop = int((root.winfo_screenheight() - 660) / 2 )
geoParam = "800x600+" + str(posLeft) +  "+" + str(posTop)
root.geometry(geoParam)
root.protocol("WM_DELETE_WINDOW", fnClose)
#root.configure(background = "#000040")
root.mainloop()
