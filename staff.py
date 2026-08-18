class Staff:
    name = "NaN"
    steamID = "NaN"
    cedmodName = "NaN"
    altName = "NaN"

    bans = -1
    warns = -1
    playtime = -1
    reportsHandled = -1
    reportsIgnored = -1

    def set_name(self, name):
        self.name = str(name)

    def set_steam_id(self, steam_id):
        self.steamID = str(steam_id)

    def set_cedmod_name(self, cedmod_name):
        self.cedmodName = str(cedmod_name)

    def set_bans(self, bans):
        self.bans = int(bans)

    def set_warns(self, warns):
        self.warns = int(warns)

    def set_playtime(self, playtime):
        self.playtime = int(playtime)


    def set_reports_handled(self, reports_handled):
        self.reportsHandled = int(reports_handled)


    def set_reports_ignored(self, reports_ignored):
        self.reportsIgnored = int(reports_ignored)

    def to_string(self):
        return "SteamID: "+str(self.steamID)+"\nCedmod Name: "+str(self.cedmodName)+"\nBans: "+str(self.bans)+" | Warns: "+str(self.warns)+"\nPlaytime: "+str(self.playtime)+"\nReports Handled: "+str(self.reportsHandled)+"\nReports Ignored: "+str(self.reportsIgnored)+"\nDays since last connection: TODO"

    def __str__(self):
        return self.name
