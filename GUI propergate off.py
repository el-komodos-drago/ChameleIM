import tkinter
from tkinter.filedialog import askopenfilename as selectfile
from tkinter.filedialog import asksaveasfilename as selectsavefile
from tkinter.simpledialog import askstring
from tkinter.font import Font

import time

from Contacts import RetriveContacts
from MainLibrary import CreateInvite, AcceptInvite

def SendInvite():
    ContactName = ""
    while ContactName == "":
        ContactName = askstring("input", "What is the name of the contact you want to add?")
    if ContactName == None:
        return()
    InputFile = selectfile(title="Select image to hide invite in",
                           filetypes=(("png files","*.png"),))
    if InputFile == "":
        return()
    OutputFile = selectsavefile(title="Select location to save invite",
                                filetypes=(("png files","*.png"),))
    if OutputFile == "":
        return()
    NoticeText = tkinter.StringVar()
    notice = tkinter.Label(master=MainWindow, textvariable=NoticeText)
    notice.grid(row=3, column=0, columnspan=3,sticky="ew")
    MainWindow.update_idletasks()
    for progress in CreateInvite(ContactName,InputFile,OutputFile): #CreateInvite uses yeild
        NoticeText.set(progress)
        MainWindow.update_idletasks()
    NoticeText.set("Invite created")
    MainWindow.update_idletasks()
    time.sleep(3)
    notice.destroy()
    #MainWindow.config(cursor="")
    

def OpenInvite():
    ContactName = ""
    while ContactName == "":
        ContactName = askstring("input", "What is the name of the contact you want to add?")
    if ContactName == None:
        return()
    InputFile = selectfile(title="Select image to hide invite in",
                           filetypes=(("png files","*.png"),))
    if InputFile == "":
        return()
    
    NoticeText = tkinter.StringVar()
    notice = tkinter.Label(master=MainWindow, textvariable=NoticeText)
    notice.grid(row=2, column=0, columnspan=3,sticky="ew")
    MainWindow.update_idletasks()
    for attempt in AcceptInvite(ContactName,InputFile): #CreateInvite uses yeild
        NoticeText.set("Generating Keypair, Attempt: "+attempt)
        MainWindow.update_idletasks()

def ContactSettings():
    print()

def Refresh():
    print()

def DisplayContact(ContactID):
    print(ContactID)

def RenderContactBar(MaxWidth):
    MaxWidth = int(MaxWidth)
    CourierNew = Font(family="Courier New")
    MaxWidth = 10
    
    ContactBar = tkinter.Frame(master=MainWindow, bg="Light Grey", width = MaxWidth,
                           highlightbackground="black",highlightthickness=1)
    ContactBar.grid(row=2, column=0,sticky="nsew")
    #ContactBar.grid_propagate(False)
    #Contact list:
    ContactButtons = {}
    contacts = RetriveContacts()
    for contact in contacts:
        ContactName,ID = contact
        if len(ContactName) > MaxWidth:
            ContactName = ContactName[0:int(MaxWidth-3)]+"..." # Cut length of contact name
        ContactButtons[ID] = tkinter.Button(master=ContactBar,text=ContactName,
                                            width=MaxWidth, #font=CourierNew, 
                                            bg="Light Grey", relief = tkinter.FLAT,
                                            command=lambda a=ID: DisplayContact(a))
        ContactButtons[ID].pack(padx=5, side=tkinter.TOP,anchor="w")
    
    #Add contact button:
    AcceptInviteButton = tkinter.Button(master=ContactBar,text="➕ Accept Invite",
                                    bg="Light Grey", relief = tkinter.FLAT,
                                    command=OpenInvite)
    AcceptInviteButton.pack(padx=10, side=tkinter.TOP,anchor="w")
    return(ContactBar)

