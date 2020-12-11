#Version 0.1.0
import tkinter
from tkinter.filedialog import askopenfilename as selectfile
from tkinter.filedialog import asksaveasfilename as selectsavefile
from tkinter.simpledialog import askstring
from tkinter.font import Font

import json

import time

from Contacts import RetriveContacts, GetContactName, RetriveRecentMessages, RetriveMessages
from Contacts import LatestMessageMine, GetContactKey, RetriveContactIDs
from MainLibrary import CreateInvite, AcceptInvite, GetMessageText,SendMessage,CreateKeypair
from MainLibrary import PollMessages, OpenMessage

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
    Unsent = True
    while Unsent:
        if InputFile == "":
            return()
        try:
            for progress in CreateInvite(ContactName,InputFile,OutputFile): #CreateInvite uses yeild
                NoticeText.set(progress)
                MainWindow.update_idletasks()
            Unsent = False
        except Exception:
            message = "Sorry but the image you selected was not big enough to store "
            message = message + "the invite in. Press ok to select a new image."
            tkinter.messagebox.showinfo(message=message)
            InputFile = selectfile(title="Select image to hide invite in",
                                   filetypes=(("png files","*.png"),))
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
    
    NoticeText = tkinter.StringVar()
    notice = tkinter.Label(master=MainWindow, textvariable=NoticeText)
    notice.grid(row=3, column=0, columnspan=3,sticky="ew")
    MainWindow.update_idletasks()
    Unsent, FirstTry,OutputFile = True, True,InputFile
    while Unsent:
        if InputFile == "":
            return()
        try:
            for attempt in AcceptInvite(ContactName,InputFile,OutputFile): #CreateInvite uses yeild
                NoticeText.set(attempt)
                MainWindow.update_idletasks()
            Unsent = False
            notice.destroy()
        except TypeError:
            raise
            return()
        except Exception as exception:
            if FirstTry:
                message = "Sorry but the image contained in the invite was not big enough "
            else:
                message = "Sorry but the image you selected was not big enough "
            FirstTry = False
            message = message + "to hide the reply in. Press ok to select a new image."
            tkinter.messagebox.showinfo(message=message)
            OutputFile = selectfile(title="Select image to hide invite in",
                                    filetypes=(("png files","*.png"),))

    RenderContactBar()

def SendMessageGUI():
    #This function processes entries into the Send Message Field text box.
    global ContactID
    if ContactID == 1:
        return()
    PKID, PublicKey, Max, IDpw = GetContactKey(ContactID)
    
    if Max == "1": #if the first key hasn't been recieved then don't allow a message to be sent
        message = "Sorry but that contact hasn't opened your invite yet. "
        message = message + "As a result you can't send them messages"
        tkinter.messagebox.showinfo(message=message)
        return()
    
    global SendMessageField
    text = SendMessageField.get()
    
    InputFile = selectfile(title="Select image to hide invite in",
                           filetypes=(("png files","*.png"),))
    if InputFile == "": # InputFile will be empty if cancel was clicked.
        return()
    
    #Get contents for message:
    LMM = LatestMessageMine(ContactID)
    if LMM == 0: # generate new keypair
        NoticeText = tkinter.StringVar()
        notice = tkinter.Label(master=MainWindow, textvariable=NoticeText)
        notice.grid(row=3, column=0, columnspan=3,sticky="ew")
        MainWindow.update_idletasks()

        for ReturnedData in CreateKeypair(ContactID): # Create Keypair to send
            if type(ReturnedData) is str:
                NoticeText.set(ReturnedData)
                MainWindow.update_idletasks()
            else:
                MyPublicKeyID,MyPublicKey,MyMax = ReturnedData
        
        notice.destroy()
        message = json.dumps([text,MyPublicKeyID,MyPublicKey,MyMax])
    else:
        message = json.dumps([text])
        print(message)
    
    SendMessageField.delete(0, tkinter.END)
    
    #Send message contents:
    Unsent = True
    while Unsent:
        if InputFile == "":
            return()
        try:
            for attempt in SendMessage(InputFile,message,IDpw,PublicKey,Max,ContactID, PKID):
                NoticeText.set(attempt)
                MainWindow.update_idletasks()
            Unsent = False
            notice.destroy()
        except TypeError: #in the event of a networking error ...
            raise #... do not handle this (as it should not occur) ...
            return() #... and don't let the next statement handle it either
        except Exception as exception:
            message = "Sorry but the image you selected was not big enough "
            message = message + "to hide the reply in. Press ok to select a new image."
            tkinter.messagebox.showinfo(message=message)
            OutputFile = selectfile(title="Select image to hide invite in",
                                    filetypes=(("png files","*.png"),))
    
    

def ContactSettings():
    print()

def ContactFromList(details):
    global ContactButtons
    item = ContactButtons.curselection()[0]
    
    global ContactIDs
    global ContactID
    ContactID = ContactIDs[item]
    DisplayContact()

def ContactFromRecent(details):
    global RecentMessageList
    try:
        item = RecentMessageList.curselection()[0]
    except IndexError: #sometimes this function is called incorrectly and this error is thrown
        return() # so the function is simply terminated
    item = item // 3
    
    global RMContactIDs
    global ContactID
    ContactID = RMContactIDs[item]
    DisplayContact()

