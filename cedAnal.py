import re
import cedmodAPI

def extract_steam_id(name):
    # Checking if a steam ID appears in the issuer name.
    if re.search("[0-9]*@steam", name) is not None:
        return re.search("[0-9]*@steam", name).group()
    else:
        # if there is not a steam ID we assume that the ban was issued using the panel so the name will be their cedmod name.
        return name

def remove_steam_names(listOfNames):
    discordNames = []
    for i in range(0,len(listOfNames)):
        if re.search("[0-9]*@steam", listOfNames[i]) is None:
            discordNames.append(listOfNames[i])
    return discordNames

def remove_discord_names(listOfNames):
    steamNames = []
    for i in range(0, len(listOfNames)):
        if re.search("[0-9]*@steam", listOfNames[i]) is not None:
            steamNames.append(listOfNames[i])
    return steamNames



def get_list_of_ban_issuers(max=50,page=None,responseJson=None,fullSteaamName=False):
    issuerNames = []

    if responseJson is None:
        responseJson = cedmodAPI.get_bans(max=max,page=page)



    if fullSteaamName:
        for i in range(0, len(responseJson["players"])):
            issuerNames.append(responseJson["players"][i]["issuer"])
    else:
        for i in range(0, len(responseJson["players"])):
            issuerNames.append(extract_steam_id(responseJson["players"][i]["issuer"]))


    return issuerNames


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

def get_list_of_warn_issuers(max=None,responseJson=None):
    issuerNames = []

    if responseJson is None:
        responseJson = cedmodAPI.get_warns(max=max)

    for i in range(0, len(responseJson["players"])):
        issuerNames.append(responseJson["players"][i]["issuer"])

    return issuerNames

def remove_duplicate_names(listOfNames):
    setOfNames = set(listOfNames)
    listOfNames = list(setOfNames)
    return listOfNames


def get_list_of_staff(type=None,responceJson=None):
    if responceJson is not None:
        issuers = get_list_of_ban_issuers(responseJson=responceJson)
    else:
        issuers = get_list_of_ban_issuers(fullSteaamName=True)

    if type is None:
        discord = remove_duplicate_names(remove_steam_names(issuers))
        steam = remove_duplicate_names(remove_discord_names(issuers))
        return (discord,steam)
    else:
        type = type.lower()

    if type == "discord":
        discord = remove_duplicate_names(remove_steam_names(issuers))
        return discord

    elif type == "steam":
        steam = remove_duplicate_names(remove_discord_names(issuers))
        return steam



def add_bans_to_staff(staffList):
    banList = get_list_of_ban_issuers(max=100)
    for i in range (0,len(staffList)):
        staffList[i].set_bans(banList.count(staffList[i].cedmodName) + banList.count(staffList[i].steamID))

def add_warns_to_staff(staffList):
    warnList = get_list_of_warn_issuers(max=100)
    for i in range(0, len(staffList)):
        staffList[i].set_warns(warnList.count(staffList[i].cedmodName) + warnList.count(staffList[i].steamID))

    return staffList