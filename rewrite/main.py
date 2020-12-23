import asyncio, websockets, sys, click, http.client, time
from prompt_toolkit import print_formatted_text, HTML
from websockets.exceptions import ConnectionClosedError
from utils.helper_display import HelperDisplay
import json


WAITING_AREA = []
USERS = {}

helper_display = HelperDisplay()


def obtntime():
    timestmp = time.localtime()
    timehour = str(timestmp.tm_hour)
    timemint = str(timestmp.tm_min)
    timesecs = str(timestmp.tm_sec)
    if int(timehour) < 10:  timehour = "0" + timehour
    if int(timemint) < 10:  timemint = "0" + timemint
    if int(timesecs) < 10:  timesecs = "0" + timesecs
    return timehour + ":" + timemint + ":" + timesecs


def ipaddress(v):
    url = "api64.ipify.org"
    if v == 4:
        url = "api.ipify.org"
    elif v == 6:
        url = "api6.ipify.org"
    try:
        connection = http.client.HTTPSConnection(url)
        connection.request("GET", "/")
        response = connection.getresponse()
        return response.read().decode("UTF-8")
    except:
        return "Error getting IP address."


def getallus(chatroom):
    userlist = []
    for indx in USERS:
        if USERS[indx]!="" and chatroom == USERS[indx][1]:
            userlist.append(USERS[indx][0])
    return userlist


async def notify_mesej(username, operands, mesgtext, chatroom):
    userlist = USERS[chatroom]["userlist"]
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


'''
USERS = {
    "DEADCAFE": {
        "roomownr": "t0xic0der",
        "userlist": {
            "t0xic0der": <websockets.server.WebSocketServerProtocol object at 0x7fd58a985580>,
            "m3x1c0": <websockets.server.WebSocketServerProtocol object at 0x7fd58a9d8dc0>
        }
    }
}
'''

'''
# FROM CLIENT TO SERVER
MESSAGE_STRUCTURE = {
    "username": "t0xic0der",
    "operands": "CHEKUSER",
    "mesgtext": "",
    "chatroom": "DEADCAFE",
}
'''

'''
# FROM SERVER TO CLIENT
MESSAGE_STRUCTURE = {
    "username": "t0xic0der",
    "operands": "CHEKUSER",
    "mesgtext": "",
    "chatroom": "DEADCAFE",
}
'''


def obtain_list_of_users_from_the_chatroom(chatroom):
    userlist = ""
    if chatroom in USERS.keys():
        for indx in USERS[chatroom]["userlist"].keys():
            userlist = userlist + indx + " "
    return userlist


