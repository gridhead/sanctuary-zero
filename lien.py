from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
import asyncio, websockets, sys, click, time


async def my_coroutine():
    session = PromptSession()
    while True:
        with patch_stdout():
            result = await session.prompt_async('Say something: ')
        print("< [" + str(time.ctime()) + "] " + str(result))
        await notify_mesej(result)


USERS = set()


async def notify_mesej(message):
    if USERS:
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    print("> [" + str(time.ctime()) + "] [USERJOIN] User just joined the Sanctuary")


async def unregister(websocket):
    USERS.remove(websocket)
    print("> [" + str(time.ctime()) + "] [USERLEFT] User just left the Sanctuary")


async def chatroom(websocket, path):
    await register(websocket)
    try:
        async for message in websocket:
            decmesg = base64.b64decode(message)
            print("< [" + str(time.ctime()) + "] " + str(decmesg))
            await notify_mesej(decmesg)
    finally:
        await unregister(websocket)


def servenow(netpdata="127.0.0.1", chatport="9696"):
    try:
        print("> [" + str(time.ctime()) + "] [HOLAUSER] Sanctuary was started up on 'ws://" + str(netpdata) + ":" + str(chatport) + "/'")
        start_server = websockets.serve(chatroom, netpdata, int(chatport))
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_until_complete(my_coroutine())
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("\n" + "> [" + str(time.ctime()) + "] [SEEUSOON] Sanctuary was shut down")
        sys.exit()


@click.command()
@click.option("-c", "--chatport", "chatport", help="Set the port value for WebSockets [0-65536]", required=True)
@click.option("-6", "--ipprotv6", "netprotc", flag_value="ipprotv6", help="Start the server on an IPv6 address", required=True)
@click.option("-4", "--ipprotv4", "netprotc", flag_value="ipprotv4", help="Start the server on an IPv4 address", required=True)
@click.version_option(version="15082020", prog_name="Sanctuary ZERO Server by t0xic0der")
def mainfunc(chatport, netprotc):
    print("> [" + str(time.ctime()) + "] [HOLAUSER] Starting Sanctuary...")
    netpdata = ""
    if netprotc == "ipprotv6":
        print("> [" + str(time.ctime()) + "] [HOLAUSER] IP version : 6")
        netpdata = "::"
    elif netprotc == "ipprotv4":
        print("> [" + str(time.ctime()) + "] [HOLAUSER] IP version : 4")
        netpdata = "0.0.0.0"
    servenow(netpdata, chatport)


if __name__ == "__main__":
    mainfunc()
