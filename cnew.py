import asyncio, websockets, time, json, click, secrets, os, sys
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.validation import Validator, ValidationError
from cryptography.fernet import Fernet
from utils.helper_display import HelperDisplay


sess = PromptSession()
sepr = chr(969696)
websocket = None
helper_display = HelperDisplay()


class emtyfind(Validator):
    def validate(self, document):
        if document.text.strip() == "":
            raise ValidationError(message="You cannot send an empty message ")


class fernetst():
    def __init__(self, pswd):
        self.suit = Fernet(pswd)

    def encrjson(self, data):
        return self.suit.encrypt(data.encode("utf8")).decode("utf8")

    def decrjson(self, data):
        return self.suit.decrypt(data.encode("utf8")).decode("utf8")

class emtyfind(Validator):
    def validate(self, document):
        text = document.text
        if text.strip() == "":
            raise ValidationError(message="You cannot send an empty message")

async def consumer_handler(cphrsuit, username, chatroom, servaddr):
    async for recvdata in websocket:
        try:
            if recvdata.split(sepr)[0] == "SNCTRYZERO" and recvdata.split(sepr)[1] == "USERJOINED" and recvdata.split(sepr)[3] == chatroom:
                print("[" + obtntime() + "] USERJOINED > " + recvdata.split(sepr)[2] + " joined - " + recvdata.split(sepr)[4] + " are connected - Indexes updated")
            elif recvdata.split(sepr)[0] == "SNCTRYZERO" and recvdata.split(sepr)[1] == "USEREXITED" and recvdata.split(sepr)[3] == chatroom:
                print("[" + obtntime() + "] USEREXITED > " + recvdata.split(sepr)[2] + " left - " + recvdata.split(sepr)[4] + " are connected - Indexes updated")
            elif recvdata.split(sepr)[0] == "SNCTRYZERO" and recvdata.split(sepr)[1] == "USERSLIST" and recvdata.split(sepr)[3] == chatroom:
                print("[" + obtntime() + "] USERSLIST > " + recvdata.split(sepr)[2] + " are connected")
            else:
                recvjson = json.loads(cphrsuit.decrjson(recvdata))
                if recvjson["chatroom"] == chatroom and recvjson["username"] != username:
                    print("[" + obtntime() + "] " + formusnm(recvjson["username"]) + " > " + helper_display.wrap_conversational_text(recvjson["mesgtext"]))
        except Exception as EXPT:
            pass


async def producer_handler(cphrsuit, username, chatroom, servaddr):
    try:
        footelem = HTML("<b>[" + chatroom + "]</b>" + " <b>" + username.strip() + "</b> > End-to-end encryption enabled on '" + servaddr + "' - Hit Ctrl+C to EXIT")
        while True:
            with patch_stdout():
                mesgtext = await sess.prompt_async(lambda:"[" + obtntime() + "] " + formusnm(str(username)) + " > ", bottom_toolbar=footelem, validator=emtyfind(), refresh_interval=0.5, prompt_continuation=lambda width, line_number, is_soft_wrap: " " * width)
            if mesgtext.strip() == "/list":
                senddata = mesgtext.strip()
            else:
                senddata = json.dumps({"username": username.strip(), "chatroom": chatroom, "mesgtext": mesgtext.strip()})
                senddata = cphrsuit.encrjson(senddata)
            await websocket.send(senddata)
    except EOFError:
        raise KeyboardInterrupt

async def hello(servaddr, username, chatroom, password):
    prod = asyncio.get_event_loop().create_task(producer_handler(cphrsuit, str(username), str(chatroom), str(servaddr)))
    cons = asyncio.get_event_loop().create_task(consumer_handler(cphrsuit, str(username), str(chatroom), str(servaddr)))
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

async def chekroom(username,chatroom,password,servaddr):
    if len(chatroom)!=8:
        return False
    try:
        geee = int(chatroom,16)
    except ValueError:
        return False
    global websocket
    websocket = await websockets.connect(servaddr)
    await websocket.send('CHKUSR'+sepr+username+sepr+chatroom+sepr+password)
    response = await websocket.recv()
    return response

def formusnm(username):
    if len(username) < 10:      return username + " " * (10 - len(username))
    elif len(username) > 10:    return username[0:10]
    else:                       return username

async def askserver(username,servaddr):
    global websocket 
    websocket = await websockets.connect(servaddr)
    await websocket.send('NEW'+sepr+username)
    response = await websocket.recv()
    return response

@click.command()
@click.option("-u", "--username", "username", help="Enter the username that you would identify yourself with", required=True)
@click.option("-p", "--password", "password", help="Enter the chatroom password for decrypting the messages")
@click.option("-c", "--chatroom", "chatroom", help="Enter the chatroom identity you would want to enter in")
@click.option("-s", "--servaddr", "servaddr", help="Enter the server address you would want to connect to", required=True)
@click.version_option(version="18102020", prog_name="SNCTRYZERO client")
def mainfunc(username, password, chatroom, servaddr):
    '''
    Added the server side generation of chatroom id
    To request to join a server, ask if the supplied chatroom is valid in server
    '''
    try:
        click.clear()
        print_formatted_text("\n")
        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <b><seagreen>Starting Sanctuary ZERO v18102020 up...</seagreen></b>"))
        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <seagreen>Attempted connection to '" + servaddr + "' at " + str(time.ctime()) + "</seagreen>"))

        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <seagreen>Chatroom identity : " + chatroom + "</seagreen>"))
        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <seagreen>Chatroom password : " + password + "</seagreen>"))
        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <seagreen>Share the chatroom identity and password to add members!</seagreen>"))
        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <seagreen>Your conversations are protected with end-to-end encryption</seagreen>"))
        asyncio.get_event_loop().run_until_complete(hello(username, chatroom, password,servaddr))

        if username.strip() != "":
            if chatroom is None:
                print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <green>A new chatroom was generated</green>"))
                # if i don't have chatroom, no password will be supplied
                output = asyncio.get_event_loop().run_until_complete(askserver(username, servaddr))
                chatroom = output.split(sepr)[0]
                password = output.split(sepr)[1]
            else:
                if not chatroom.isupper():
                    chatroom = chatroom.upper()
                isValid = asyncio.get_event_loop().run_until_complete(chekroom(username,chatroom,password,servaddr))
                if isValid == "True":
                    print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <green>A valid credential was entered</green>"))
                elif isValid == "False":
                    print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <green>An invalid credential was entered</green>"))
                    sys.exit()
        else:
            print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <red>An invalid username was entered</red>"))
            sys.exit()
        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <seagreen><b>Identity</b> " + chatroom + " > <b>Password</b> " + password + "</seagreen>"))
        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <seagreen>Share the chatroom identity, password and server address to invite members</seagreen>"))
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