class ServerOperations():
    def __init__(self, websocket):
        self.websocket = websocket

    def check_websocket_object_presence(self):
        for indx in USERS.keys():
            for jndx in USERS[indx].keys():
                if self.websocket == USERS[indx][jndx]:
                    return True
        return False

    def obtain_username_and_chatroom_of_whoever_left(self):
        username, chatroom = "", ""
        for indx in USERS.keys():
            for jndx in USERS[indx]["userlist"].keys():
                if USERS[indx]["userlist"][jndx] == self.websocket:
                    username = jndx
                    chatroom = indx
        return username, chatroom

    async def check_specific_username_presence_in_the_chatroom(self, mesgdict):
        if mesgdict["operands"] == "CHEKUSER":
            if mesgdict["chatroom"] in USERS.keys():
                if mesgdict["username"] in USERS[mesgdict["chatroom"]]["userlist"].keys():
                    await self.websocket.send("True")
                    await self.websocket.close()
                    WAITING_AREA.remove(self.websocket)
                else:
                    await self.websocket.send("False")
            else:
                USERS[mesgdict["chatroom"]] = {}
                USERS[mesgdict["chatroom"]]["roomownr"] = mesgdict["username"]
                USERS[mesgdict["chatroom"]]["userlist"] = {mesgdict["username"]: self.websocket}
                print_formatted_text(HTML(
                    "[" + obtntime() + "] " + "<b>NEWROOMEXT</b> > <green>" + mesgdict["username"] + "@" + mesgdict[
                        "chatroom"] + "</green>"))
                # WAITING_AREA.remove(websocket)
                await self.websocket.send("False")

    async def prove_user_identity_inside_a_chatroom(self, mesgdict):
        USERS[mesgdict["chatroom"]]["userlist"][mesgdict["username"]] = self.websocket
        WAITING_AREA.remove(self.websocket)
        print_formatted_text(HTML(
            "[" + obtntime() + "] " + "<b>USERJOINED</b> > <green>" + mesgdict["username"] + "@" + mesgdict[
                "chatroom"] + "</green>"))
        jointext = mesgdict["username"] + " joined the chatroom"
        await notify_mesej("SNCTRYZERO", "USERJOIN", jointext, mesgdict["chatroom"])

    async def dispatch_list_of_users(self, mesgdict):
        userlist = obtain_list_of_users_from_the_chatroom(mesgdict["chatroom"])
        await personal_message("SNCTRYZERO", "USERLIST", userlist, mesgdict["chatroom"], self.websocket)

    async def whisper_messages_to_a_specific_username(self, mesgdict):
        if mesgdict["destuser"] in USERS[mesgdict["chatroom"]]["userlist"].keys():
            await personal_message(mesgdict["username"], "PURRMESG", mesgdict["mesgtext"], mesgdict["chatroom"],
                                   USERS[mesgdict["chatroom"]]["userlist"][mesgdict["destuser"]])
        else:
            purrfail = "Whisper failed - Username not available in the chatroom"
            await personal_message("SNCTRYZERO", "PURRFAIL", purrfail, mesgdict["chatroom"], self.websocket)

    async def remove_specific_username_from_the_room(self, mesgdict):
        if mesgdict["destuser"] in USERS[mesgdict["chatroom"]]["userlist"].keys():
            await personal_message("SNCTRYZERO", "KICKUSER", "", mesgdict["chatroom"],
                                   USERS[mesgdict["chatroom"]]["userlist"][mesgdict["destuser"]])
            await USERS[mesgdict["chatroom"]]["userlist"][mesgdict["destuser"]].close()
            USERS[mesgdict["chatroom"]]["userlist"].pop(mesgdict["destuser"])
            print("Connection closed neega!")
        else:
            kickfail = "Removal failed - Username not available in the chatroom"
            await personal_message("SNCTRYZERO", "KICKFAIL", kickfail, mesgdict["chatroom"], self.websocket)

    async def anonymously_dispatch_message_to_specific_username(self, mesgdict):
        if mesgdict["destuser"] in USERS[mesgdict["chatroom"]]["userlist"].keys():
            await personal_message("SNCTRYZERO", "ANONMESG", mesgdict["mesgtext"], mesgdict["chatroom"],
                                   USERS[mesgdict["chatroom"]]["userlist"][mesgdict["destuser"]])
        else:
            anonfail = "Anonymous dispatch failed - Username not available in the chatroom"
            await personal_message("SNCTRYZERO", "ANONFAIL", anonfail, mesgdict["chatroom"], self.websocket)

    async def convey_normal_messages(self, mesgdict):
        print_formatted_text(
            HTML(
                "[" + obtntime() + "] " + "<b>SNCTRYZERO</b> > " + helper_display.wrap_text(str(mesgdict["mesgtext"]))))
        await notify_mesej(mesgdict["username"], "CONVEYMG", mesgdict["mesgtext"], mesgdict["chatroom"])

    async def handle_broken_connections(self):
        username, chatroom = self.obtain_username_and_chatroom_of_whoever_left()
        USERS[chatroom]["userlist"].pop(username)
        leftmesg = username + " left the chatroom"
        print_formatted_text(
            HTML("[" + obtntime() + "] " + "<b>USEREXITED</b> > <red>" + username + "@" + chatroom + "</red>"))
        await notify_mesej("SNCTRYZERO", "LEFTMESG", leftmesg, chatroom)


