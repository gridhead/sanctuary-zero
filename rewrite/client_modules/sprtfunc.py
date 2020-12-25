import json
import time
from hashlib import sha256

from click import style

from . import textdisp


genrwork = textdisp.GeneralWorking()


class ClientOperations():
    def __init__(self, username, chatroom, servaddr, password, websocket):
        self.username = username
        self.chatroom = chatroom
        self.servaddr = servaddr
        self.password = password
        self.websocket = websocket

    def save_connection_profile_to_file(self):
        try:
            filename = self.username + "_" + self.chatroom + ".conf"
            connsave = {
                "profvers": "24122020",
                "username": self.username,
                "servaddr": self.servaddr,
                "chatroom": self.chatroom,
                "password": self.password,
                "timestmp": time.ctime()
            }
            with open(filename, "w") as connfile:
                json.dump(connsave, connfile)
            genrwork.simple_decorate("SNCTRYZERO", "Connection profile was saved successfully")
        except Exception as EXPT:
            genrwork.simple_decorate("SNCTRYZERO", "Connection profile could not be saved")

    async def check_username_presence(self):
        mesgdict = {
            "username": self.username,
            "operands": "CHEKUSER",
            "mesgtext": "",
            "passhash": sha256(self.password.encode("utf-8")).hexdigest(),
            "chatroom": self.chatroom
        }
        await self.websocket.send(json.dumps(mesgdict))
        async for recvdata in self.websocket:
            return json.loads(recvdata)

    async def identify_yourself(self):
        mesgdict = {
            "username": self.username,
            "operands": "IDENTIFY",
            "mesgtext": "",
            "chatroom": self.chatroom
        }
        await self.websocket.send(json.dumps(mesgdict))

    async def initiate_chatroom_shutdown(self):
        mesgdict = {
            "username": self.username,
            "operands": "STOPROOM",
            "mesgtext": "",
            "chatroom": self.chatroom,
        }
        senddata = json.dumps(mesgdict)
        await self.websocket.send(senddata)

    async def fetch_list_of_users_connected_to_chatroom(self):
        mesgdict = {
            "username": self.username,
            "operands": "LISTUSER",
            "mesgtext": "",
            "chatroom": self.chatroom,
        }
        senddata = json.dumps(mesgdict)
        await self.websocket.send(senddata)

    def show_help_and_support_topics(self):
        helplist = [
            style("/list", bold=True) + " - " + "Fetch the list of users connected to chatroom",
            style("/save", bold=True) + " - " + "Save current connection to a file",
            style("/wipe", bold=True) + " - " + "Clear the client-side screen buffer",
            style("/ownr", bold=True) + " - " + "Fetch the owner name of the chatroom",
            style("/stop", bold=True) + " - " + "Shut down the chatroom and remove all users",
            style("/purr <username> <mesgtext>", bold=True) + " - " + "Whisper messages to a specific user in the chatroom",
            style("/anon <username> <mesgtext>", bold=True) + " - " + "Anonymously dispatch messages to a specific user",
            style("/kick <username>", bold=True) + " - " + "Remove a user from the chatroom",
            style("/help", bold=True) + " - " + "Show help and support topics"
        ]
        genrwork.simple_decorate("SNCTRYZERO", "Following options are at your disposal")
        for indx in helplist:
            print(" " * 24 + textdisp.HelperDisplay().wrap_conversational_text(indx))

    async def fetch_owner_name_of_the_chatroom(self):
        mesgdict = {
            "username": self.username,
            "operands": "FETCOWNR",
            "mesgtext": "",
            "chatroom": self.chatroom,
        }
        senddata = json.dumps(mesgdict)
        await self.websocket.send(senddata)

    async def remove_username_from_the_chatroom(self, mesgtext):
        if len(mesgtext.strip().split()) == 2:
            destuser = mesgtext.strip().split()[1]
            if destuser == self.username:
                genrwork.simple_decorate("SNCTRYZERO", "You cannot remove yourself from the chatroom")
            else:
                mesgdict = {
                    "username": self.username,
                    "operands": "KICKUSER",
                    "mesgtext": "",
                    "destuser": destuser,
                    "chatroom": self.chatroom,
                }
                senddata = json.dumps(mesgdict)
                await self.websocket.send(senddata)
        else:
            genrwork.simple_decorate("SNCTRYZERO", "Please correct your removal syntax and try again")

    async def whisper_message_to_specific_username(self, mesgtext, cphrsuit):
        if len(mesgtext.strip().split()) >= 3:
            destuser = mesgtext.strip().split()[1]
            if destuser == self.username:
                genrwork.simple_decorate("SNCTRYZERO", "You cannot whisper messages to yourself")
            else:
                mesgtext = mesgtext.replace("/purr", "").strip()
                mesgtext = mesgtext.replace(destuser, "").strip()
                mesgdict = {
                    "username": self.username,
                    "operands": "PURRMESG",
                    "mesgtext": cphrsuit.encrtext(mesgtext.strip()),
                    "destuser": destuser,
                    "chatroom": self.chatroom,
                }
                senddata = json.dumps(mesgdict)
                await self.websocket.send(senddata)
        else:
            genrwork.simple_decorate("SNCTRYZERO", "Please correct your whisper syntax and try again")

    async def anonymously_dispatch_to_specific_username(self, mesgtext, cphrsuit):
        if len(mesgtext.strip().split()) >= 3:
            destuser = mesgtext.strip().split()[1]
            if destuser == self.username:
                genrwork.simple_decorate("SNCTRYZERO", "You cannot anonymously dispatch messages to yourself")
            else:
                mesgtext = mesgtext.replace("/anon", "").strip()
                mesgtext = mesgtext.replace(destuser, "").strip()
                mesgdict = {
                    "username": self.username,
                    "operands": "ANONMESG",
                    "mesgtext": cphrsuit.encrtext(mesgtext.strip()),
                    "destuser": destuser,
                    "chatroom": self.chatroom,
                }
                senddata = json.dumps(mesgdict)
                await self.websocket.send(senddata)
        else:
            genrwork.simple_decorate("SNCTRYZERO", "Please correct your anonymous dispatch syntax and try again")

    async def send_normal_message(self, mesgtext, cphrsuit):
        mesgdict = {
            "username": self.username,
            "operands": "CONVEYMG",
            "mesgtext": cphrsuit.encrtext(mesgtext.strip()),
            "chatroom": self.chatroom,
        }
        senddata = json.dumps(mesgdict)
        await self.websocket.send(senddata)
