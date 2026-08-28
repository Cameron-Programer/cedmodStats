from tkinter import *
from tkinter import ttk
import cedAnal
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

def addStaff(member,staffCombobox):
    staffList.append(member)
    staffListStringList.append(str(member))
    staffCombobox["values"] = staffListStringList



def staffSelected(staffCombobox,staffInfoText):
    staffIndex = staffCombobox.current()
    staffInfoText.set(staffList[staffIndex].to_string())


def on_new_staff_save(staffCombobox,steamID,cedmodID,root,steamList,cedmodList,altName=None):
    steamID = steamList[steamID]
    cedmodID = cedmodList[cedmodID]

    member = Staff()
    member.set_steam_id(cedAnal.extract_steam_id(steamID))
    member.set_cedmod_name(cedmodID)
    member.set_name(steamID)
    if altName is not None:
        member.altName = altName

    addStaff(member,staffCombobox)
    root.destroy()



def popup_new_staff(mainWindow, staffCombobox):
    root = Toplevel(mainWindow)

    cedmodStaffList,steamStaffList = cedAnal.get_list_of_staff()

    content = ttk.Frame(root,padding=(6,6,12,12))

    steamIDLabel = ttk.Label(content,text="SteamID")
    cedmodNameLabel = ttk.Label(content,text="Cedmod Name")

    steamIDComboBox = ttk.Combobox(content,values=steamStaffList,width=50)
    cedmodNameComboBox = ttk.Combobox(content,values=cedmodStaffList,width=30)


    saveButton = ttk.Button(content,text="Save",command=lambda: on_new_staff_save(staffCombobox=staffCombobox,steamID=steamIDComboBox.current(),cedmodID=cedmodNameComboBox.current(),root=root,steamList=steamStaffList,cedmodList=cedmodStaffList))
    abortButton = ttk.Button(content,text="Abort",command=root.destroy)

    #---

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    content.rowconfigure(3,weight=1)
    content.rowconfigure(1, weight=3)
    content.columnconfigure(0, weight=1)
    content.columnconfigure(5, weight=1)

    #---

    content.grid(column=0,row=0,sticky=NSEW)

    steamIDLabel.grid(column=0,row=1,sticky=NSEW)
    cedmodNameLabel.grid(column=5,row=1,sticky=NSEW)
    steamIDComboBox.grid(column=0,row=3,sticky=EW,padx=5)
    cedmodNameComboBox.grid(column=5,row=3,sticky=EW,padx=5)
    saveButton.grid(column=5,row=5,sticky=S)
    abortButton.grid(column=0,row=5,sticky=S)


    root.mainloop()

# ------

def display_stats_window():
    staffInfoText = StringVar(value="SteamID:\nCedmod Name:\nBans: | Warns: \nPlaytime: \nReports Handled: \n Reports Ignored: "+"\nDays since last connection: TODO")

    content = ttk.Frame(root,padding=(3,3,12,12))
    staffCombobox = ttk.Combobox(content, values=staffListStringList)
    staffInfoLabel = ttk.Label(content, textvariable=staffInfoText, padding=(12, 12, 24, 24))

    newMenu = ttk.Button(content,text="Add Staff",command=lambda:popup_new_staff(root,staffCombobox))

    staffCombobox.bind("<<ComboboxSelected>>",lambda e: staffSelected(staffCombobox,staffInfoText))

    content.columnconfigure(0,weight=1)
    root.columnconfigure(0,weight=1)
    content.rowconfigure(0,weight=1)
    root.rowconfigure(0,weight=1)

    content.grid(column=0, row=0,sticky=NSEW)
    staffCombobox.grid(column=0, row=0,sticky=EW)
    staffInfoLabel.grid(column=0, row=1, sticky=NSEW)
    newMenu.grid(column=1, row=0,sticky=E)

    root.mainloop()

display_stats_window()

