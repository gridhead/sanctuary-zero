import asyncio, websockets, time, json, click, secrets
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit import print_formatted_text, HTML

#cd Projects/sanctuary-zero && source venv/bin/activate && python3 cnew.py -u t0xic0der

session = PromptSession()
USERLIST = set()


async def consumer_handler(websocket, username, chatroom):
    async for recvdata in websocket:
        try:
            recvjson = json.loads(recvdata)
            if recvjson["chatroom"] == chatroom:
                if recvjson["username"] != username:
                    print("< [" + str(time.ctime()) + "] | " + recvjson["username"] + " | " + recvjson["mesgtext"])
        except Exception as EXPT:
            pass


async def producer_handler(websocket, username, chatroom):
    footelem = HTML("<b><style bg='ansired'>" + username.strip() + "</style></b>@<b><style bg='ansiblue'>" + chatroom + "</style></b> - <b><style bg='ansiblue'>Sanctuary ZERO v15082020</style></b>")
    while True:
        with patch_stdout():
            mesgtext = await session.prompt_async("> [" + str(time.ctime()) + "] | " + str(username) + " | ", bottom_toolbar=footelem)
        senddata = json.dumps({"username": username, "chatroom": chatroom, "mesgtext": mesgtext})
        await websocket.send(senddata)


async def hello(servaddr, username, chatroom):
    async with websockets.connect(servaddr) as websocket:
        prod = asyncio.get_event_loop().create_task(producer_handler(websocket, str(username), str(chatroom)))
        cons = asyncio.get_event_loop().create_task(consumer_handler(websocket, str(username), str(chatroom)))
        await websocket.send(str(username) + " has joined the chatroom.")
        await prod
        await cons
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

def formusnm(username):
    if len(username) < 10:
        return username + " " * (10 - len(username))
    elif len(username) > 10:
        return username[0:10]
    else:
        return username


@click.command()
@click.option("-u", "--username", "username", help="Enter the username that you would identify yourself with", required=True)
@click.option("-c", "--chatroom", "chatroom", help="Enter the chatroom identity you would want to enter in")
@click.option("-s", "--servaddr", "servaddr", help="Enter the server address you would want to connect to", required=True)
@click.version_option(version="15082020", prog_name="Sanctuary ZERO by t0xic0der")
def mainfunc(username, chatroom, servaddr):
    print_formatted_text(HTML("* <gray>[" + str(time.ctime()) + "]</gray> " + "<b><seagreen>Starting Sanctuary ZERO v15082020 up...</seagreen></b>"))
    print_formatted_text(HTML("* <gray>[" + str(time.ctime()) + "]</gray> " + "<lightgreen>Connected to " + servaddr + " successfully</lightgreen>"))
    username = formusnm(username)
    if chatroom is None:
        print_formatted_text(HTML("* <gray>[" + str(time.ctime()) + "]</gray> " + "<yellow>Welcome " + username.strip() + "! You have joined a newly created chatroom</yellow>"))
        chatroom = randgene()
    elif chekroom(chatroom):
        print_formatted_text(HTML("* <gray>[" + str(time.ctime()) + "]</gray> " + "<yellow>Welcome " + username.strip() + "! You have joined the specified chatroom</yellow>"))
    print_formatted_text(HTML("* <gray>[" + str(time.ctime()) + "]</gray> " + "<lightgreen>Chatroom identity [" + chatroom.upper() + "] - Share to add members</lightgreen>"))
    asyncio.get_event_loop().run_until_complete(hello(servaddr, username, chatroom))


if __name__ == "__main__":
    mainfunc()