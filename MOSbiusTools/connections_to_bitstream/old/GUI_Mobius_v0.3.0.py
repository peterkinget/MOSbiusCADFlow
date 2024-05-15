#!/usr/local/bin/python3
# GUI_Mobius_v0.2.0
# Oct. 30, 2022
# v0.0   created by Longyi Li;
# v0.1   Peter Kinget -- resizable window and frame
# v0.1.1 Peter Kinget -- save CLK button
# v0.1.2 Peter Kinget -- updated the file formats for padding beginning and end
# v0.1.3 Peter Kinget -- got rid of PIL (pillow) and made file extension to csv
# v0.2.0 Peter Kinget -- switched to pin numbers

from tkinter import *
from tkinter.filedialog import asksaveasfile
# from PIL import ImageTk, Image
import json

# create the root window
root = Tk()
root.title('MOBIUS MOS Circuits on Chip v0.2.0')
# create the resizeable frame in window -- see https://stackoverflow.com/questions/7591294/how-to-create-a-self-resizing-grid-of-buttons-in-tkinter
frame = Frame(root)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
frame.grid(row=0, column=0, sticky="news")
grid = Frame(frame)
grid.grid(sticky="news", column=0, row=7, columnspan=2)
frame.rowconfigure(7, weight=1)
frame.columnconfigure(0, weight=1)

# set up the variables
text = [[None]*68 for _ in range(10)]
buttons = [[None]*68 for _ in range(10)]
bus = [None for _ in range(10)]
pin = [None for _ in range(68)]
zero=0;

no_connects = {11, 12, 13}
tmp_list = [[10], list(range(14,69)), list(range(1,10))]
pin_to_matrix_order = [num for sublist in tmp_list for num in sublist]
# print(pin_to_matrix_order)

def action(i, j):
    if (text[i][j].get()=='1'):
        text[i][j].set('0')
    else:
        text[i][j].set('1')
        

# print the pin labels (i.e. column labels)
LINEONE=Text(frame, height=1, width=5)
LINEONE.grid(row = 0, column = 0)
LINEONE.insert("1.0", "PIN")
for i in range(68):
    pin[i]=Text(frame, height=1, width=3, font=("Arial",10))
    pin[i].grid(row = 0, column = i+1)
    if not((i+1) in no_connects): 
        pin[i].insert("1.0", "%02d" % (i+1)) # regular pin connected to Switch Matrix
    else: 
        pin[i].insert("1.0", "NC")           # pin not connected to Switch Matrix

# print the connection matrix with bus labels (i.e. row labels) 
for i in range(10):
    bus[i] = Text(frame, height=1, width=8)
    bus[i].grid(row = i+1, column = 0)
    bus[i].insert("1.0", "BUS%02d" % (i+1))
    # now populate the connection matrix with clickable buttons
    for j in range(68):
        text[i][j] = StringVar()
        text[i][j].set('0')
        btn = Button(frame, command = lambda i=i, j=j: action(i,j))
        btn.config(textvariable = text[i][j], font=("Arial",8)) # , width=1, height=1)
        btn.grid(column=j+1, row=i+1, sticky="news")

def resetall():
    for i in range(10):
        for j in range(68):
            text[i][j].set('0')
            
def save():
    Files = [('CSV File', '*.csv'),('All Files', '*.*')]
    file = asksaveasfile(filetypes = Files, defaultextension = Files)
    print (file)
    with open(file.name, 'w') as f:
        # leading zero option
        if (var1.get()==1):
            f.write("0\n")
        # add dummy bit to start
        f.write("0\n")
        # write the bits
        for i in range(9, -1, -1):
  #          for j in range(67, -1, -1):
  #              if (j!=1) and (j!=2) and (j!=3): #ignore pin 2,3,4
            for j in reversed(pin_to_matrix_order):
                if not(j in no_connects):
                    f.write(text[i][j-1].get())    
                    f.write("\n")                        
            f.write("")    
        # add dummy bit to end
        f.write("0\n")
            
