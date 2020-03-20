# Program for selecting items at random from a .txt file
#
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import random
import time

def selectAnother(event):

    # Clear the display of the previous selection:
    canvas.delete("selectionText")
    canvas.delete("selectionTextRect")
    canvas.delete("arcs")
    circleColor = originalCircleColor
    if len(notYetSelected) < len(itemsFromFile):
        circleColor = "#%06x" % random.randint(0, 0xCCCCCC)
        canvas.itemconfigure('outerCircle',fill=circleColor)

    # Draw as many arcs as the number of the remaining possible selections:
    if len(notYetSelected) > 1:
        arcExtent = 360 / len(notYetSelected)
        startingAngle = 90
        for element in notYetSelected:
            arcColor = "#%06x" % random.randint(0, 0xCCCCCC)
            canvas.create_arc(25, 25, 615, 615, start=startingAngle, extent=arcExtent, fill=arcColor, tags='arcs')
            canvas.create_rectangle((60, 280, 580, 360), tags='selectionTextRect', fill="white")
            canvas.create_text((320,320),text=element + "???", font=("Arial", 36), fill=arcColor, tags='selectionText')
            root.update()
            delayLength = 2.5 / len(notYetSelected)
            time.sleep(delayLength)
            startingAngle += arcExtent

    # Make the random selection, announce it, and remove this item from the list of remaining possibilities:
    if len(notYetSelected) > 0:
        selectionIndex = random.randint(0,len(notYetSelected)-1)
        canvas.delete("arcs")
        canvas.create_rectangle((60, 280, 580, 360), tags='selectionTextRect', fill="white")
        canvas.create_text((320,320),text=notYetSelected[selectionIndex], font=("Arial", 36), fill=circleColor, tags='selectionText')
        notYetSelected.remove(notYetSelected[selectionIndex])
    else:
        canvas.create_rectangle((60, 280, 580, 360), tags='selectionTextRect', fill="white")
        canvas.create_text((320,320),text="No more to select", fill=circleColor, font=("Arial", 36), tags='selectionText')
        
def terminateProgram(event):
    canvas.delete(ALL)
    root.destroy()

# Set up screen for "wheel" display:
root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

canvas = Canvas(root, width=900, height=640)
canvas.grid(column=0, row=0, sticky=(N, W, E, S))

# This line is supposed to somehow make the file dialogue (see below) disappear after you make your selection,
# but it apparently is only effective in combination with root.destroy(), as used upon exiting the program.
root.update()

# Read items from text file into list:
#
# To create this text file:
# (1) Make a special Word doc with a list of all the items. Do not include any blank lines.
# (2) Use www.online-convert.com to convert that Word doc to txt. This will be in the UTF-8 format (instead of
#     the troublesome Mac Extended Ascii character set used by TextEdit).
itemsFromFile = []
filename = filedialog.askopenfilename()
with open(filename,encoding='utf-8-sig') as Datei:
    for line in Datei:
        rightStrippedLine = line.strip()
        if len(rightStrippedLine) > 0:
            itemsFromFile.append(rightStrippedLine)

# Make a copy of the list of items, to use for selection purposes
notYetSelected = itemsFromFile

# Draw circle as outer border of "wheel":
originalCircleColor = "#%06x" % random.randint(0, 0xCCCCCC)
canvas.create_oval(25, 25, 615, 615, fill=originalCircleColor, outline='black', width=2, tags='outerCircle')

# Draw as many arcs as the number of the remaining possible selections:
if len(notYetSelected) > 1:
    arcExtent = 360 / len(notYetSelected)
    startingAngle = 90
    for element in notYetSelected:
        canvas.create_arc(25, 25, 615, 615, start=startingAngle, extent=arcExtent,tags='arcs')
        startingAngle += arcExtent

# Draw buttons on screen:
id = canvas.create_rectangle((640, 25, 875, 525), tags='buttons', fill="green")
canvas.tag_bind(id, "<Button-1>", selectAnother)
id = canvas.create_rectangle((640, 530, 875, 615), tags='buttons', fill="red")
canvas.tag_bind(id, "<Button-1>", terminateProgram)

# Start event-driven processing:
root.mainloop()
