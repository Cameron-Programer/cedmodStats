import threading
##TTK
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
#Date and time managment
import datetime as dt
from calendar import monthrange
#Project functions and classes
import requests.exceptions

import cedAnalysis
from staff import Staff

#---

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


def on_new_staff_save(cedmodID, steamID, staffCombobox,root):
    member = Staff()

    member.set_steam_id(cedAnalysis.extract_steam_id(steamID))
    member.set_name(steamID)

    member.set_cedmod_name(cedmodID)
    if member.cedmodName =="":
        member.set_cedmod_name("NaN")

    if member.name == "NaN":
        member.set_name(cedmodID)

    addStaff(member, staffCombobox)
    root.destroy()


def refresh_stats(dateLimit,bans=True,warns=True,reports=True,playtime=True):
    print("GUI: Refreshing Stats")

    threadList = []
    if bans:
        threadList.append(threading.Thread(target=cedAnalysis.add_bans_to_staff, args=((staffList,))))
    if warns:
        threadList.append(threading.Thread(target=cedAnalysis.add_warns_to_staff, args=((staffList,))))
    if reports:
        threadList.append(threading.Thread(target=cedAnalysis.add_reports_to_staff, args=((staffList,))))
    if playtime:
        threadList.append(threading.Thread(target=cedAnalysis.add_playtime_to_staff, args=((staffList,))))
        threadList.append(threading.Thread(target=cedAnalysis.add_deta_to_staff, args=((staffList,))))

    for thread in threadList:
        thread.start()

    for thread in threadList:
        thread.join()


def popup_new_staff(mainWindow, staffCombobox, listOfStaffCombined):
    root = Toplevel(mainWindow)
    content = ttk.Frame(root, padding=(6, 6, 12, 12))

    cedmodStaffList, steamStaffList = listOfStaffCombined

    steamIDComboBox = ttk.Combobox(content, values=steamStaffList, width=50)
    cedmodNameComboBox = ttk.Combobox(content, values=cedmodStaffList, width=30)

    steamIDLabel = ttk.Label(content, text="SteamID")
    cedmodNameLabel = ttk.Label(content, text="Cedmod Name")
    titleLabel = ttk.Label(content, text="New staff registration menu", font=Font(size=15))

    saveButton = ttk.Button(content, text="Save", command=lambda: on_new_staff_save(steamID=steamIDComboBox.get(),
                                                                                    cedmodID=cedmodNameComboBox.get(),
                                                                                    staffCombobox=staffCombobox,
                                                                                    root=root))

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

def display_stats_window(mainWidnow, staff:Staff):
    root = Toplevel(mainWidnow)
    root.title("Cedmod stats")
    root.minsize(250, 50)
    statsFont = Font(size=10)

    content = ttk.Frame(root, padding=(3, 3, 12, 12))

    closeButton = ttk.Button(content, text="Close", command=root.destroy)

    nameLabel = ttk.Label(content,text=str("Name: "+staff.name),font=Font(size=15))
    steamIDLabel = ttk.Label(content,text=str("SteamID: "+staff.steamID),font=statsFont)
    cedmodNameLabel = ttk.Label(content,text=str("Cedmod name: "+staff.cedmodName),font=statsFont)
    banLabel = ttk.Label(content,text=str("Bans: "+str(staff.bans)),font=statsFont)
    warnLabel = ttk.Label(content,text=str("Warns: "+str(staff.warns)),font=statsFont)
    playtimeLabel = ttk.Label(content,text=str("Playtime: "+str(staff.playtime)),font=statsFont)
    ignoredLabel = ttk.Label(content,text=str("Reports ignored: "+str(staff.reportsIgnored)),font=statsFont)
    handledLabel = ttk.Label(content,text=str("Reports handled: "+str(staff.reportsHandled)),font=statsFont)
    lastConnectionLabel = ttk.Label(content,text=str("Days since last connection: "+str(staff.daysSinceConnection)),font=statsFont)

    content.columnconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    content.rowconfigure(0, weight=1)
    content.rowconfigure(1, weight=2)

    content.rowconfigure(10, weight=3)

    content.columnconfigure(0, weight=1)
    content.columnconfigure(1, weight=1)

    content.grid(column=0, row=0, sticky=NSEW)

    nameLabel.grid(column=0,row=1,padx=5,pady=2,columnspan=2)

    steamIDLabel.grid(column=0,row=2,padx=5,pady=2)
    cedmodNameLabel.grid(column=1,row=2,padx=5,pady=2)

    banLabel.grid(column=0,row=4,pady=2)
    warnLabel.grid(column=1,row=4,pady=2)

    playtimeLabel.grid(column=0,row=5,padx=5,pady=2)
    lastConnectionLabel.grid(column=1, row=5, padx=5, pady=2)

    ignoredLabel.grid(column=0,row=6,padx=5,pady=2)
    handledLabel.grid(column=1,row=6,padx=5,pady=2)

    closeButton.grid(column=0, row=10, sticky=S,columnspan=2,padx=5,pady=5)

    root.mainloop()

