from . import textdisp
import json


gnrlwork = textdisp.GeneralWorking()


async def notify_mesej(username, operands, mesgtext, chatroom, USERDICT):
    userlist = USERDICT[chatroom]["userlist"]
    for user in userlist.keys():
        mesgdict = {
            "username": username,
            "operands": operands,
            "mesgtext": mesgtext,
            "chatroom": chatroom
        }
        mesgjson = json.dumps(mesgdict)
        await userlist[user].send(mesgjson)


async def personal_message(username, operands, mesgtext, chatroom, destsock):
    mesgdict = {
        "username": username,
        "operands": operands,
        "mesgtext": mesgtext,
        "chatroom": chatroom
    }
    mesgjson = json.dumps(mesgdict)
    await destsock.send(mesgjson)


def obtain_list_of_users_from_the_chatroom(chatroom, USERDICT):
    userlist = ""
    if chatroom in USERDICT.keys():
        for indx in USERDICT[chatroom]["userlist"].keys():
            userlist = userlist + indx + " "
    return userlist


class ServerOperations():
    def __init__(self, USERDICT, WAITAREA, websocket):
        self.websocket = websocket
        self.USERDICT = USERDICT
        self.WAITAREA = WAITAREA

    def check_websocket_object_presence(self):
        for indx in self.USERDICT.keys():
            for jndx in self.USERDICT[indx].keys():
                if self.websocket == self.USERDICT[indx][jndx]:
                    return True
        return False

    def obtain_username_and_chatroom_of_whoever_left(self):
        username, chatroom = "", ""
        for indx in self.USERDICT.keys():
            for jndx in self.USERDICT[indx]["userlist"].keys():
                if self.USERDICT[indx]["userlist"][jndx] == self.websocket:
                    username = jndx
                    chatroom = indx
        return username, chatroom

    async def check_specific_username_presence_in_the_chatroom(self, mesgdict):
        if mesgdict["operands"] == "CHEKUSER":
            if mesgdict["chatroom"] in self.USERDICT.keys():
                if mesgdict["passhash"] == self.USERDICT[mesgdict["chatroom"]]["passhash"]:
                    if mesgdict["username"] in self.USERDICT[mesgdict["chatroom"]]["userlist"].keys():
                        await personal_message("SNCTRYZERO", "USERPRST", "", mesgdict["chatroom"], self.websocket)
                        await self.websocket.close()
                        self.WAITAREA.remove(self.websocket)
                    else:
                        await personal_message("SNCTRYZERO", "USERABST", "", mesgdict["chatroom"], self.websocket)
                else:
                    await personal_message("SNCTRYZERO", "WRNGPASS", "", mesgdict["chatroom"], self.websocket)
                    await self.websocket.close()
                    self.WAITAREA.remove(self.websocket)
            else:
                self.USERDICT[mesgdict["chatroom"]] = {}
                self.USERDICT[mesgdict["chatroom"]]["roomownr"] = mesgdict["username"]
                self.USERDICT[mesgdict["chatroom"]]["passhash"] = mesgdict["passhash"]
                self.USERDICT[mesgdict["chatroom"]]["userlist"] = {mesgdict["username"]: self.websocket}
                gnrlwork.decorate("NEWROOMEXT", "<blue>" + mesgdict["username"] + " created " + mesgdict["chatroom"] + "</blue>")
                #WAITAREA.remove(websocket)
                await personal_message("SNCTRYZERO", "ROOMMADE", "", mesgdict["chatroom"], self.websocket)

    async def prove_user_identity_inside_a_chatroom(self, mesgdict):
        self.USERDICT[mesgdict["chatroom"]]["userlist"][mesgdict["username"]] = self.websocket
        self.WAITAREA.remove(self.websocket)
        gnrlwork.decorate("USERJOINED", "<green>" + mesgdict["username"] + " joined " + mesgdict["chatroom"] + "</green>")
        jointext = mesgdict["username"] + " joined the chatroom"
        await notify_mesej("SNCTRYZERO", "USERJOIN", jointext, mesgdict["chatroom"], self.USERDICT)

    async def dispatch_list_of_users(self, mesgdict):
        userlist = obtain_list_of_users_from_the_chatroom(mesgdict["chatroom"], self.USERDICT)
        gnrlwork.decorate("LISTRQSTED", "<orange>" + mesgdict["username"] + " from " + mesgdict["chatroom"] + " requested for participant list</orange>")
        await personal_message("SNCTRYZERO", "USERLIST", userlist, mesgdict["chatroom"], self.websocket)

    async def fetch_owner_name_of_the_chatroom(self, mesgdict):
        ownrname = self.USERDICT[mesgdict["chatroom"]]["roomownr"]
        gnrlwork.decorate("OWNRRQSTED", "<olive>" + mesgdict["username"] + " from " + mesgdict["chatroom"] + " requested for chatroom owner name</olive>")
        ownrmesg = ownrname + " is the owner of " + mesgdict["chatroom"]
        await personal_message("SNCTRYZERO", "FETCOWNR", ownrmesg, mesgdict["chatroom"], self.websocket)

    async def whisper_messages_to_a_specific_username(self, mesgdict):
        if mesgdict["destuser"] in self.USERDICT[mesgdict["chatroom"]]["userlist"].keys():
            gnrlwork.decorate("PURRPASSED", "<magenta>" + mesgdict["username"] + " from " + mesgdict["chatroom"] + " whispered messages to " + mesgdict["destuser"] + "</magenta>")
            await personal_message(mesgdict["username"], "PURRMESG", mesgdict["mesgtext"], mesgdict["chatroom"], self.USERDICT[mesgdict["chatroom"]]["userlist"][mesgdict["destuser"]])
        else:
            purrfail = "Whisper failed - Username not available in the chatroom"
            gnrlwork.decorate("PURRFAILED", "<magenta>" + mesgdict["username"] + " from " + mesgdict["chatroom"] + " failed to whisper messages</magenta>")
            await personal_message("SNCTRYZERO", "PURRFAIL", purrfail, mesgdict["chatroom"], self.websocket)

    async def remove_specific_username_from_the_room(self, mesgdict):
        if mesgdict["username"] == self.USERDICT[mesgdict["chatroom"]]["roomownr"]:
            if mesgdict["destuser"] in self.USERDICT[mesgdict["chatroom"]]["userlist"].keys():
                gnrlwork.decorate("KICKPASSED", "<red>" + mesgdict["username"] + " removed " + mesgdict["destuser"] + " from " + mesgdict["chatroom"] + "</red>")
                await personal_message("SNCTRYZERO", "KICKUSER", "You were removed from the chatroom", mesgdict["chatroom"], self.USERDICT[mesgdict["chatroom"]]["userlist"][mesgdict["destuser"]])
                await self.USERDICT[mesgdict["chatroom"]]["userlist"][mesgdict["destuser"]].close()
                self.USERDICT[mesgdict["chatroom"]]["userlist"].pop(mesgdict["destuser"])
                rmovnote = mesgdict["destuser"] + " was removed from the chatroom"
                await notify_mesej(mesgdict["username"], "KICKNOTE", rmovnote, mesgdict["chatroom"], self.USERDICT)
            else:
                gnrlwork.decorate("KICKFAILED", "<red>" + mesgdict["username"] + " failed to remove users from " + mesgdict["chatroom"] + "</red>")
                kickfail = "Removal failed - Username not available in the chatroom"
                await personal_message("SNCTRYZERO", "KICKFAIL", kickfail, mesgdict["chatroom"], self.websocket)
        else:
            gnrlwork.decorate("KICKUNAUTH", "<red>" + mesgdict["username"] + " from " + mesgdict["chatroom"] + " attempted unauthorized user removal</red>")
            kickauth = "Removal failed - You are not authorized to remove users"
            await personal_message("SNCTRYZERO", "KICKFAIL", kickauth, mesgdict["chatroom"], self.websocket)

    async def anonymously_dispatch_message_to_specific_username(self, mesgdict):
        if mesgdict["destuser"] in self.USERDICT[mesgdict["chatroom"]]["userlist"].keys():
            gnrlwork.decorate("ANONPASSED", "<teal>" + mesgdict["username"] + " from " + mesgdict["chatroom"] + " anonymously dispatched messages to " + mesgdict["destuser"] + "</teal>")
            await personal_message("SNCTRYZERO", "ANONMESG", mesgdict["mesgtext"], mesgdict["chatroom"], self.USERDICT[mesgdict["chatroom"]]["userlist"][mesgdict["destuser"]])
        else:
            gnrlwork.decorate("ANONFAILED", "<teal>" + mesgdict["username"] + " from " + mesgdict["chatroom"] + " failed to anonymously dispatch messages</teal>")
            anonfail = "Anonymous dispatch failed - Username not available in the chatroom"
            await personal_message("SNCTRYZERO", "ANONFAIL", anonfail, mesgdict["chatroom"], self.websocket)

    async def convey_normal_messages(self, mesgdict):
        gnrlwork.decorate("CONVEYMESG", mesgdict["username"] + " sent a message to " + mesgdict["chatroom"])
        await notify_mesej(mesgdict["username"], "CONVEYMG", mesgdict["mesgtext"], mesgdict["chatroom"], self.USERDICT)

    async def handle_broken_connections(self):
        username, chatroom = self.obtain_username_and_chatroom_of_whoever_left()
        self.USERDICT[chatroom]["userlist"].pop(username)
        leftmesg = username + " left the chatroom"
        gnrlwork.decorate("USEREXITED", "<maroon>" + username + " left " + chatroom + "</maroon>")
        await notify_mesej("SNCTRYZERO", "LEFTMESG", leftmesg, chatroom, self.USERDICT)
