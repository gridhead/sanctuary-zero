"""
##########################################################################
*
*   Copyright © 2019-2020 Akashdeep Dhar <t0xic0der@fedoraproject.org>
*
*   This program is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   This program is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <https://www.gnu.org/licenses/>.
*
##########################################################################
"""

import asyncio
import json
import sys
import time
from json.decoder import JSONDecodeError

import click
import websockets
from client_modules import modutils, sprtfunc, textdisp
from prompt_toolkit import HTML, PromptSession, print_formatted_text
from prompt_toolkit.patch_stdout import patch_stdout


genrwork = textdisp.GeneralWorking()

sess = PromptSession()


async def consumer_handler(cphrsuit, websocket, username):
    async for recvjson in websocket:
        try:
            recvdict = json.loads(recvjson)
            if recvdict["operands"] == "CONVEYMG" and recvdict["username"] != username:
                genrwork.simple_decorate(recvdict["username"], cphrsuit.decrtext(recvdict["mesgtext"]))
            elif recvdict["operands"] == "LEFTMESG":
                genrwork.simple_decorate(recvdict["username"], recvdict["mesgtext"])
            elif recvdict["operands"] == "USERJOIN":
                genrwork.simple_decorate(recvdict["username"], recvdict["mesgtext"])
            elif recvdict["operands"] == "PURRFAIL":
                genrwork.simple_decorate(recvdict["username"], recvdict["mesgtext"])
            elif recvdict["operands"] == "PURRMESG":
                genrwork.simple_decorate(recvdict["username"], cphrsuit.decrtext(recvdict["mesgtext"]))
            elif recvdict["operands"] == "ANONFAIL":
                genrwork.simple_decorate(recvdict["username"], recvdict["mesgtext"])
            elif recvdict["operands"] == "ANONMESG":
                genrwork.simple_decorate(recvdict["username"], cphrsuit.decrtext(recvdict["mesgtext"]))
            elif recvdict["operands"] == "KICKFAIL":
                genrwork.simple_decorate(recvdict["username"], recvdict["mesgtext"])
            elif recvdict["operands"] == "KICKNOTE":
                genrwork.simple_decorate(recvdict["username"], recvdict["mesgtext"])
            elif recvdict["operands"] == "STOPNOTE":
                genrwork.simple_decorate(recvdict["username"], recvdict["mesgtext"])
            elif recvdict["operands"] == "STOPFAIL":
                genrwork.simple_decorate(recvdict["username"], recvdict["mesgtext"])
            elif recvdict["operands"] == "KICKUSER":
                genrwork.simple_decorate(recvdict["username"], recvdict["mesgtext"])
            elif recvdict["operands"] == "FETCOWNR":
                genrwork.simple_decorate(recvdict["username"], recvdict["mesgtext"])
            elif recvdict["operands"] == "USERLIST":
                genrwork.simple_decorate(recvdict["username"], "Following users are connected")
                userlist = recvdict["mesgtext"].split()
                for indx in userlist:
                    print(" " * 24 + textdisp.HelperDisplay().wrap_conversational_text(indx))
        except Exception as EXPT:
            pass


async def producer_handler(cphrsuit, clenoprs):
    try:
        footelem = HTML("<b>[" + clenoprs.chatroom + "]</b>" + " <b>" + clenoprs.username + \
                        "</b> > End-to-end encryption enabled on '" + clenoprs.servaddr + "' - Hit Ctrl+C to EXIT")
        while True:
            with patch_stdout():
                mesgtext = await sess.prompt_async(
                    lambda: HTML("[" + genrwork.obtntime() + "] " +
                            "<b>" + genrwork.formusnm(clenoprs.username) + "</b>" + " > "),
                    bottom_toolbar=footelem,
                    validator=modutils.emtyfind(),
                    refresh_interval=0.5,
                    prompt_continuation=lambda width, line_number, is_soft_wrap: " " * width)
            if mesgtext.strip() == "/list":
                await clenoprs.fetch_list_of_users_connected_to_chatroom()
            elif mesgtext.strip() == "/stop":
                await clenoprs.initiate_chatroom_shutdown()
            elif mesgtext.strip() == "/save":
                clenoprs.save_connection_profile_to_file()
            elif mesgtext.strip() == "/wipe":
                click.clear()
                print_formatted_text("\n")
            elif mesgtext.strip() == "/help":
                clenoprs.show_help_and_support_topics()
            elif mesgtext.strip() == "/cont":
                clenoprs.print_contributors_info()
            elif mesgtext.strip() == "/ownr":
                await clenoprs.fetch_owner_name_of_the_chatroom()
            elif mesgtext.strip().split()[0] == "/kick":
                await clenoprs.remove_username_from_the_chatroom(mesgtext)
            elif mesgtext.strip().split()[0] == "/purr":
                await clenoprs.whisper_message_to_specific_username(mesgtext, cphrsuit)
            elif mesgtext.strip().split()[0] == "/anon":
                await clenoprs.anonymously_dispatch_to_specific_username(mesgtext, cphrsuit)
            else:
                await clenoprs.send_normal_message(mesgtext, cphrsuit)
    except EOFError:
        raise KeyboardInterrupt


