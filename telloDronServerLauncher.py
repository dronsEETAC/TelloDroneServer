from tkinter import *
from PIL import ImageTk, Image
from ServerPlayMQTT import ServerRun as ServerPlayRun
from MQTTOneDroneServer import ServerRun as ServerOnDroneRun

root = Tk()
root.geometry("800x500")

def startOneDron ():
    ServerOnDroneRun()

def startPlay():
    global playersEntry
    ServerPlayRun(int (playersEntry.get()))

def play ():
    global playersEntry
    global canvas
    global bg
    global image
    global startOneDroneButton
    global labelNumPlayers
    global playersEntry
    global startPlayButton
    if startOneDroneButton is not None:
        startOneDroneButton.place_forget()

    image = Image.open("assets/play.png")
    image = image.resize((600, 500), Image.ANTIALIAS)
    bg = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image=bg, anchor="nw")

    labelNumPlayers = Label(root, text = 'Number of players')
    labelNumPlayers.place(x=180, y=470, anchor="nw")
    playersEntry = Entry (root, width = 10)
    playersEntry.insert (0,"4")
    playersEntry.place(x=300, y=470, anchor="nw")
    startPlayButton = Button(root, text="Start", bg='#367E18', fg='#FFE9A0', width=20,
                         command=startPlay)
    startPlayButton.place(x=400, y=470, anchor="nw")

def oneDron ():
    global image
    global canvas
    global bg
    global startOneDroneButton
    global labelNumPlayers
    global playersEntry
    global startPlayButton

    if startPlayButton is not None:
        startPlayButton.place_forget()
        playersEntry.place_forget()
        labelNumPlayers.place_forget()



    image = Image.open("assets/oneDrone.png")
    image = image.resize((600, 500), Image.ANTIALIAS)
    bg = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image=bg, anchor="nw")
    startOneDroneButton = Button(root, text="Start", bg='#367E18', fg='#FFE9A0', width=40,
                             command=startOneDron)
    startOneDroneButton.place(x=200, y=470, anchor="nw")

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=4)

startOneDroneButton = None
startPlayButton = None

oneDronBtn = Button(root, text="one dron", bg='#F57328', fg="white",
                     command=oneDron)
oneDronBtn.grid(row=0, column=0, padx=5, pady=5, sticky=N + S + E + W)
playBtn = Button(root, text="play", bg='#F57328', fg="white",
                     command=play)
playBtn.grid(row=1, column=0, padx=5, pady=5, sticky=N + S + E + W)

image = Image.open("assets/presentation.png")
image = image.resize((700, 500), Image.ANTIALIAS)
bg = ImageTk.PhotoImage(image)
canvas = Canvas(root, width=700, height=500)
canvas.grid(row=0, column=1, rowspan=2, padx=20, pady=20, sticky=N + S + E + W)

canvas.create_image(0, 0, image=bg, anchor="nw")

root.mainloop()