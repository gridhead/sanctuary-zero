import asyncio, websockets, sys, click, time, os,secrets
from prompt_toolkit import print_formatted_text, HTML
from websockets.exceptions import ConnectionClosedError
from cryptography.fernet import Fernet, InvalidToken
from utils.helper_display import HelperDisplay


USERS = {}
CHATROOM = {}
sepr = chr(969696)
current_rooms=[]

class fernetst():
    def __init__(self, pswd):
        self.suit = Fernet(pswd)

    def encrjson(self, data):
        return self.suit.encrypt(data.encode("utf8")).decode("utf8")

    def decrjson(self, data):
        return self.suit.decrypt(data.encode("utf8")).decode("utf8")
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


def getallus(chatroom):
    userlist = []
    for indx in USERS:
        if USERS[indx]!="" and chatroom == USERS[indx][1]:
            userlist.append(USERS[indx][0])
    return userlist


async def notify_mesej(message):
    if USERS: await asyncio.wait([user.send(message) for user in USERS])


def chk_username_presence(mesg_json):
    new_name = mesg_json.split(sepr)[1]
    chatroom_id = mesg_json.split(sepr)[2]
    if new_name in getallus(chatroom_id):
        return True
    else:
        return False


async def notify_mesej(message):
    if USERS:
        await asyncio.wait([user.send(message) for user in USERS])

async def send_chatroommembers_list(websoc):
    chatroom_id = USERS[websoc][1]
    users_list = "SNCTRYZERO" + sepr + "USERSLIST" + sepr + str(getallus(chatroom_id)) + sepr + chatroom_id
    await websoc.send(users_list)

async def chatroom(websocket, path):
    if not websocket in USERS:
        USERS[websocket] = ""
    try:
        async for mesgjson in websocket:
            if sepr in mesgjson and websocket in USERS:
                if USERS[websocket] == "":
                    if mesgjson.split(sepr)[0] == 'NEW':
                        new_room = randgene()
                        current_rooms.append(new_room)
                        USERS[websocket] = [mesgjson.split(sepr)[1], new_room]
                        password = Fernet.generate_key().decode("utf-8")
                        CHATROOM[new_room] = password
                        await websocket.send(new_room+sepr+password)
                        print_formatted_text(HTML("[" + obtntime() + "] " + "<b>USERJOINED</b> > <green>" + mesgjson.split(sepr)[1] + "@" + new_room + "</green>"))
                        await notify_mesej("SNCTRYZERO" + sepr + "USERJOINED" + sepr + mesgjson.split(sepr)[1] + sepr + new_room + sepr + str(getallus(new_room)))
                    elif mesgjson.split(sepr)[0] == 'CHKUSR':
                        # [query username chatroom password]
                        if mesgjson.split(sepr)[2] in current_rooms and mesgjson.split(sepr)[3] == CHATROOM[mesgjson.split(sepr)[2]] and str(chk_username_presence(mesgjson)) == "False":
                            await websocket.send("True")
                            USERS[websocket] = [mesgjson.split(sepr)[1],mesgjson.split(sepr)[1]]
                            print_formatted_text(HTML("[" + obtntime() + "] " + "<b>USERJOINED</b> > <green>" + mesgjson.split(sepr)[3] + "@" + mesgjson.split(sepr)[1] + "</green>"))
                            await notify_mesej("SNCTRYZERO" + sepr + "USERJOINED" + sepr + mesgjson.split(sepr)[3] + sepr + mesgjson.split(sepr)[1] + sepr + str(getallus(mesgjson.split(sepr)[1])))
                        else:
                            await websocket.send("False")
                            isInvalid = True
                    elif str(mesgjson) == '/list':
                        await send_chatroommembers_list(websocket)
            else:
                print_formatted_text(HTML("[" + obtntime() + "] " + "<b>SNCTRYZERO</b> > " + helper_display.wrap_text(str(mesgjson))))
                await notify_mesej(mesgjson)
    except ConnectionClosedError as EXPT:
        if isInvalid == False:
            print_formatted_text(HTML("[" + obtntime() + "] " + "<b>USEREXITED</b> > <red>" + USERS[websocket][0] + "@" + USERS[websocket][1] + "</red>"))
            userlist = getallus(USERS[websocket][1])
            userlist.remove(USERS[websocket][0])
            leftmesg = "SNCTRYZERO" + sepr + "USEREXITED" + sepr + USERS[websocket][0] + sepr + USERS[websocket][1] + sepr + str(userlist)
            USERS.pop(websocket)
            await notify_mesej(leftmesg)
        else:
            isInvalid = False

def randgene():
    numb = 8
    randstrg = ''.join(secrets.choice("ABCDEF" + "0123456789") for i in range(numb))
    return randstrg


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
@click.version_option(version="18102020", prog_name="SNCTRYZERO Server")
def mainfunc(chatport, netprotc):
    try:
        click.clear()
        print_formatted_text("\n")
        print_formatted_text(HTML("[" + obtntime() + "] " + "<b>SNCTRYZERO</b> > <green><b>Starting SNCTRYZERO server v18102020...</b></green>" + "\n" + \
            "[" + obtntime() + "] " + "<b>SNCTRYZERO</b> > Know more about the project at https://github.com/t0xic0der/sanctuary-zero/wiki" + "\n" + \
            "[" + obtntime() + "] " + "<b>SNCTRYZERO</b> > Find folks we're thankful to at https://github.com/t0xic0der/sanctuary-zero/graphs/contributors"))
        netpdata = ""
        if netprotc == "ipprotv6":
            print_formatted_text(HTML("[" + obtntime() + "] " + "<b>SNCTRYZERO</b> > <green>IP version : 6</green>"))
            netpdata = "::"
        elif netprotc == "ipprotv4":
            print_formatted_text(HTML("[" + obtntime() + "] " + "<b>SNCTRYZERO</b> > <green>IP version : 4</green>"))
            netpdata = "0.0.0.0"
        servenow(netpdata, chatport)
    except OSError:
        print_formatted_text(HTML("[" + obtntime() + "] " + "<b>SNCTRYZERO</b> > <red><b>The server could not be started up</b></red>"))


if __name__ == "__main__":
    mainfunc()