async def hello(servaddr, username, chatroom, password):
    async with websockets.connect(servaddr) as websocket:
        try:
            clenoprs = sprtfunc.ClientOperations(username, chatroom, servaddr, password, websocket)
            presence = await clenoprs.check_username_presence()
            if presence["operands"] == "ROOMMADE" or presence["operands"] == "USERABST":
                cphrsuit = textdisp.FernetUtility(password.encode("utf8"))
                prod = asyncio.get_event_loop().create_task(
                    producer_handler(
                        cphrsuit, clenoprs
                    )
                )
                cons = asyncio.get_event_loop().create_task(
                    consumer_handler(
                        cphrsuit, websocket, str(username)
                    )
                )
                await clenoprs.identify_yourself()
                genrwork.decorate("SNCTRYZERO", "<green>Welcome to " + presence["chatroom"] + "</green>")
                await prod
                await cons
                asyncio.get_event_loop().run_forever()
            elif presence["operands"] == "USERPRST":
                genrwork.decorate("SNCTRYZERO", "<red>Username already exist in chatroom</red>")
                await websocket.close()
                raise KeyboardInterrupt
            elif presence["operands"] == "WRNGPASS":
                genrwork.decorate("SNCTRYZERO", "<red>Provided password does not match the chatroom password</red>")
                await websocket.close()
                raise KeyboardInterrupt
        except Exception as EXPT:
            if websocket.closed:
                genrwork.decorate("SNCTRYZERO", "<red>A connection to the server was lost</red>")
            raise KeyboardInterrupt


def read_connection_profile(connprof):
    click.clear()
    print_formatted_text("\n")
    genrwork.decorate("SNCTRYZERO", "<b><seagreen>Starting SNCTRYZERO Client v25122020 up...</seagreen></b>")
    try:
        with open(connprof) as fileobjc:
            conndata = json.load(fileobjc)
        genrwork.decorate(
            "SNCTRYZERO",
            "<seagreen>Attempted connection to '" + conndata["servaddr"] + "' at " + str(time.ctime()) + "</seagreen>"
        )
        valdunit = modutils.ValidityChecking()
        servaddr = valdunit.check_socket_validity(conndata["servaddr"])
        username = valdunit.check_username_validity(conndata["username"])
        chatroom = valdunit.check_chatroom_validity(conndata["chatroom"])
        password = valdunit.check_password_validity(conndata["password"])
        genrwork.decorate(
            "SNCTRYZERO",
            "<seagreen><b>Identity</b> " + chatroom + " > <b>Password</b> " + password + "</seagreen>"
        )
        genrwork.decorate(
            "SNCTRYZERO",
            "<seagreen>Share the chatroom identity, password and server address to invite members</seagreen>"
        )
        asyncio.get_event_loop().run_until_complete(hello(servaddr, username, chatroom, password))
    except FileNotFoundError as EXPT:
        genrwork.decorate("SNCTRYZERO", "<red>The provided connection profile could not be found</red>")
        raise KeyboardInterrupt
    except JSONDecodeError as EXPT:
        genrwork.decorate("SNCTRYZERO", "<red>The provided connection profile is invalid</red>")
        raise KeyboardInterrupt


@click.command()
@click.option("-f", "--connprof", "connprof", help="Enter the location of the connection profile file.", required=True)
@click.version_option(version="25122020", prog_name="SNCTRYZERO client")
def mainfunc(connprof):
    try:
        read_connection_profile(connprof)
    except OSError as EXPT:
        genrwork.decorate("SNCTRYZERO", "<red>A connection to the server could not be established</red>")
        raise KeyboardInterrupt
    except websockets.exceptions.ConnectionClosedError as EXPT:
        genrwork.decorate("SNCTRYZERO", "<red>A connection to the server was lost</red>")
        raise KeyboardInterrupt
    except KeyboardInterrupt as EXPT:
        genrwork.decorate("SNCTRYZERO", "<red>Leaving SNCTRYZERO...</red>")
        sys.exit()


if __name__ == "__main__":
    mainfunc()
