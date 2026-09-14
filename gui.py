import threading
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
import cedAnalysis
from staff import Staff

staffList = []
staffListStringList = []


def addStaff(member, staffCombobox):
    staffList.append(member)
    staffListStringList.append(str(member))
    staffCombobox["values"] = staffListStringList


def update_new_staff_combobox_api(cedCombo, steamCombo):
    print("making request")
    cedmodStaffList, steamStaffList = cedAnalysis.get_list_of_staff()
    print("Request Finished")

    cedCombo["values"] = cedmodStaffList
    steamCombo["values"] = steamStaffList


def staffSelected(staffCombobox, staffInfoText):
    staffIndex = staffCombobox.current()
    staffInfoText.set(staffList[staffIndex].to_string())


def on_new_staff_save(staffCombobox, steamIDpos, cedmodIDpos, root, steamList, cedmodList, altName=None):
    steamID = steamList[steamIDpos]
    cedmodID = cedmodList[cedmodIDpos]

    member = Staff()

    if steamIDpos != -1:
        member.set_steam_id(cedAnalysis.extract_steam_id(steamID))
        member.set_name(steamID)

    if cedmodIDpos != -1:
        member.set_cedmod_name(cedmodID)
        if member.name == "NaN":
            member.set_name(cedmodID)

    if altName is not None:
        member.altName = altName

    addStaff(member, staffCombobox)
    root.destroy()


def popup_new_staff(mainWindow, staffCombobox, listOfStaffCombined):
    root = Toplevel(mainWindow)
    content = ttk.Frame(root, padding=(6, 6, 12, 12))

    cedmodStaffList, steamStaffList = listOfStaffCombined

    steamIDComboBox = ttk.Combobox(content, values=steamStaffList, width=50)
    cedmodNameComboBox = ttk.Combobox(content, values=cedmodStaffList, width=30)

    steamIDLabel = ttk.Label(content, text="SteamID")
    cedmodNameLabel = ttk.Label(content, text="Cedmod Name")
    titleLabel = ttk.Label(content, text="New staff registration menu", font=Font(size=15))

    saveButton = ttk.Button(content, text="Save", command=lambda: on_new_staff_save(staffCombobox=staffCombobox,
                                                                                    steamIDpos=steamIDComboBox.current(),
                                                                                    cedmodIDpos=cedmodNameComboBox.current(),
                                                                                    root=root,
                                                                                    steamList=steamIDComboBox["values"],
                                                                                    cedmodList=cedmodNameComboBox[
                                                                                        "values"]))
    abortButton = ttk.Button(content, text="Cancel", command=root.destroy)

    # ---

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    content.rowconfigure(3, weight=1)
    content.rowconfigure(1, weight=3)
    content.columnconfigure(0, weight=1)
    content.columnconfigure(5, weight=1)

    # ---

    content.grid(column=0, row=0, sticky=NSEW)
    titleLabel.grid(column=0, row=0)
    steamIDLabel.grid(column=0, row=1, sticky=NSEW)
    cedmodNameLabel.grid(column=5, row=1, sticky=NSEW)
    steamIDComboBox.grid(column=0, row=3, sticky=EW, padx=5)
    cedmodNameComboBox.grid(column=5, row=3, sticky=EW, padx=5)
    saveButton.grid(column=5, row=5, sticky=S)
    abortButton.grid(column=0, row=5, sticky=S)

    root.mainloop()


# ------

def display_stats_window(mainWidnow, staffInfoText):
    root = Toplevel(mainWidnow)
    root.title("Cedmod stats")
    root.minsize(250, 50)

    content = ttk.Frame(root, padding=(3, 3, 12, 12))

    staffInfoLabel = ttk.Label(content, text=staffInfoText.get(), padding=(12, 12, 24, 24), font=Font(size=15))
    closeButton = ttk.Button(content, text="Close", command=root.destroy)

    content.columnconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    content.rowconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    content.rowconfigure(1, weight=3)

    content.grid(column=0, row=0, sticky=NSEW)
    staffInfoLabel.grid(column=0, row=0, sticky=NSEW)
    closeButton.grid(column=0, row=1, sticky=S)

    root.mainloop()


def display_settings_window(mainWindow):
    def validate_key(key):
        print("2")

    root = Toplevel(mainWindow)

    content = ttk.Frame(root, padding=(3, 3, 12, 12))

    apiLabel = ttk.Label(content, text="API Key")
    apiEntry = ttk.Entry(content)
    # TODO add methord to enter API key here

    saveButton = ttk.Button(content, text="Save", )
    closeButton = ttk.Button(content, text="Close")

    content.columnconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    content.rowconfigure(0, weight=1)

    content.columnconfigure(1, weight=1)
    content.rowconfigure(1, weight=1)
    content.rowconfigure(2, weight=1)

    content.grid(column=0, row=0)
    apiLabel.grid(column=0, row=1)
    apiEntry.grid(column=1, row=1)
    saveButton.grid(column=1, row=2)
    closeButton.grid(column=0, row=2)


def refresh_stats(refreshDataButton):
    print("GUI: Refreshing Stats")
    threadList = [threading.Thread(target=cedAnalysis.add_bans_to_staff, args=((staffList,))),
    threading.Thread(target=cedAnalysis.add_warns_to_staff, args=((staffList,))),
    threading.Thread(target=cedAnalysis.add_playtime_to_staff, args=((staffList,))),
    threading.Thread(target=cedAnalysis.add_deta_to_staff, args=((staffList,))),
    threading.Thread(target=cedAnalysis.add_reports_to_staff, args=((staffList,)))
    ]
    for thread in threadList:
        thread.start()

    for thread in threadList:
        thread.join()

def display_main_menu():
    root = Tk()
    root.title("Cedmod stats")
    root.minsize(350, 80)

    content = ttk.Frame(root, padding=(3, 3, 12, 12))
    staffCombobox = ttk.Combobox(content, values=staffListStringList, font=Font(size=10))

    staffInfoText = StringVar(
        value="Name: ⚠️ No user has been selected \nSteamID:\nCedmod Name:\nBans: | Warns: \nPlaytime: \nReports Handled: \nReports Ignored: " + "\nDays since last connection: TODO")

    APIKey = StringVar(value="Bearer ")

    showStatsButton = ttk.Button(content, text="Show Stats", command=lambda: display_stats_window(root, staffInfoText))

    refreshDataButton = ttk.Button(content, text="Refresh Data", command=lambda: refresh_stats(refreshDataButton))
    settingsButton = ttk.Button(content, text="Settings", command=lambda: display_settings_window(root))

    nameLabel = Label(content, text="Cedmod Stats Menu")

    staffCombobox.bind("<<ComboboxSelected>>", lambda e: staffSelected(staffCombobox, staffInfoText))

    listOfStaffCombined = cedAnalysis.get_list_of_staff()
    newStaffButton = ttk.Button(content, text="Add Staff", command=lambda: popup_new_staff(root, staffCombobox, listOfStaffCombined))

    content.columnconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    content.rowconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    content.grid(column=0, row=0, sticky=NSEW)
    nameLabel.grid(column=0, row=0)
    staffCombobox.grid(column=0, row=1, sticky=EW)
    newStaffButton.grid(column=5, row=0, )
    showStatsButton.grid(column=5, row=1)
    refreshDataButton.grid(column=10, row=0)
    settingsButton.grid(column=10, row=1)

    root.mainloop()


display_main_menu()
