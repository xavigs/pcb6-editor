from tkinter import *
from tkinter import ttk, filedialog, messagebox
import os
import binascii

# Constants
APP_TITLE = "Editor PCB 6.0 v2019 - by Xavi G Sunyer"
PCB6_FOLDER = ""
MANAGER_EXE = "MANAGER.EXE"
EQ_PFK = "DBDAT\EQ022022.PKF"
DBCs = []
HEX_STRING = {"20": "A", "23": "B", "22": "C", "25": "D", "24": "E", "27": "F", "26": "G", "29": "H", "28": "I", "2B": "J",
            "2A": "K", "2D": "L", "2C": "M", "2F": "N", "2E": "O", "31": "P", "30": "Q", "33": "R", "32": "S", "35": "T",
            "34": "U", "37": "V", "36": "W", "39": "X", "38": "Y", "3B": "Z",
            "00": "a", "03": "b", "02": "c", "05": "d", "04": "e", "07": "f", "06": "g", "09": "h", "08": "i", "0B": "j",
            "0A": "k", "0D": "l", "0C": "m", "0F": "n", "0E": "o", "11": "p", "10": "q", "13": "r", "12": "s", "15": "t",
            "14": "u", "17": "v", "16": "w", "19": "x", "18": "y", "1B": "z",
            "80": "á", "88": "é", "8C": "í", "92": "ó", "9B": "ú",
            "51": "0", "50": "1", "53": "2", "52": "3", "55": "4", "54": "5", "57": "6", "56": "7", "59": "8", "58": "9",
            "41": " ", "4C": "-", "4F": "."}
POINTERS = [2803, 11, 9900, 8, 9920, 2901, 16, 12, 2402, 1805, 1806, 1807]

# Variables
maxFolder = -1

'''
if managerSize == 2619392:
    if eqPKFSize == 1632501:
        # Right sizes
        eqPKF = open(EQ_PFK, "rb")
        #line = eqPKF.readline()
        #line = eqPKF.read(10)
        #print(decToHex(line[1]))
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

        for root, dirs, files in os.walk("patches"):
            for folder in dirs:
                if folder.isnumeric():
                    if int(folder) > maxFolder:
                        maxFolder = int(folder)

        if maxFolder == -1:
            newFolder = "000"
        else:
            newFolder = str(maxFolder + 1).rjust(3, "0")

        os.mkdir("patches\\" + newFolder)

        for index, DBC in enumerate(DBCs):
            numCharsShortName = int(DBC[84:86], 16)
            currentChar = 88
            numChars = 0
            shortName = ""

            while numChars < numCharsShortName:
                shortName += HEX_STRING[DBC[currentChar:(currentChar + 2)]]
                numChars += 1
                currentChar += 2

            print(shortName)

            newDBC = open("patches\\" + newFolder + "\\EQBA" + str(POINTERS[index]).rjust(4, "0") + ".DBC", "wb")
            newDBC.write(binascii.unhexlify(DBC))
            newDBC.close()
    else:
        # Wrong Teams PKF size
        print("La mida del PFK d'equips és incorrecta")
else:
    # Wrong EXE size
    print("La mida de l'EXE és incorrecta")

exit()
'''

##########################################################

def decToHex(number):
    return hex(number)[2:].upper().rjust(2, "0")

def fnOnClickSelectFolder():
    PCB6Folder = filedialog.askdirectory(initialdir = "/", title = "Selecciona la carpeta de instalación del PC Basket 6.0:")
    PCB6_FOLDER = PCB6Folder.replace("/", "\\")
    txtFolder.configure(state = "normal")
    txtFolder.delete(first = 0, last = 500)
    txtFolder.insert(0, PCB6Folder)
    txtFolder.configure(state = "readonly")

    # Load data
    try:
        managerSize = os.stat(PCB6_FOLDER + "\\" + MANAGER_EXE).st_size
        eqPKFSize = os.stat(PCB6_FOLDER + "\\" + EQ_PFK).st_size
        print(managerSize)
        print(eqPKFSize)
        lblImgLoading.place(x = 368, y = 271)
        lblLoading.place(x = (800 - 128) / 2, y = 346)

        if managerSize == 2619392:
            if eqPKFSize == 1632501:
                lblImgLoading.place_forget()
                lblLoading.place_forget()
            else:
                # Wrong Teams PKF size
                messagebox.showerror("PKF incorrecto", "ERROR: El tamaño del PKF de equipos es incorrecto.")
        else:
            # Wrong EXE size
            messagebox.showerror("MANAGER.EXE incorrecto", "ERROR: El tamaño del MANAGER.EXE es incorrecto.")
    except FileNotFoundError:
        messagebox.showerror("Directorio incorrecto", "ERROR: No se han encontrado los archivos adecuados en el directorio seleccionado. Seleccione otro directorio, por favor.")

def fnClose():
    root.destroy() # Destroy window

# Tkinter window
root = Tk()
root.title(APP_TITLE)
bit = root.iconbitmap("editor.ico")

# Fonts
fntTahoma10 = ("Tahoma", 10)

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

# Show window
posLeft = int((root.winfo_screenwidth() - 800) / 2 )
posTop = int((root.winfo_screenheight() - 660) / 2 )
geoParam = "800x600+" + str(posLeft) +  "+" + str(posTop)
root.geometry(geoParam)
root.protocol("WM_DELETE_WINDOW", fnClose)
#root.configure(background = "#000040")
root.mainloop()