def listConnections():
    popup = Tk()
    popup.wm_title("Connections")
    
    textMessage = ""
    warningNC = False
    
    for i in range(10):
        textMessage = textMessage + "Bus %02d: " % (i+1)
        firstpin = True
        for j in range(68):
            if (text[i][j].get() == '1'):
                if firstpin:
                    textMessage = textMessage + "%02d" % (j+1)
                    firstpin = False
                else:
                    textMessage = textMessage + ", %02d" % (j+1)
        for k in no_connects:
            if (text[i][k-1].get() == '1'):
                warningNC = True
        textMessage = textMessage + "\n"
    if warningNC:
        textMessage = textMessage + "\n WARNING: There are connections to NC\n"
        
    label = Label(popup, text=textMessage, justify=LEFT)
    # label.pack(side="top", pady=10, anchor="w")
    label.pack() 
    B1 = Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()    

def writeConnectionsToFile():
    popup = Tk()
    popup.wm_title("Writing Connections to connections.json")
    
    textMessage = ""
    warningNC = False

    # build the dictionary
    connections = {}
    for i in range(10):
        label = f"{i}"
        connections[label]= []
        for j in range(68):
            if (text[i][j].get() == '1'):
                connections[label].append(j)
                print(i,j)
    print(connections)
    # dump to json file
    filename = "connections.json"
    with open(filename, "w") as outfile:
        json.dump(connections, outfile)
        
    textMessage = "Wrote connections.json\n"
        
    label = Label(popup, text=textMessage, justify=LEFT)
    # label.pack(side="top", pady=10, anchor="w")
    label.pack() 
    B1 = Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()    

def saveClockPattern():
    Files = [('CSV File', '*.csv'),('All Files', '*.*')]
    file = asksaveasfile(filetypes = Files, defaultextension = Files)
    print (file)
    with open(file.name, 'w') as f:
        # start with two 'empty cycles'
        f.write("0\n")
        f.write("0\n")
        # write 650 rising edges
        for i in range(650):
            f.write("0\n")
            f.write("1\n")
        # pad with two 'empty cycles'
        f.write("0\n")
        f.write("0\n")
            
# Put the buttons on the bottom row
#
# Reset Button
rsttext = StringVar()
rsttext.set('RESET')    
RST = Button(frame, command = resetall)
RST.config(textvariable = rsttext, width = 6, height = 1)
RST.grid(row = 11, column = 0,columnspan=3, sticky='W')

# List Connections Button
listConnectionsText = StringVar()
listConnectionsText.set('List Connections')
LISTCON = Button(frame, command = lambda : listConnections())
LISTCON.config(textvariable = listConnectionsText, width =10, height = 1)
LISTCON.grid(row=11, column=5, columnspan=3, sticky='W')

# Write Connections Button
writeConnectionsText = StringVar()
writeConnectionsText.set('Write Connections')
WRITECON = Button(frame, command = lambda : writeConnectionsToFile())
WRITECON.config(textvariable = writeConnectionsText, width =10, height = 1)
WRITECON.grid(row=11, column=2, columnspan=3, sticky='W')

# Add leading 0 Button
var1 = IntVar()
cb1 = Checkbutton(frame, text='Add Leading 0',variable=var1, onvalue=1, offvalue=0)
cb1.grid(row = 11, column = 10,columnspan=3, sticky='W')

# Export Button
exptext = StringVar()
exptext.set('EXPORT')   
EXPORT = Button(frame, command = lambda : save())
EXPORT.config(textvariable = exptext, width = 6, height = 1)
EXPORT.grid(row = 11, column = 15,columnspan=3, sticky='W')

# Clock Export Button
clock_exptext = StringVar()
clock_exptext.set('Save CLK')   
EXPORT = Button(frame, command = lambda : saveClockPattern())
EXPORT.config(textvariable = clock_exptext, width = 6, height = 1)
EXPORT.grid(row = 11, column = 20,columnspan=3, sticky='W')

# Add schematic image
sch = PhotoImage(file="sch_pin_numbers.png")
#sch = sch.resize((600,600), Image.ANTIALIAS)

# img = ImageTk.PhotoImage(sch)

# Create a Label Widget to display the text or Image
label = Label(root, image = sch)
label.grid(row = 1, column = 0) #,columnspan=100, sticky='W')

        
frame.columnconfigure(tuple(range(69)), weight=1)
frame.rowconfigure(tuple(range(12)), weight=1)

root.mainloop()
