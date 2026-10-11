import re
from time import sleep
import cedmodAPI
import datetime as dt


def extract_steam_id(name):
    # Checking if a steam ID appears in the issuer name.
    if re.search("[0-9]*@steam", name) is not None:
        return re.search("[0-9]*@steam", name).group()
    else:
        # if there is not a steam ID we assume that the ban was issued using the panel so the name will be their cedmod name.
        return name


def remove_steam_names(listOfNames):
    discordNames = []
    for i in range(0, len(listOfNames)):
        if re.search("[0-9]*@steam", listOfNames[i]) is None:
            discordNames.append(listOfNames[i])
    return discordNames


def remove_discord_names(listOfNames):
    steamNames = []
    for i in range(0, len(listOfNames)):
        if re.search("[0-9]*@steam", listOfNames[i]) is not None:
            steamNames.append(listOfNames[i])
    return steamNames


def get_list_of_ban_issuers(max=50, page=None, responseJson=None, fullSteaamName=False):
    issuerNames = []

    if responseJson is None:
        responseJson = cedmodAPI.get_bans(max=max, page=page)

    if fullSteaamName:
        for i in range(0, len(responseJson["players"])):
            issuerNames.append(responseJson["players"][i]["issuer"])
    else:
        for i in range(0, len(responseJson["players"])):
            issuerNames.append(extract_steam_id(responseJson["players"][i]["issuer"]))

    return issuerNames


def get_list_of_ban_issuers_to_date(date, fullSteaamName=False):
    #This is basically the same as the get_list_of_ban_issuers function however it will get the banlist up to the date parameter rather than using max or page.
    issuerNames = []
    dateNotMet = True
    page = 0
    while True:
        responseJson = cedmodAPI.get_bans(max=100,page=page)
        if fullSteaamName:
            for i in range(0, len(responseJson["players"])):
                if dt.datetime.strptime(
                        responseJson["players"][i]["timeStamp"].split("T")[0],"%Y-%m-%d") < date:
                    #Checking if the date for the slected ban is before the maxdate, if it is we return the issuer names
                    return issuerNames
                issuerNames.append(responseJson["players"][i]["issuer"])


        else:
            for i in range(0, len(responseJson["players"])):
                if dt.datetime.strptime(responseJson["players"][i]["timeStamp"].split("T")[0],"%Y-%m-%d") < date:
                    return issuerNames
                issuerNames.append(extract_steam_id(responseJson["players"][i]["issuer"]))

        page += 1
        # If we have not found a ban that was issued before the selected date we go to the next page


        # Enforcing a 5-second delay between request after requesting 5 pages of bans to avoid flooding the cedmod servers
        if page > 5:
            sleep(5)




def get_list_of_report_handlers(status=-1, responseJson=None):
    handlerNames = []

    if responseJson is None:
        responseJson = cedmodAPI.get_reports()

    if 0 <= status <= 3:
        for i in range(0, len(responseJson["players"])):
            if responseJson["players"][i]["status"] == str(status) and responseJson["players"][i]["handler"] != "":
                handlerNames.append(responseJson["players"][i]["handler"])
    else:
        for i in range(0, len(responseJson["players"])):
            if responseJson["players"][i]["handler"] != "":
                handlerNames.append(responseJson["players"][i]["handler"])

    return handlerNames


def get_list_of_warn_issuers(max=None, responseJson=None):
    issuerNames = []

    if responseJson is None:
        responseJson = cedmodAPI.get_warns(max=max)

    for i in range(0, len(responseJson["players"])):
        issuerNames.append(responseJson["players"][i]["issuer"])

    return issuerNames


def get_list_of_warn_issuers_to_date(date,max=100,page=0):
    issuerNames = []

    while True:

        responseJson = cedmodAPI.get_warns(max=max,page=page)

        for i in range(0, len(responseJson["players"])):
            if dt.datetime.strptime(responseJson["players"][i]["timeStamp"].split("T")[0], "%Y-%m-%d") < date:
                # Checking if date on warn is from before the selected date
                return issuerNames
            issuerNames.append(responseJson["players"][i]["issuer"])

        page +=1
        # If we have not found a warn that was issued before the selected date we go to the next page

        # Enforcing a 5-second delay between request after requesting 5 pages of warns to avoid flooding the cedmod servers
        if page > 5:
            sleep(5)


def get_list_of_staff_steam_names(max=50):
    namesList = []
    response = cedmodAPI.get_activity(max=max, staffOnly=True)
    for i in range(0, len(response["players"])):
        user = response["players"][i]
        namesList.append(str(user["userName"] + "(" + user["userId"] + ")"))

    return namesList


def remove_duplicate_names(listOfNames):
    setOfNames = set(listOfNames)
    listOfNames = list(setOfNames)
    return listOfNames


def get_list_of_staff(type=None):

    issuers = get_list_of_warn_issuers(max=100)


    if type is None:
        discord = list(dict.fromkeys((remove_steam_names(issuers))))
        steam = get_list_of_staff_steam_names()
        return (discord, steam)
    else:
        type = type.lower()

    if type == "discord":
        discord = remove_duplicate_names(remove_steam_names(issuers))
        return discord

    elif type == "steam":
        steam = remove_duplicate_names(remove_discord_names(issuers))
        return steam


