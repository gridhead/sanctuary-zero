import asyncio, websockets, time, json, click, secrets, os, sys, socket
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit import print_formatted_text, HTML
from cryptography.fernet import Fernet
from utils.helper_display import HelperDisplay
from client_modules import sprtfunc, modutils

obtntime = sprtfunc.obtntime

sess = PromptSession()
sepr = chr(969696)
helper_display = HelperDisplay()
closesig = False


async def consumer_handler(cphrsuit, websocket, username, chatroom, servaddr):
    async for recvjson in websocket:
        try:
            recvdict = json.loads(recvjson)
            if recvdict["operands"] == "CONVEYMG" and recvdict["username"] != username:
                print("[" + obtntime() + "] " + modutils.formusnm(recvdict["username"]) + " > " + helper_display.wrap_conversational_text(recvdict["mesgtext"]))
            elif recvdict["operands"] == "LEFTMESG":
                print("[" + obtntime() + "] " + modutils.formusnm(recvdict["username"]) + " > " + helper_display.wrap_conversational_text(recvdict["mesgtext"]))
            elif recvdict["operands"] == "USERJOIN":
                print("[" + obtntime() + "] " + modutils.formusnm(recvdict["username"]) + " > " + helper_display.wrap_conversational_text(recvdict["mesgtext"]))
            elif recvdict["operands"] == "PURRFAIL":
                print("[" + obtntime() + "] " + modutils.formusnm(recvdict["username"]) + " > " + helper_display.wrap_conversational_text(recvdict["mesgtext"]))
            elif recvdict["operands"] == "PURRMESG":
                print("[" + obtntime() + "] " + modutils.formusnm(recvdict["username"]) + " > " + helper_display.wrap_conversational_text(recvdict["mesgtext"]))
            elif recvdict["operands"] == "ANONFAIL":
                print("[" + obtntime() + "] " + modutils.formusnm(recvdict["username"]) + " > " + helper_display.wrap_conversational_text(recvdict["mesgtext"]))
            elif recvdict["operands"] == "ANONMESG":
                print("[" + obtntime() + "] " + modutils.formusnm(recvdict["username"]) + " > " + helper_display.wrap_conversational_text(recvdict["mesgtext"]))
            elif recvdict["operands"] == "KICKFAIL":
                print("[" + obtntime() + "] " + modutils.formusnm(recvdict["username"]) + " > " + helper_display.wrap_conversational_text(recvdict["mesgtext"]))
            elif recvdict["operands"] == "KICKUSER":
                print("[" + obtntime() + "] " + modutils.formusnm(recvdict["username"]) + " > " + helper_display.wrap_conversational_text("You were removed from the chatroom"))
            elif recvdict["operands"] == "USERLIST":
                print("[" + obtntime() + "] " + modutils.formusnm(recvdict["username"]) + " > " + helper_display.wrap_conversational_text("Following users are connected"))
                userlist = recvdict["mesgtext"].split()
                for indx in userlist:
                    print(" " * 24 + helper_display.wrap_conversational_text(indx))
        except Exception as EXPT:
            pass


async def producer_handler(cphrsuit, websocket, username, chatroom, servaddr, clenoprs):
    try:
        footelem = HTML("<b>[" + chatroom + "]</b>" + " <b>" + username.strip() + "</b> > End-to-end encryption enabled on '" + servaddr + "' - Hit Ctrl+C to EXIT")
        while True:
            with patch_stdout():
                mesgtext = await sess.prompt_async(lambda: "[" + obtntime() + "] " + modutils.formusnm(str(username)) + " > ", bottom_toolbar=footelem, validator=modutils.emtyfind(), refresh_interval=0.5, prompt_continuation=lambda width, line_number, is_soft_wrap: " " * width)
            if mesgtext.strip() == "/list":
                await clenoprs.fetch_list_of_users_connected_to_chatroom();
            elif mesgtext.strip().split()[0] == "/kick":
                await clenoprs.remove_username_from_the_chatroom(mesgtext)
            elif mesgtext.strip().split()[0] == "/purr":
                await clenoprs.whisper_message_to_specific_username(mesgtext)
            elif mesgtext.strip().split()[0] == "/anon":
                await clenoprs.anonymously_dispatch_to_specific_username(mesgtext)
            else:
                await clenoprs.send_normal_message(mesgtext)
    except EOFError:
        raise KeyboardInterrupt


async def hello(servaddr, username, chatroom, password):
    async with websockets.connect(servaddr) as websocket:
        try:
            clenoprs = sprtfunc.ClientOperations(username, chatroom, websocket)
            chkUserPresence = await clenoprs.chk_username_presence()
            print(chkUserPresence)
            if chkUserPresence == "False":
                cphrsuit = modutils.fernetst(password.encode("utf8"))
                prod = asyncio.get_event_loop().create_task(producer_handler(cphrsuit, websocket, str(username), str(chatroom), str(servaddr), clenoprs))
                cons = asyncio.get_event_loop().create_task(consumer_handler(cphrsuit, websocket, str(username), str(chatroom), str(servaddr)))
                await clenoprs.identify_yourself()
                await prod
                await cons
                asyncio.get_event_loop().run_forever()
            else:
                print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <red>Username already exist in chatroom</red>"))
                await websocket.close()
                sys.exit()
        except Exception as EXPT:
            if websocket.closed:
                print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <red>A connection to the server was lost</red>".format(EXPT)))
            raise KeyboardInterrupt


@click.command()
@click.option("-u", "--username", "username", help="Enter the username that you would identify yourself with", required=True)
@click.option("-p", "--password", "password", help="Enter the chatroom password for decrypting the messages")
@click.option("-c", "--chatroom", "chatroom", help="Enter the chatroom identity you would want to enter in")
@click.option("-s", "--servaddr", "servaddr", help="Enter the server address you would want to connect to", required=True)
@click.version_option(version="30102020", prog_name="SNCTRYZERO client")
def mainfunc(username, password, chatroom, servaddr):
    try:
        click.clear()
        print_formatted_text("\n")
        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <b><seagreen>Starting Sanctuary ZERO v30102020 up...</seagreen></b>"))
        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <seagreen>Attempted connection to '" + servaddr + "' at " + str(time.ctime()) + "</seagreen>"))
        if not modutils.check_socket(servaddr):
            print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <red>Attempted connection to '" + servaddr + "' failed at " + str(time.ctime()) +" due to invalid url" "</red>"))
            sys.exit()
        if username.strip() != "":
            if chatroom is None:
                print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <green>A new chatroom was generated</green>"))
                chatroom = modutils.randgene()
            else:
                if modutils.chekroom(chatroom) is True:
                    print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <green>A valid chatroom identity was entered</green>"))
                elif not chatroom.isupper():
                    chatroom = chatroom.upper()
                    if modutils.chekroom(chatroom):
                        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <green>A valid chatroom identity was entered</green>"))
                    else:
                        print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <red>An invalid chatroom identity was entered</red>"))
                        sys.exit()
                else:
                    print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <red>An invalid chatroom identity was entered</red>"))
                    sys.exit()
            if password is None:
                print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <green>A new password was generated</green>"))
                password = Fernet.generate_key().decode("utf8")
            else:
                if modutils.chekpass(password) is True:
                    print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <green>A valid chatroom password was entered</green>"))
                else:
                    print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <red>An invalid chatroom password was entered</red>"))
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
