import tkinter
from tkinter.filedialog import askopenfilename as selectfile
from tkinter.filedialog import asksaveasfilename as selectsavefile
from tkinter.simpledialog import askstring
from tkinter.font import Font

#from PIL import Image, ImageTk

import time

from Contacts import RetriveContacts, GetContactName, RetriveRecentMessages, RetriveMessages
from MainLibrary import CreateInvite, AcceptInvite, GetMessageText

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
    notice.grid(row=3, column=0, columnspan=3,sticky="ew")
    MainWindow.update_idletasks()
    for attempt in AcceptInvite(ContactName,InputFile): #CreateInvite uses yeild
        NoticeText.set("Generating Keypair, Attempt: "+attempt)
        MainWindow.update_idletasks()

def ContactSettings():
    print()

def Refresh():
    print()

def ContactFromList(details):
    global ContactButtons
    item = ContactButtons.curselection()[0]
    
    global ContactIDs
    ContactID = ContactIDs[item]
    DisplayContact(ContactID)

def ContactFromRecent(details):
    global RecentMessageList
    try:
        item = RecentMessageList.curselection()[0]
    except IndexError: #sometimes this function is called incorrectly and this error is thrown
        return() # so the function is simply terminated
    item = item // 3
    
    global RMContactIDs
    ContactID = RMContactIDs[item]
    DisplayContact(ContactID)

def DisplayImage(MessageID):
    print(MessageID)

def DisplayContact(ContactID):
    ContactName = GetContactName(ContactID)
    
    global ContactDisplayed
    ContactDisplayed.destroy()
    ContactDisplayed = tkinter.Label(master=MessagesHeader,text=ContactName,
                                     bg="Dark Grey", relief = tkinter.FLAT)
    ContactDisplayed.pack(padx=0, side=tkinter.LEFT,anchor="w")
    
    #blank existing message list
    global MessageListScrollBox
    for child in MessageListScrollBox.winfo_children():
        child.destroy()
    
    #global MessageListInner
    #MessageListInner.destroy()
    #MessageListInner = tkinter.Frame(master=MessageListScrollBox, bg="Light Grey")
    #MessageListInner.pack(fill=tkinter.X)
    
    messages = RetriveMessages(ContactID)
    for message in messages:
        MessageFrame = tkinter.Frame(MessageListScrollBox, bg="Dark Grey",
                                     highlightbackground="black", highlightthickness=1)
        if message[0] == 1:
            MessageFrom = "Me"
        else:
            MessageFrom = ContactName
        MessageFromLabel = tkinter.Label(master=MessageFrame,text=MessageFrom,
                                         bg="Dark Grey", relief = tkinter.FLAT,
                                         font="Arial 10 bold")
        MessageFromLabel.pack(anchor="w")
        ImageAddress = "messages/"+str(message[1])+".png"
        MessageImage = tkinter.PhotoImage(file = ImageAddress)
        width = MessageImage.width()
        subsample = int(width / 100)
        MessageImage = MessageImage.subsample(subsample)
        #MessageImage = ImageTk.PhotoImage(Image.open(ImageAddress))
        MessageImageButton = tkinter.Button(MessageFrame, image=MessageImage,
                                            command = lambda a=message[1]: DisplayImage(a),
                                            relief = tkinter.FLAT)
        MessageImageButton.image = MessageImage
        MessageImageButton.pack(anchor="w", padx=5)        
        MessageText = GetMessageText(message[1], message[3],message[2])
        MessageTextLabel = tkinter.Label(master=MessageFrame,text=MessageText,
                                         bg="Dark Grey", relief = tkinter.FLAT)
        MessageTextLabel.pack(anchor="w")
        
        MessageFrame.pack(pady = 5,fill=tkinter.X)

