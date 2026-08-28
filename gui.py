import threading
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
import cedAnal
from staff import Staff

staffList = []
staffListStringList = []


def addStaff(member, staffCombobox):
    staffList.append(member)
    staffListStringList.append(str(member))
    staffCombobox["values"] = staffListStringList


def update_new_staff_combobox_api(cedCombo, steamCombo):
    print("making request")
    cedmodStaffList, steamStaffList = cedAnal.get_list_of_staff()

    cedCombo["values"] = cedmodStaffList
    steamCombo["values"] = steamStaffList


def staffSelected(staffCombobox, staffInfoText):
    staffIndex = staffCombobox.current()
    staffInfoText.set(staffList[staffIndex].to_string())
    print(staffList[staffIndex].to_string())


def on_new_staff_save(staffCombobox, steamIDpos, cedmodIDpos, root, steamList, cedmodList, altName=None):
    steamID = steamList[steamIDpos]
    cedmodID = cedmodList[cedmodIDpos]

    member = Staff()

    if steamIDpos != -1:
        member.set_steam_id(cedAnal.extract_steam_id(steamID))
        member.set_name(steamID)

    if cedmodIDpos != -1:
        member.set_cedmod_name(cedmodID)
        if member.name == "NaN":
            member.set_name(cedmodID)

    if altName is not None:
        member.altName = altName

    addStaff(member, staffCombobox)
    root.destroy()


def popup_new_staff(mainWindow, staffCombobox):
    root = Toplevel(mainWindow)

    content = ttk.Frame(root, padding=(6, 6, 12, 12))

    steamIDComboBox = ttk.Combobox(content, width=50)
    cedmodNameComboBox = ttk.Combobox(content, width=30)

    threading.Thread(target=update_new_staff_combobox_api, args=(cedmodNameComboBox, steamIDComboBox)).start()

    steamIDLabel = ttk.Label(content, text="SteamID")
    cedmodNameLabel = ttk.Label(content, text="Cedmod Name")

    saveButton = ttk.Button(content, text="Save", command=lambda: on_new_staff_save(staffCombobox=staffCombobox,
                                                                                    steamIDpos=steamIDComboBox.current(),
                                                                                    cedmodIDpos=cedmodNameComboBox.current(),
                                                                                    root=root,
                                                                                    steamList=steamIDComboBox["values"],
                                                                                    cedmodList=cedmodNameComboBox[
                                                                                        "values"]))
    abortButton = ttk.Button(content, text="Abort", command=root.destroy)

    # ---

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    content.rowconfigure(3, weight=1)
    content.rowconfigure(1, weight=3)
    content.columnconfigure(0, weight=1)
    content.columnconfigure(5, weight=1)

    # ---

    content.grid(column=0, row=0, sticky=NSEW)

    steamIDLabel.grid(column=0, row=1, sticky=NSEW)
    cedmodNameLabel.grid(column=5, row=1, sticky=NSEW)
    steamIDComboBox.grid(column=0, row=3, sticky=EW, padx=5)
    cedmodNameComboBox.grid(column=5, row=3, sticky=EW, padx=5)
    saveButton.grid(column=5, row=5, sticky=S)
    abortButton.grid(column=0, row=5, sticky=S)

    root.mainloop()


# ------

def display_stats_window():
    root = Tk()
    root.title("Cedmod stats")
    root.minsize(250, 50)

    staffInfoText = StringVar(
        value="SteamID:\nCedmod Name:\nBans: | Warns: \nPlaytime: \nReports Handled: \n Reports Ignored: " + "\nDays since last connection: TODO")

    content = ttk.Frame(root, padding=(3, 3, 12, 12))
    staffCombobox = ttk.Combobox(content, values=staffListStringList, font=Font(size=10))

    staffInfoLabel = ttk.Label(content, textvariable=staffInfoText, padding=(12, 12, 24, 24), font=Font(size=15))

    newMenu = ttk.Button(content, text="Add Staff", command=lambda: popup_new_staff(root, staffCombobox))

    staffCombobox.bind("<<ComboboxSelected>>", lambda e: staffSelected(staffCombobox, staffInfoText))

    content.columnconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    content.rowconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    content.grid(column=0, row=0, sticky=NSEW)
    staffCombobox.grid(column=0, row=0, sticky=EW)
    staffInfoLabel.grid(column=0, row=1, sticky=NSEW)
    newMenu.grid(column=1, row=0, sticky=E)

    root.mainloop()


display_stats_window()
