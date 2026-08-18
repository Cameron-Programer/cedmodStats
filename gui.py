from tkinter import *
from tkinter import ttk
from staff import Staff

root = Tk()
root.title("Cedmod stats")
root.minsize(250,50)

exampleStaff = Staff()

exampleStaff.set_name("John Unia ")
exampleStaff.set_steam_id("76561198058985031@steam")
exampleStaff.set_cedmod_name("uniaaa")

exampleStaff2 = Staff()
exampleStaff2.set_name("John Cameron")
exampleStaff2.set_steam_id("76561198259540599@steam")
exampleStaff2.set_cedmod_name("gbcameron")


staffList = [exampleStaff,exampleStaff2]
staffListStringList = []

for i in range (0,len(staffList)):
    staffListStringList.append(str(staffList[i]))



def staffSelected(args):
    staffIndex = staffCombobox.current()
    staffInfoText.set(staffList[staffIndex].to_string())


# ------
staffInfoText = StringVar(value="SteamID:\nCedmod Name:\nBans: | Warns: \nPlaytime: \nReports Handled: \n Reports Ignored: "+"\nDays since last connection: TODO")


content = ttk.Frame(root,padding=(3,3,12,12))
staffCombobox = ttk.Combobox(content, values=staffListStringList)
staffInfoLable = ttk.Label(content, textvariable=staffInfoText,padding=(12,12,24,24))

staffCombobox.bind("<<ComboboxSelected>>", staffSelected)

content.columnconfigure(0,weight=1)
root.columnconfigure(0,weight=1)
content.rowconfigure(0,weight=1)
root.rowconfigure(0,weight=1)

content.grid(column=0, row=0,sticky=NSEW)
staffCombobox.grid(column=0, row=0,sticky=EW)
staffInfoLable.grid(column=0, row=1,sticky=NSEW)

root.mainloop()
