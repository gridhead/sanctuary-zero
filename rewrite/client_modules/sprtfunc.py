import time
import json
import os
import textwrap


class HelperDisplay:
    """
    Utility Helper for Displaying Data
    Current methods:
        1.) wrap_text
        2.) wrap_conversational_text
        3.) _get_width -> internal use
    """
    def wrap_text(self, message: str, indent: int = 24) -> str:
        """ Wrap general texts """
        wrapped_message = str()
        indent_text = " " * indent
        message_width = len(message)
        width = self._get_width(indent)
        for i in range(0, message_width, width):
            if i > 0:
                wrapped_message += indent_text
            wrapped_message += message[i: i + width]
            if i < message_width - width:
                wrapped_message += "\n"
        return wrapped_message

    def wrap_conversational_text(self, message: str, indent: int = 24) -> str:
        """ Wrap conversational texts which are broken by words """
        width = self._get_width(indent)
        wrapped_lines = textwrap.wrap(message, width=width)
        if len(wrapped_lines) == 1:
            wrapped_message = self.wrap_text(wrapped_lines[0])
            return wrapped_message
        wrapped_message = str()
        for idx, line in enumerate(wrapped_lines):
            indent_text = " " * indent if idx > 0 else ""
            new_line = "\n" if idx < len(wrapped_lines) - 1 else ""
            indented_line = indent_text + line + new_line
            wrapped_message += indented_line
        return wrapped_message

    def _get_width(self, indent: int = 24) -> int:
        """ Get the current width based on the terminal size """
        max_width = os.get_terminal_size()[0]
        return max_width - indent


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


class ClientOperations():
    def __init__(self, username, chatroom, websocket):
        self.username = username
        self.chatroom = chatroom
        self.websocket = websocket

    async def chk_username_presence(self):
        mesgdict = {
            "username": self.username,
            "operands": "CHEKUSER",
            "mesgtext": "",
            "chatroom": self.chatroom
        }
        await self.websocket.send(json.dumps(mesgdict))
        async for recvdata in self.websocket:
            return recvdata

    async def identify_yourself(self):
        mesgdict = {
            "username": self.username,
            "operands": "IDENTIFY",
            "mesgtext": "",
            "chatroom": self.chatroom
        }
        await self.websocket.send(json.dumps(mesgdict))

    async def fetch_list_of_users_connected_to_chatroom(self):
        mesgdict = {
            "username": self.username,
            "operands": "LISTUSER",
            "mesgtext": "",
            "chatroom": self.chatroom,
        }
        senddata = json.dumps(mesgdict)
        await self.websocket.send(senddata)

    async def remove_username_from_the_chatroom(self, mesgtext):
        if len(mesgtext.strip().split()) == 2:
            destuser = mesgtext.strip().split()[1]
            if destuser == self.username:
                print("[" + obtntime() + "] " + "SNCTRYZERO" + " > " + helper_display.wrap_conversational_text("You cannot remove yourself from the chatroom"))
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
            print("[" + obtntime() + "] " + "SNCTRYZERO" + " > " + helper_display.wrap_conversational_text("Please correct your removal syntax and try again"))

    async def whisper_message_to_specific_username(self, mesgtext):
        if len(mesgtext.strip().split()) >= 3:
            destuser = mesgtext.strip().split()[1]
            if destuser == self.username:
                print("[" + obtntime() + "] " + "SNCTRYZERO" + " > " + helper_display.wrap_conversational_text("You cannot whisper messages to yourself"))
            else:
                mesgtext = mesgtext.replace("/purr", "").strip()
                mesgtext = mesgtext.replace(destuser, "").strip()
                mesgdict = {
                    "username": self.username,
                    "operands": "PURRMESG",
                    "mesgtext": mesgtext,
                    "destuser": destuser,
                    "chatroom": self.chatroom,
                }
                senddata = json.dumps(mesgdict)
                await self.websocket.send(senddata)
        else:
            print("[" + obtntime() + "] " + "SNCTRYZERO" + " > " + helper_display.wrap_conversational_text("Please correct your whisper syntax and try again"))

    async def anonymously_dispatch_to_specific_username(self, mesgtext):
        if len(mesgtext.strip().split()) >= 3:
            destuser = mesgtext.strip().split()[1]
            if destuser == self.username:
                print("[" + obtntime() + "] " + "SNCTRYZERO" + " > " + helper_display.wrap_conversational_text("You cannot anonymously dispatch to yourself"))
            else:
                mesgtext = mesgtext.replace("/anon", "").strip()
                mesgtext = mesgtext.replace(destuser, "").strip()
                mesgdict = {
                    "username": self.username,
                    "operands": "ANONMESG",
                    "mesgtext": mesgtext,
                    "destuser": destuser,
                    "chatroom": self.chatroom,
                }
                senddata = json.dumps(mesgdict)
                await self.websocket.send(senddata)
        else:
            print("[" + obtntime() + "] " + "SNCTRYZERO" + " > " + helper_display.wrap_conversational_text("Please correct your anonymous dispatch syntax and try again"))

    async def send_normal_message(self, mesgtext):
        mesgdict = {
            "username": self.username,
            "operands": "CONVEYMG",
            "mesgtext": mesgtext.strip(),
            "chatroom": self.chatroom,
        }
        senddata = json.dumps(mesgdict)
        # senddata = cphrsuit.encrjson(senddata)
        await self.websocket.send(senddata)
