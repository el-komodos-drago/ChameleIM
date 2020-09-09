import tkinter
from tkinter.filedialog import askopenfilename as selectfile
from tkinter.filedialog import asksaveasfilename as selectsavefile
from tkinter.simpledialog import askstring

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
    notice.grid(row=2, column=0, columnspan=3,sticky="ew")
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

def DisplayContact(ContactID):
    print(ContactID)

def RenderContactBar(MaxCharacters):
    ContactBar = tkinter.Frame(master=MainWindow, bg="Light Grey",
                           highlightbackground="black",highlightthickness=1)
    ContactBar.grid(row=1, column=0,sticky="nsew")
    
    #Contact list:
    ContactButtons = {}
    contacts = RetriveContacts()
    for contact in contacts:
        ContactName,ID = contact
        if len(ContactName) > MaxCharacters:
            ContactName = ContactName[0:MaxCharacters-3]+"..." # Cut length of contact name
        
        ContactButtons[ID] = tkinter.Button(master=ContactBar,text=ContactName,
                                            bg="Light Grey", relief = tkinter.FLAT,
                                            command=lambda a=ID: DisplayContact(a))
        ContactButtons[ID].pack(padx=10, side=tkinter.TOP,anchor="w")
    
    #Add contact button:
    AcceptInviteButton = tkinter.Button(master=ContactBar,text="➕ Accept Invite",
                                    bg="Light Grey", relief = tkinter.FLAT,
                                    command=OpenInvite)
    AcceptInviteButton.pack(padx=10, side=tkinter.TOP,anchor="w")
    return(ContactBar)

def Resize(details):
    MaxCharacters = (details.width/40)-2
    RenderContactBar(MaxCharacters)
    

MainWindow = tkinter.Tk()
MainWindow.minsize(600,100)

# Border colors as suggested by
#https://code.activestate.com/recipes/580735-frame-with-border-color-for-tkinter/

### ROW 1 ###
header = tkinter.Frame(master=MainWindow, bg="Dark Grey")
header.grid(row=0, column=0, columnspan=3,sticky="ew")
### ROW 2 ###
MainWindow.rowconfigure(1,weight=1) #resize the buttom row
#Column 1
MainWindow.columnconfigure(0, weight=1,minsize=150) #resize ContactBar
ContactBar = RenderContactBar(600)
header.bind("<Configure>",Resize)

#Column 2
MainWindow.columnconfigure(1, weight=2,minsize=300)
MessageList = tkinter.Frame(master=MainWindow)
MessageList.grid(row=1, column=1)
#Column 3
MainWindow.columnconfigure(2, weight=1,minsize=150)
RecentMessages = tkinter.Frame(master=MainWindow)
RecentMessages.grid(row=1, column=2)

SendInviteButton = tkinter.Button(master=header, text="📨 Send Invite", bg="Dark Grey", 
                                  highlightbackground="black", highlightthickness=1,
                                  relief = tkinter.SUNKEN, command=SendInvite)
SendInviteButton.config(highlightbackground="#000", highlightcolor="#000")
SendInviteButton.pack(side=tkinter.LEFT)

MainWindow.mainloop()