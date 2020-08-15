import asyncio, websockets, time, json, click, secrets
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit import print_formatted_text, HTML


session = PromptSession()
uri = "ws://localhost:9696"


async def consumer_handler(websocket, username, chatroom):
    async for message in websocket:
        print("< [" + str(time.ctime()) + "] " + str(message))


async def producer_handler(websocket, username, chatroom):
    while True:
        with patch_stdout():
            result = await session.prompt_async("> [" + str(time.ctime()) + "] ", rprompt=username)
        await websocket.send(result)


async def hello(username, chatroom):
    async with websockets.connect(uri) as websocket:
        await websocket.send(str(username) + " has joined the chatroom.")
        cons = asyncio.get_event_loop().create_task(consumer_handler(websocket, username, chatroom))
        prod = asyncio.get_event_loop().create_task(producer_handler(websocket, username, chatroom))
        await cons
        await prod
        asyncio.get_event_loop().run_forever()


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
            return True
        except ValueError:
            return False


@click.command()
@click.option("-u", "--username", "username", help="Enter the username that you would identify yourself with", required=True)
@click.option("-c", "--chatroom", "chatroom", help="Enter the chatroom name you would want to enter in")
@click.version_option(version="15082020", prog_name="Sanctuary ZERO by t0xic0der")
def mainfunc(username, chatroom):
    if chatroom is None:
        print("< [" + str(time.ctime()) + "] A new chatroom was created as a chatroom name was not provided")
        chatroom = randgene()
    elif chekroom(chatroom):
        print("< [" + str(time.ctime()) + "] You have joined the specified chatroom ")
    print("< [" + str(time.ctime()) + "] Chatroom ID " + chatroom.upper() + " - Share for people to join in")
    asyncio.get_event_loop().run_until_complete(hello(username, chatroom))


if __name__ == "__main__":
    mainfunc()