async def chatroom(websocket, path):
    servoprs = ServerOperations(websocket)
    if not servoprs.check_websocket_object_presence():
        WAITING_AREA.append(websocket)
    try:
        async for mesgjson in websocket:
            mesgdict = json.loads(mesgjson)
            if mesgdict["operands"] == "CHEKUSER":
                await servoprs.check_specific_username_presence_in_the_chatroom(mesgdict)
            elif mesgdict["operands"] == "IDENTIFY":
                await servoprs.prove_user_identity_inside_a_chatroom(mesgdict)
            elif mesgdict["operands"] == "LISTUSER":
                await servoprs.dispatch_list_of_users(mesgdict)
            elif mesgdict["operands"] == "PURRMESG":
                await servoprs.whisper_messages_to_a_specific_username(mesgdict)
            elif mesgdict["operands"] == "KICKUSER":
                await servoprs.remove_specific_username_from_the_room(mesgdict)
            elif mesgdict["operands"] == "KILLROOM":
                pass
            elif mesgdict["operands"] == "ANONMESG":
                await servoprs.anonymously_dispatch_message_to_specific_username(mesgdict)
            elif mesgdict["operands"] == "CONVEYMG":
                await servoprs.convey_normal_messages(mesgdict)
    except ConnectionClosedError as EXPT:
        await servoprs.handle_broken_connections()


def servenow(netpdata="127.0.0.1", chatport="9696"):
    try:
        start_server = websockets.serve(chatroom, netpdata, int(chatport))
        asyncio.get_event_loop().run_until_complete(start_server)
        print_formatted_text(HTML("[" + obtntime() + "] " + "<b>SNCTRYZERO</b> > <green>SNCTRYZERO server was started up on 'ws://" + str(netpdata) + ":" + str(chatport) + "/'</green>"))
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("")
        print_formatted_text(HTML("[" + obtntime() + "] " + "<b>SNCTRYZERO</b> > <red><b>SNCTRYZERO server was shut down</b></red>"))
        sys.exit()


@click.command()
@click.option("-c", "--chatport", "chatport", help="Set the port value for the server [0-65536]", required=True)
@click.option("-6", "--ipprotv6", "netprotc", flag_value="ipprotv6", help="Start the server on an IPv6 address", required=True)
@click.option("-4", "--ipprotv4", "netprotc", flag_value="ipprotv4", help="Start the server on an IPv4 address", required=True)
@click.version_option(version="30102020", prog_name="SNCTRYZERO Server")
def mainfunc(chatport, netprotc):
    try:
        click.clear()
        print_formatted_text("\n")
        print_formatted_text(HTML("[" + obtntime() + "] " + "<b>SNCTRYZERO</b> > <green><b>Starting SNCTRYZERO server v30102020...</b></green>" + "\n" + \
            "[" + obtntime() + "] " + "<b>SNCTRYZERO</b> > Know more about the project at https://github.com/t0xic0der/sanctuary-zero/wiki" + "\n" + \
            "[" + obtntime() + "] " + "<b>SNCTRYZERO</b> > Find folks we're thankful to at https://github.com/t0xic0der/sanctuary-zero/graphs/contributors"))
        netpdata = ""
        if netprotc == "ipprotv6":
            print_formatted_text(HTML("[" + obtntime() + "] " + "<b>SNCTRYZERO</b> > <green>IP version : 6</green>"))
            netpdata = "::"
            print_formatted_text(HTML("[" + obtntime() + "] " + "<b>SNCTRYZERO</b> > <green>IP address : " + ipaddress(6) + "</green>"))
        elif netprotc == "ipprotv4":
            print_formatted_text(HTML("[" + obtntime() + "] " + "<b>SNCTRYZERO</b> > <green>IP version : 4</green>"))
            netpdata = "0.0.0.0"
            print_formatted_text(HTML("[" + obtntime() + "] " + "<b>SNCTRYZERO</b> > <green>IP address : " + ipaddress(4) + "</green>"))
        servenow(netpdata, chatport)
    except OSError:
        print_formatted_text(HTML("[" + obtntime() + "] " + "<b>SNCTRYZERO</b> > <red><b>The server could not be started up</b></red>"))


if __name__ == "__main__":
    mainfunc()