def RenderContactBar(MaxWidth):
    CourierNew = Font(family="Courier New")
    MaxCharacters = 15
    
    ContactBar = tkinter.Frame(master=MainWindow, bg="Light Grey",
                           highlightbackground="black",highlightthickness=1)
    ContactBar.grid(row=2, column=0,sticky="nsew")
    
    CScrollBar = tkinter.Scrollbar(ContactBar, orient=tkinter.VERTICAL)
    #Contact list:
    global ContactButtons
    ContactButtons = tkinter.Listbox(ContactBar, bg="Light Grey", relief = tkinter.FLAT,
                                     highlightthickness=0,selectbackground="Light Grey",
                                     fg = "black", selectforeground="black",
                                     activestyle="none", yscrollcommand=CScrollBar.set)
    CScrollBar.config(command=ContactButtons.yview)
    CScrollBar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
    ContactButtons.pack(padx=10, anchor="w", fill=tkinter.Y)
    
    global ContactIDs
    ContactIDs = []
    contacts = RetriveContacts()
    for contact in contacts:
        ContactName,ID = contact
        ContactIDs.append(ID)
        #if len(ContactName) > MaxCharacters:
            #ContactName = ContactName[0:int(MaxCharacters-3)]+"..." # Cut length of contact name
        
        ContactButtons.insert(tkinter.END, ContactName)
    ContactButtons.bind("<<ListboxSelect>>",ContactFromList)
    
    #Add contact button:
    AcceptInviteButton = tkinter.Button(master=ContactBar,text="➕ Accept Invite",
                                    bg="Light Grey", relief = tkinter.FLAT,
                                    command=OpenInvite)
    AcceptInviteButton.pack(padx=10, side=tkinter.TOP,anchor="w")
    return(ContactBar)

def RenderMessagesHeader():
    global ContactDisplayed
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
    MScrollBar = tkinter.Scrollbar(RecentMessages, orient=tkinter.VERTICAL)
    global RecentMessageList
    RecentMessageList = tkinter.Listbox(RecentMessages, bg="Light Grey", relief = tkinter.FLAT,
                                        highlightthickness=0,selectbackground="Light Grey",
                                        fg = "black", selectforeground="black",
                                        activestyle="none", yscrollcommand=MScrollBar.set)
    MScrollBar.config(command=RecentMessageList.yview)
    MScrollBar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
    RecentMessageList.pack(padx=10, anchor="w", fill=tkinter.Y)
    
    messages = RetriveRecentMessages()
    global RMContactIDs
    RMContactIDs = []
    for message in messages:
        RMContactIDs.append(message[4])
        RecentMessageList.insert(tkinter.END, message[3])
        MessageText = GetMessageText(message[0],message[1],message[2])
        MessageText.ljust(40)
        RecentMessageList.insert(tkinter.END, MessageText[:20])
        RecentMessageList.insert(tkinter.END, MessageText[21:40])
    
    RecentMessageList.bind("<<ListboxSelect>>",ContactFromRecent)

def CreateMessageList():
    MLScrollBar = tkinter.Scrollbar(MessageList, orient=tkinter.VERTICAL)
    global MessageListScrollBox
    MessageListScrollBox = tkinter.Canvas(MessageList, bg="Light Grey", relief = tkinter.FLAT,
                                          highlightthickness=0, yscrollcommand=MLScrollBar.set)
    MLScrollBar.config(command=MessageListScrollBox.yview)
    MLScrollBar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
    MessageListScrollBox.pack(fill=tkinter.BOTH,padx = 15, pady = 10)
    MessageListScrollBox.bind("<Configure>",
                              lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    global MessageListInner
    MessageListInner = tkinter.Frame(master=MessageListScrollBox, bg="Light Grey")
    MessageListInner.pack()
    
    #Dev Note: Send Message Box Here

def Resize(details):
    MaxCharacters = (details.width/50)-2
    RenderContactBar(MaxCharacters)
    
ContactDisplayedName = ""
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
MessageList = tkinter.Frame(master=MainWindow, bg="Light Grey",
                           highlightbackground="black",highlightthickness=1)
MessageList.grid(row=2, column=1, sticky="nsew")
CreateMessageList()
#Column 3
MainWindow.columnconfigure(2, weight=1,minsize=150)
RecentMessages = tkinter.Frame(master=MainWindow, bg="Light Grey",
                           highlightbackground="black",highlightthickness=1)
RecentMessages.grid(row=2, column=2, sticky="nsew")

MainWindow.update()
RenderRecentMessages()

MainWindow.mainloop()