def RenderMessagesHeader():
    ContactDisplayed = tkinter.Label(master=MessagesHeader,text="",
                                     bg="Dark Grey", relief = tkinter.FLAT)
    ContactDisplayed.pack(padx=0, side=tkinter.LEFT,anchor="w")
    ContactSetttings = tkinter.Button(master=MessagesHeader,text="⚙️",
                                     bg="Dark Grey", relief = tkinter.FLAT,
                                     command=ContactSettings)
    ContactSetttings.pack(padx=0, side=tkinter.RIGHT,anchor="e")
    RefreshButton = tkinter.Button(master=MessagesHeader,text="⟳",
                             bg="Dark Grey", relief = tkinter.FLAT,
                             command=Refresh)
    RefreshButton.pack(padx=0, side=tkinter.RIGHT,anchor="e")
    return(ContactDisplayed)

def RenderRecentHeader():
    ContactDisplayed = tkinter.Label(master=RecentHeader,text="Recent Messages",
                                     bg="Dark Grey", relief = tkinter.FLAT)
    ContactDisplayed.pack(padx=0, side=tkinter.LEFT,anchor="w")
    ContactSetttings = tkinter.Button(master=RecentHeader,text="🛑",
                                     bg="Dark Grey", relief = tkinter.FLAT,
                                     command=ContactSettings)
    ContactSetttings.pack(padx=0, side=tkinter.RIGHT,anchor="e")
    RefreshButton = tkinter.Button(master=RecentHeader,text="⚙️",
                             bg="Dark Grey", relief = tkinter.FLAT,
                             command=Refresh)
    RefreshButton.pack(padx=0, side=tkinter.RIGHT,anchor="e")
    
def RenderRecentMessages():
    messages = RetriveRecentMessages()

def Resize(details):
    MaxCharacters = (details.width/50)-2
    RenderContactBar(MaxCharacters)
    

MainWindow = tkinter.Tk()
MainWindow.minsize(600,100)

# Border colors as suggested by
#https://code.activestate.com/recipes/580735-frame-with-border-color-for-tkinter/

### ROW 1 ###
FullWidth = tkinter.Frame(master=MainWindow) # Full width is a 0 height 100% width frame
FullWidth.grid(row=0, column=0, columnspan=3,sticky="ew")#used by contact bar to resize

### ROW 2 ###
#Column 1
#Dev note, combine button into frame
ContactsHeader = tkinter.Frame(master=MainWindow, bg="Dark Grey",
                               highlightbackground="black", highlightthickness=1)
ContactsHeader.grid(row=1, column=0, sticky="ew")

SendInviteButton = tkinter.Button(master=ContactsHeader, text="📨 Send Invite", bg="Dark Grey", 
                                  relief = tkinter.FLAT, command=SendInvite)
SendInviteButton.pack(side=tkinter.LEFT)
#Column 2
MessagesHeader = tkinter.Frame(master=MainWindow, bg="Dark Grey",
                               highlightbackground="black", highlightthickness=1)
MessagesHeader.grid(row=1, column=1, sticky="ew")
ContactDisplayed = RenderMessagesHeader()
#Column 3
RecentHeader = tkinter.Frame(master=MainWindow, bg="Dark Grey",
                               highlightbackground="black", highlightthickness=1)
RecentHeader.grid(row=1, column=2, sticky="ew")
RenderRecentHeader()
### ROW 3 ###
MainWindow.rowconfigure(2,weight=1) #resize the buttom row
#Column 1
MainWindow.columnconfigure(0, weight=1,minsize=150) #resize ContactBar
ContactBar = RenderContactBar(15)
FullWidth.bind("<Configure>",Resize)

#Column 2
MainWindow.columnconfigure(1, weight=2,minsize=300)
MessageList = tkinter.Frame(master=MainWindow)
MessageList.grid(row=2, column=1)
#Column 3
MainWindow.columnconfigure(2, weight=1,minsize=150)
RecentMessages = tkinter.Frame(master=MainWindow)
RecentMessages.grid(row=2, column=2)

MainWindow.mainloop()