#---


def updateDayComboList(year,month,dayCombo):
    if (month != "") and (year != ""):
        year = int(year)
        month = int(month)
        weekday,daysInMonth = monthrange(year=year,month=month)
        dayCombo["values"] = cedAnalysis.get_list_of_days(max=daysInMonth)
    else:
        print("GUI: Error, invalid month or year ")


def display_request_data_window(mainwindow):
    root = Toplevel(mainwindow)
    root.title("Cedmod stats")
    root.minsize(350, 80)

    content = ttk.Frame(root, padding=(3, 3, 12, 12))

    rangeLabel = ttk.Label(content,text="Include reports up to:")#
    typeLabel = ttk.Label(content,text="Include:")

    yearLabel = ttk.Label(content,text="Year")
    monthLabel = ttk.Label(content,text="Month")
    dayLabel = ttk.Label(content,text="Day")
    yearCombo = ttk.Combobox(content, values=cedAnalysis.get_list_of_years())
    monthCombo = ttk.Combobox(content,values=cedAnalysis.get_list_of_months())
    dayCombo = ttk.Combobox(content, values=["Select month and year first"])

    bans = BooleanVar(value=False)
    warns = BooleanVar(value=False)
    reports = BooleanVar(value=False)
    playtime = BooleanVar(value=False)

    warnsCheck = ttk.Checkbutton(content,text="Warns",variable=warns,onvalue=True,offvalue=False)
    bansCheck = ttk.Checkbutton(content,text="Bans",variable=bans,onvalue=True,offvalue=False)
    reportsCheck = ttk.Checkbutton(content,text="Reports",variable=reports,onvalue=True,offvalue=False)
    playtimeCheck = ttk.Checkbutton(content,text="Playtime",variable=playtime,onvalue=True,offvalue=False)

    requestButton = ttk.Button(content,text="Make request",command=lambda: refresh_stats(dt.datetime(year=int(yearCombo.get()),month=int(monthCombo.get()),day=int(dayCombo.get())),bans.get(),warns.get(),reports.get(),playtime.get()))
    abortButton = ttk.Button(content,text="Abort")

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    content.grid(column=1, row=1, sticky=NSEW)

    yearLabel.grid(column=1,row=1,sticky=S)
    monthLabel.grid(column=2,row=1,sticky=S)
    dayLabel.grid(column=3,row=1,sticky=S)

    rangeLabel.grid(column=0, row=2, sticky=W,padx=5,pady=5)
    yearCombo.grid(column=1,row=2,sticky=N)
    monthCombo.grid(column=2,row=2,sticky=N)
    dayCombo.grid(column=3, row=2, sticky=N)

    typeLabel.grid(column=0,row=3,sticky=W,padx=5,pady=5)
    warnsCheck.grid(column=1,row=3,sticky=NSEW)
    bansCheck.grid(column=2,row=3,sticky=NSEW)
    reportsCheck.grid(column=3,row=3,sticky=NSEW)
    playtimeCheck.grid(column=4,row=3,sticky=NSEW)

    abortButton.grid(column=1,row=4,sticky=S)
    requestButton.grid(column=2, row=4, sticky=S)

    monthCombo.bind('<<ComboboxSelected>>',lambda x: updateDayComboList(yearCombo.get(),monthCombo.get(),dayCombo))
    yearCombo.bind('<<ComboboxSelected>>',lambda x: updateDayComboList(yearCombo.get(),monthCombo.get(),dayCombo))

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


def display_main_menu():
    root = Tk()
    root.title("Cedmod stats")
    root.minsize(350, 80)

    content = ttk.Frame(root, padding=(3, 3, 12, 12))
    staffCombobox = ttk.Combobox(content, values=staffListStringList, font=Font(size=10))

    staffInfoText = StringVar(
        value="Name: ⚠️ No user has been selected \nSteamID:\nCedmod Name:\nBans: | Warns: \nPlaytime: \nReports Handled: \nReports Ignored: " + "\nDays since last connection: TODO")

    APIKey = StringVar(value="Bearer ")

    showStatsButton = ttk.Button(content, text="Show Stats", command=lambda: display_stats_window(root,staffList[staffCombobox.current()]))

    refreshDataButton = ttk.Button(content, text="Refresh Data", command=lambda: display_request_data_window(root))
    settingsButton = ttk.Button(content, text="Settings", command=lambda: display_settings_window(root))

    nameLabel = Label(content, text="Cedmod Stats Menu")

    staffCombobox.bind("<<ComboboxSelected>>", lambda e: staffSelected(staffCombobox, staffInfoText))

    listOfStaffCombined = cedAnalysis.get_list_of_staff()
    newStaffButton = ttk.Button(content, text="Add Staff",
                                command=lambda: popup_new_staff(root, staffCombobox, listOfStaffCombined))

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
