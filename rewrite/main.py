import asyncio, websockets, sys, click
from prompt_toolkit import print_formatted_text
from websockets.exceptions import ConnectionClosedError
import json
from server_modules import textdisp, sprtfunc, modutils


WAITAREA = []

USERDICT = {}

gnrlwork = textdisp.GeneralWorking()

'''
USERDICT = {
    "DEADCAFE": {
        "roomownr": "t0xic0der",
        "passhash": "",
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


async def chatroom(websocket, path):
    if not sprtfunc.ServerOperations(USERDICT, WAITAREA, websocket).check_websocket_object_presence():
        WAITAREA.append(websocket)
    try:
        async for mesgjson in websocket:
            mesgdict = json.loads(mesgjson)
            if mesgdict["operands"] == "CHEKUSER":
                await sprtfunc.ServerOperations(USERDICT, WAITAREA, websocket).check_specific_username_presence_in_the_chatroom(mesgdict)
            elif mesgdict["operands"] == "IDENTIFY":
                await sprtfunc.ServerOperations(USERDICT, WAITAREA, websocket).prove_user_identity_inside_a_chatroom(mesgdict)
            elif mesgdict["operands"] == "LISTUSER":
                await sprtfunc.ServerOperations(USERDICT, WAITAREA, websocket).dispatch_list_of_users(mesgdict)
            elif mesgdict["operands"] == "PURRMESG":
                await sprtfunc.ServerOperations(USERDICT, WAITAREA, websocket).whisper_messages_to_a_specific_username(mesgdict)
            elif mesgdict["operands"] == "KICKUSER":
                await sprtfunc.ServerOperations(USERDICT, WAITAREA, websocket).remove_specific_username_from_the_room(mesgdict)
            elif mesgdict["operands"] == "STOPROOM":
                await sprtfunc.ServerOperations(USERDICT, WAITAREA, websocket).initiate_chatroom_shutdown(mesgdict)
            elif mesgdict["operands"] == "FETCOWNR":
                await sprtfunc.ServerOperations(USERDICT, WAITAREA, websocket).fetch_owner_name_of_the_chatroom(mesgdict)
            elif mesgdict["operands"] == "ANONMESG":
                await sprtfunc.ServerOperations(USERDICT, WAITAREA, websocket).anonymously_dispatch_message_to_specific_username(mesgdict)
            elif mesgdict["operands"] == "CONVEYMG":
                await sprtfunc.ServerOperations(USERDICT, WAITAREA, websocket).convey_normal_messages(mesgdict)
    except ConnectionClosedError as EXPT:
        await sprtfunc.ServerOperations(USERDICT, WAITAREA, websocket).handle_broken_connections()


def servenow(netpdata="127.0.0.1", chatport="9696"):
    try:
        start_server = websockets.serve(chatroom, netpdata, int(chatport))
        asyncio.get_event_loop().run_until_complete(start_server)
        gnrlwork.decorate("SNCTRYZERO", "<green>SNCTRYZERO server was started up on 'ws://" + str(netpdata) + ":" + str(chatport) + "/'</green>")
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("")
        gnrlwork.decorate("SNCTRYZERO", "<red><b>SNCTRYZERO server was shut down</b></red>")
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
        gnrlwork.decorate("SNCTRYZERO", "<green><b>Starting SNCTRYZERO server v30102020...</b></green>")
        gnrlwork.decorate("SNCTRYZERO", "Know more about the project at https://github.com/t0xic0der/sanctuary-zero/wiki")
        gnrlwork.decorate("SNCTRYZERO", "Find folks we're thankful to at https://github.com/t0xic0der/sanctuary-zero/graphs/contributors")
        netpdata = ""
        if netprotc == "ipprotv6":
            gnrlwork.decorate("SNCTRYZERO", "<green>IP version : 6</green>")
            netpdata = "::"
            gnrlwork.decorate("SNCTRYZERO", "<green>IP address : " + modutils.obtain_reachable_ip_address(6) + "</green>")
        elif netprotc == "ipprotv4":
            gnrlwork.decorate("SNCTRYZERO", "<green>IP version : 4</green>")
            netpdata = "0.0.0.0"
            gnrlwork.decorate("SNCTRYZERO", "<green>IP address : " + modutils.obtain_reachable_ip_address(4) + "</green>")
        servenow(netpdata, chatport)
    except OSError:
        gnrlwork.decorate("SNCTRYZERO", "<red><b>The server could not be started up</b></red>")


if __name__ == "__main__":
    mainfunc()