def get_dict_of_staff_playtime(max=50,activityMin=30):
    response = cedmodAPI.get_activity(max=max,activityMin=activityMin)
    playerList = response["players"]
    dictList = []
    for i in range(0, len(playerList)):
        dictList.append((playerList[i]["userId"], playerList[i]["activity"]))

    return dict(dictList)


def get_dict_of_staff_connection_delta(max=50):
    response = cedmodAPI.get_activity(max=max,staffOnly=True)
    dictList = []
    playerList = response["players"]
    for i in range(0,len(playerList)):
        lastSeenList = re.search("\\d{4}-\\d{2}-\\d*", string=playerList[i]["lastSeen"]).group().split("-")
        lastSeenDateTime = dt.datetime(year=int(lastSeenList[0]), month=int(lastSeenList[1]),day=int(lastSeenList[2]))
        delta = (dt.datetime.now() - lastSeenDateTime).days
        dictList.append((playerList[i]["userId"],delta))

    return dict(dictList)


def get_dict_of_staff_reports(max=100,page=0):
    reports = cedmodAPI.get_reports(max=max,page=page)
    listOfReports = reports["players"]
    dict = {}
    for i in range(0,len(listOfReports)):
        report = listOfReports[i]
        if report["handler"] in dict:
            dict[report["handler"]][report["status"]] += 1
        else:
            dict.update({report["handler"]:[0,0,0,0]})
            dict[report["handler"]][report["status"]] += 1

    return dict

def get_dict_of_staff_reports_to_date(date,max=100,page = 0):
    dict = {}

    while True:

        reports = cedmodAPI.get_reports(max=max,page=page)
        listOfReports = reports["players"]

        for i in range(0,len(listOfReports)):
            report = listOfReports[i]
            if dt.datetime.strptime(report["created"].split("T")[0], "%Y-%m-%d") < date:
                #Checking if the date on the report is from before the selected date
                return dict
            elif report["handler"] in dict:
                dict[report["handler"]][report["status"]] += 1
            else:
                dict.update({report["handler"]:[0,0,0,0]})
                dict[report["handler"]][report["status"]] += 1

        page +=1
        # If we have not found a report that was created before the selected date we go to the next page


        # Enforcing a 5-second delay between request after requesting 5 pages of reports to avoid flooding the cedmod servers
        if page > 5:
            sleep(5)


def get_list_of_years():
    array = []
    #get current year
    currentYear = dt.datetime.now().year
    # SCP:SL was launched in 2017
    launchYear = 2017

    yearsSinceLaunch = (currentYear-launchYear)+1

    for i in range(0,(yearsSinceLaunch)):
        array.append(currentYear)
        currentYear -= 1

    return array


def get_list_of_months():
    array = []
    for i in range(1,13):
        array.append(i)
    return array


def get_list_of_days(max = 31):
    array = []
    for i in range(1,max+1):
        array.append(i)
    return array

# ------------ Functions that add stats to staff go below ------------

def add_bans_to_staff(staffList,date):
    print("CedA: Starting adding bans to staff list")
    banList = get_list_of_ban_issuers_to_date(date=date)
    for i in range(0, len(staffList)):
        staffList[i].set_bans(banList.count(staffList[i].cedmodName) + banList.count(staffList[i].steamID))
    print("CedA: Finished adding bans to staff list")


def add_warns_to_staff(staffList,date):
    print("CedA: Starting adding warns to staff list")
    warnList = get_list_of_warn_issuers_to_date(date=date)
    for i in range(0, len(staffList)):
        staffList[i].set_warns(warnList.count(staffList[i].cedmodName) + warnList.count(staffList[i].steamID))
    print("CedA: Finished adding warns to staff list")


def add_deta_to_staff(staffList):
    print("CedA: Starting adding delta to staff list")
    playtimeDict = get_dict_of_staff_connection_delta()
    for i in range(0, len(staffList)):
        staffList[i].set_days_since_connection(playtimeDict[staffList[i].steamID])
    print("CedA: Finished adding delta to staff list")


def add_playtime_to_staff(staffList,date):
    days = (dt.datetime.now() - date).days
    print("CedA: Starting adding playtime to staff list")
    playtimeDict = get_dict_of_staff_playtime(activityMin=days)
    for i in range(0, len(staffList)):
        staffList[i].set_playtime(playtimeDict[staffList[i].steamID] / 3600)
    print("CedA: Finished adding playtime to staff list")


def add_reports_to_staff(staffList,date):
    print("CedA: Starting adding reports to staff list")
    reportsDict = get_dict_of_staff_reports_to_date(date=date)
    for i in range(0,len(staffList)):
        if staffList[i].cedmodName in reportsDict:
            staffList[i].set_reports_ignored(reportsDict[staffList[i].cedmodName][2])
            staffList[i].set_reports_handled(reportsDict[staffList[i].cedmodName][3])
        else:
            print("CedA: ERROR Cedmod name has either not handled a report or is different from discord username")
            staffList[i].set_reports_ignored(-2)
            staffList[i].set_reports_handled(-2)
    print("CedA: Finished adding report to staff list")