def DisplayImage(MessageID):
    print(MessageID)

def RenderMessage(message,ContactName):
    MessageFrame = tkinter.Frame(MessageListInner, bg="Dark Grey",
                                     highlightbackground="black", highlightthickness=0)
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
    subsample = int(width / 200)
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
    return(MessageFrame)

def Refresh():
    contacts = RetriveContactIDs()
    
    global ContactID
    if ContactID != 1: #Priorities the open contact
        contacts.remove(ContactID) #Remove them from the list of contracts to poll for
        MessageTexts = PollMessages(ContactID)
        for FileName in FileNames:
            MessageText = OpenMessage(FileName)
            MessageTexts.append(MessageText)
        
    
    for contact in contacts:
        PollMessages(contact[0])

def DisplayContact():
    global ContactID 
    ContactName = GetContactName(ContactID)
    
    global ContactDisplayed
    ContactDisplayed.destroy()
    ContactDisplayed = tkinter.Label(master=MessagesHeader,text=ContactName,
                                     bg="Dark Grey", relief = tkinter.FLAT)
    ContactDisplayed.pack(padx=0, side=tkinter.LEFT,anchor="w")
    
    #blank existing message list
    #global MessageListScrollBox
    global MessageListInner
    for child in MessageListInner.winfo_children():
        child.destroy()
    
    #create very wide widget to ensure correct rendering
    text="----------------------------------------------------------------------------------"
    for i in range(10):
        text = text + "---------------------------------------------------------------------"
        FillWidth = tkinter.Label(MessageListInner,text=text, fg="Light Grey", bg="Light Grey")
    FillWidth.pack()
    
    #progress info here
    messages = RetriveMessages(ContactID)
    for message in messages:
        MessageFrame = RenderMessage(message,ContactName)
        MessageFrame.pack(pady = 5,fill=tkinter.X)
        MainWindow.update_idletasks()

def CreateInviteButton():
    SendInviteButton = tkinter.Button(master=ContactsHeader, text="📨 Send Invite", bg="Dark Grey", 
                                  relief = tkinter.FLAT, command=SendInvite)
    SendInviteButton.pack(side=tkinter.LEFT)

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

def RenderContactBar(MaxWidth = 15):
    # CourierNew = Font(family="Courier New")
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

def CreateMessageList():
    #Code based on https://blog.tecladocode.com/tkinter-scrollable-frames/ 
    MessageListScrollBox = tkinter.Canvas(MessageList, bg="Light Grey", highlightthickness=0)
    MLScrollBar = tkinter.Scrollbar(MessageList, orient="vertical",
                                    command=MessageListScrollBox.yview)
    global MessageListInner
    MessageListInner = tkinter.Frame(MessageListScrollBox, bg="Light Grey")

    MessageListInner.bind("<Configure>", lambda e: MessageListScrollBox.configure(
                          scrollregion=MessageListScrollBox.bbox("all")))

    MessageListScrollBox.create_window((0, 0), window=MessageListInner, anchor="nw")

    MessageListScrollBox.configure(yscrollcommand=MLScrollBar.set)
    
    MessageListScrollBox.grid(row=0, column=0, padx = 15, pady = 10,
                              sticky="nesw")
    MLScrollBar.grid(row=0, column=1, sticky="ns")
    MessageList.columnconfigure(0, weight=1)
    MessageList.rowconfigure(0, weight=1)
    #MessageListScrollBox.pack(padx = 15, pady = 10, side="top", fill="both", expand=True)
    #MLScrollBar.pack(side="right", fill="y")
    
    #Send Message Box
    SendMessageFrame = tkinter.Frame(MessageList, bg = "white", highlightbackground = "black",
                                     highlightthickness = 1)
    SendMessageFrame.grid(row=1,column=0, columnspan=2,sticky="nsew", padx = 10, pady = 10)
    #SendMessageFrame.pack(side="top",anchor="w", fill = "x", padx = 10, pady = 10)
    global SendMessageField
    SendMessageField = tkinter.Entry(SendMessageFrame, bg="white")
    SendMessageField.pack(fill="x",anchor="w",side="left",padx = 5)
    SendMessageButton = tkinter.Button(SendMessageFrame, bg = "white", relief="flat",
                                        text="✈",command=SendMessageGUI)
    SendMessageButton.pack(anchor="e",side="right")
    
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
        print(message)
        RMContactIDs.append(message[4])
        RecentMessageList.insert(tkinter.END, message[3])
        MessageText = GetMessageText(message[0],message[1],message[2])
        MessageText.ljust(40)
        RecentMessageList.insert(tkinter.END, MessageText[:20])
        RecentMessageList.insert(tkinter.END, MessageText[21:40])
    
    RecentMessageList.bind("<<ListboxSelect>>",ContactFromRecent)

def Resize(details):
    MaxCharacters = (details.width/50)-2
    RenderContactBar(MaxCharacters)

ContactID=1
ContactDisplayedName = ""
MainWindow = tkinter.Tk()
MainWindow.minsize(600,100)
MainWindow.title("Alice's ChameleIM")

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
CreateInviteButton()

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