import asyncio, websockets, sys, click, time, os
from prompt_toolkit import print_formatted_text, HTML


USERS = set()


def obtntime():
    timestmp = time.localtime()
    timehour = str(timestmp.tm_hour)
    timemint = str(timestmp.tm_min)
    timesecs = str(timestmp.tm_sec)
    if int(timehour) < 10:
        timehour = "0" + timehour
    if int(timemint) < 10:
        timemint = "0" + timemint
    if int(timesecs) < 10:
        timesecs = "0" + timesecs
    timestrg = timehour + ":" + timemint + ":" + timesecs
    return timestrg


async def notify_mesej(message):
    if USERS:
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    print_formatted_text(HTML("<gray>[" + obtntime() + "]</gray> " + "<b>SNCTRYZERO</b> ⮞ <yellow>A user just joined the SNCTRYZERO</yellow>"))


async def unregister(websocket):
    USERS.remove(websocket)
    print_formatted_text(HTML("<gray>[" + obtntime() + "]</gray> " + "<b>SNCTRYZERO</b> ⮞ <yellow>A user just left the SNCTRYZERO</yellow>"))


async def chatroom(websocket, path):
    await register(websocket)
    try:
        async for mesgjson in websocket:
            print_formatted_text(HTML("<gray>[" + obtntime() + "]</gray> " + "<b>SNCTRYZERO</b> ⮞ " + str(mesgjson)))
            await notify_mesej(mesgjson)
    except Exception as EXPT:
        await unregister(websocket)


def servenow(netpdata="127.0.0.1", chatport="9696"):
    try:
        print_formatted_text(HTML("<gray>[" + obtntime() + "]</gray> " + "<b>SNCTRYZERO</b> ⮞ <lightgreen>SNCTRYZERO was started up on 'ws://" + str(netpdata) + ":" + str(chatport) + "/'</lightgreen>"))
        start_server = websockets.serve(chatroom, netpdata, int(chatport))
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("")
        print_formatted_text(HTML("<gray>[" + obtntime() + "]</gray> " + "<b>SNCTRYZERO</b> ⮞ <yellow>SNCTRYZERO was shut down</yellow>"))
        sys.exit()


@click.command()
@click.option("-c", "--chatport", "chatport", help="Set the port value for the server [0-65536]", required=True)
@click.option("-6", "--ipprotv6", "netprotc", flag_value="ipprotv6", help="Start the server on an IPv6 address", required=True)
@click.option("-4", "--ipprotv4", "netprotc", flag_value="ipprotv4", help="Start the server on an IPv4 address", required=True)
@click.version_option(version="18082020", prog_name="SNCTRYZERO Server by t0xic0der")
def mainfunc(chatport, netprotc):
    os.system("clear")
    print_formatted_text(HTML("<gray>[" + obtntime() + "]</gray> " + "<b>SNCTRYZERO</b> ⮞ <lightgreen><b>Starting SNCTRYZERO v18082020...</b></lightgreen>"))
    netpdata = ""
    if netprotc == "ipprotv6":
        print_formatted_text(HTML("<gray>[" + obtntime() + "]</gray> " + "<b>SNCTRYZERO</b> ⮞ <lightgreen>IP version : 6</lightgreen>"))
        netpdata = "::"
    elif netprotc == "ipprotv4":
        print_formatted_text(HTML("<gray>[" + obtntime() + "]</gray> " + "<b>SNCTRYZERO</b> ⮞ <lightgreen>IP version : 4</lightgreen>"))
        netpdata = "0.0.0.0"
    try:
        servenow(netpdata, chatport)
    except OSError:
        print_formatted_text(HTML("<gray>[" + obtntime() + "]</gray> " + "<b>SNCTRYZERO</b> ⮞ <yellow>The server could not be started up</yellow>"))


if __name__ == "__main__":
    mainfunc()