import asyncio, websockets, time, json, click, secrets, os, sys
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.validation import Validator, ValidationError
from cryptography.fernet import Fernet, InvalidToken


sess = PromptSession()
sepr = chr(969696)


class emtyfind(Validator):
    def validate(self, document):
        text = document.text
        if text.strip() == "":
            raise ValidationError(message="You cannot send an empty message")


class fernetst():
    def __init__(self, pswd):
        self.suit = Fernet(pswd)

    def encrjson(self, data):
        return self.suit.encrypt(data.encode("utf8")).decode("utf8")

    def decrjson(self, data):
        return self.suit.decrypt(data.encode("utf8")).decode("utf8")


async def consumer_handler(cphrsuit, websocket, username, chatroom, servaddr):
    async for recvdata in websocket:
        try:
            if recvdata.split(sepr)[0] == "SNCTRYZERO" and recvdata.split(sepr)[1] == "USERJOINED" and recvdata.split(sepr)[3] == chatroom:
                print("[" + obtntime() + "] USERJOINED > " + recvdata.split(sepr)[2] + " joined - " + recvdata.split(sepr)[4] + " are connected - Indexes updated")
            elif recvdata.split(sepr)[0] == "SNCTRYZERO" and recvdata.split(sepr)[1] == "USEREXITED" and recvdata.split(sepr)[3] == chatroom:
                print("[" + obtntime() + "] USEREXITED > " + recvdata.split(sepr)[2] + " left - " + recvdata.split(sepr)[4] + " are connected - Indexes updated")
            else:
                recvjson = json.loads(cphrsuit.decrjson(recvdata))
                if recvjson["chatroom"] == chatroom and recvjson["username"] != username:
                    print("[" + obtntime() + "] " + formusnm(recvjson["username"]) + " > " + recvjson["mesgtext"])
        except Exception as EXPT:
            pass


async def producer_handler(cphrsuit, websocket, username, chatroom, servaddr):
    footelem = HTML("<b>[" + chatroom + "]</b>" + " " + username.strip() + " - Sanctuary ZERO v04092020 running on '" + servaddr + "' - Hit Ctrl+C to EXIT")
    while True:
        with patch_stdout():
            mesgtext = await sess.prompt_async("[" + obtntime() + "] " + formusnm(str(username)) + " > ", bottom_toolbar=footelem, validator=emtyfind())
        senddata = json.dumps({"username": username.strip(), "chatroom": chatroom, "mesgtext": mesgtext.strip()})
        senddata = cphrsuit.encrjson(senddata)
        await websocket.send(senddata)


async def hello(servaddr, username, chatroom, password):
    async with websockets.connect(servaddr) as websocket:
        cphrsuit = fernetst(password.encode("utf8"))
        prod = asyncio.get_event_loop().create_task(producer_handler(cphrsuit, websocket, str(username), str(chatroom), str(servaddr)))
        cons = asyncio.get_event_loop().create_task(consumer_handler(cphrsuit, websocket, str(username), str(chatroom), str(servaddr)))
        await websocket.send(username+sepr+chatroom)
        await prod
        await cons
        asyncio.get_event_loop().run_forever()


def obtntime():
    timestmp = time.localtime()
    timehour = str(timestmp.tm_hour)
    timemint = str(timestmp.tm_min)
    timesecs = str(timestmp.tm_sec)
    if int(timehour) < 10:  timehour = "0" + timehour
    if int(timemint) < 10:  timemint = "0" + timemint
    if int(timesecs) < 10:  timesecs = "0" + timesecs
    return timehour + ":" + timemint + ":" + timesecs


def randgene():
    numb = 8
    randstrg = ''.join(secrets.choice("ABCDEF" + "0123456789") for i in range(numb))
    return randstrg


def chekroom(strg):
    if len(strg) != 8:
        return False
    else:
        try:
            geee = int(strg, 16)
            return strg.isupper()
        except ValueError:
            return False


def chekpass(pswd):
    try:
        suit = Fernet(pswd)
        return True
    except:
        return False


def formusnm(username):
    if len(username) < 10:      return username + " " * (10 - len(username))
    elif len(username) > 10:    return username[0:10]
    else:                       return username


@click.command()
@click.option("-u", "--username", "username", help="Enter the username that you would identify yourself with", required=True)
@click.option("-p", "--password", "password", help="Enter the chatroom password for decrypting the messages")
@click.option("-c", "--chatroom", "chatroom", help="Enter the chatroom identity you would want to enter in")
@click.option("-s", "--servaddr", "servaddr", help="Enter the server address you would want to connect to", required=True)
@click.version_option(version="04092020", prog_name="SNCTRYZERO Client by t0xic0der")
def mainfunc(username, password, chatroom, servaddr):
    try:
        os.system("clear")
        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <b><seagreen>Starting Sanctuary ZERO v04092020 up...</seagreen></b>"))
        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <seagreen>Connected to '" + servaddr + "' successfully</seagreen>"))
        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <seagreen>Session started at " + str(time.ctime()) + "</seagreen>"))
        if chatroom is None:
            print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <green>A new chatroom was generated</green>"))
            chatroom = randgene()
        else:
            if chekroom(chatroom) is True:
                print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <green>A valid chatroom identity was entered</green>"))
            elif not chatroom.isupper():
                chatroom = chatroom.upper()
                if chekroom(chatroom):
                    print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <green>A valid chatroom identity was entered</green>"))
                else:
                    print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <green>An invalid chatroom identity was entered</green>"))
                    sys.exit()
            else:
                    print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <green>An invalid chatroom identity was entered</green>"))
                    sys.exit()
        if password is None:
            print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <green>A new password was generated</green>"))
            password = Fernet.generate_key().decode("utf8")
        else:
            if chekpass(password) is True:
                print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <green>A valid chatroom password was entered</green>"))
            else:
                print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <green>An invalid chatroom password was entered</green>"))
                sys.exit()
        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <seagreen>Chatroom identity : " + chatroom + "</seagreen>"))
        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <seagreen>Chatroom password : " + password + "</seagreen>"))
        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <seagreen>Share the chatroom identity and password to add members!</seagreen>"))
        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <seagreen>Your conversations are protected with end-to-end encryption</seagreen>"))
        asyncio.get_event_loop().run_until_complete(hello(servaddr, username, chatroom, password))
    except KeyboardInterrupt as EXPT:
        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <red>Leaving SNCTRYZERO...</red>"))
        sys.exit()
    except OSError as EXPT:
        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <red>A connection to the server could not be established</red>"))
        sys.exit()
    except websockets.exceptions.ConnectionClosedError as EXPT:
        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <red>A connection to the server was lost</red>"))
        sys.exit()


if __name__ == "__main__":
    mainfunc()
