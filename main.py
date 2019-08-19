from tkinter import *
from tkinter import ttk, filedialog, messagebox
import os
import binascii

# Constants
APP_TITLE = "Editor PCB 6.0 v2019 - by Xavi G Sunyer"
PCB6_FOLDER = ""
MANAGER_EXE = "MANAGER.EXE"
EQ_PKF = "DBDAT\\EQ022022.PKF"
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

# Punters => No sabem quin és el punter de la selecció europea
POINTERS = [2803, 11, 9900, 8, 9910, 2901, 16, 12, 2402, 1805, 1806, 1807, 1808, 1809, 1303,
        1813, 7, 101, 4, 17, 14, 13, 15, 104, 2905, 704, 301, 302, 105, 106,
        801, 901, 902, 903, 904, 1001, 1101, 1002, 1202, 1203, 107, 2902, 102, 2906, 2804,
        201, 202, 303, 304, 401, 501, 2703, 2704, 2705, 5, 2707, 3, 2709, 2101, 9955,
        2103, 1216, 1301, 1302, 2802, 1304, 1305, 1306, 1701, 1702, 1703, 1307, 1308, 1309, 1310,
        1501, 1502, 1503, 1901, 1707, 1801, 1802, 9920, 22, 203, 502, 601, 602, 701, 702,
        703, 705, 2203, 2204, 2205, 2301, 2004, 2102, 2104, 2706, 2708, 10, 2506, 2512, 2513,
        2601, 2602, 2701, 2305, 2306, 2401, 2201, 2202, 1, 103, 9, 2801, 2, 2002, 2003,
        20, 21, 2504, 2505, 1803, 1804, 1705, 1706, 1601, 1704, 1902, 2001, 3001, 18, 6,
        1204, 1205, 1206, 1207, 1201, 1208, 1209, 1311, 1401, 1402, 1214, 2403, 2501, 2502, 2503,
        2304, 2302, 2303, 19, 2105, 2903, 2904, 2702, 706, 905, 1812, 9950]

# Variables
maxFolder = -1

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
        # Global variables
        global MANAGER_EXE
        global EQ_PKF
        global maxFolder

        # Load files and test sizes
        MANAGER_EXE = PCB6_FOLDER + "\\" + MANAGER_EXE
        EQ_PKF = PCB6_FOLDER + "\\" + EQ_PKF
        managerSize = os.stat(MANAGER_EXE).st_size
        eqPKFSize = os.stat(EQ_PKF).st_size
        lblImgLoading.place(x = 368, y = 271)
        lblLoading.place(x = (800 - 128) / 2, y = 346)
        lblImgLoading.update()
        lblLoading.update()

        if managerSize == 2619392:
            if eqPKFSize == 1632501:
                # Right sizes
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
