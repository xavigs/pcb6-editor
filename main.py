from tkinter import *
import os
import binascii

# Constants
APP_TITLE = "Editor PCB 6.0 v2019 - by Xavi G Sunyer"
MANAGER_EXE = "E:\PCB6\MANAGER.EXE"
EQ_PFK = "E:\PCB6\DBDAT\EQ022022.PKF"
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

def decToHex(number):
    return hex(number)[2:].upper().rjust(2, "0")

managerSize = os.stat(MANAGER_EXE).st_size
eqPKFSize = os.stat(EQ_PFK).st_size

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

            newDBC = open("EQBA" + str(POINTERS[index]).rjust(4, "0") + ".DBC", "wb")
            newDBC.write(binascii.unhexlify(DBC))
            newDBC.close()
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
