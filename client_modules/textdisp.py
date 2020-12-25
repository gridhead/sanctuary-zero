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

import os
import secrets
import textwrap
import time

from click import style
from cryptography.fernet import Fernet
from prompt_toolkit import HTML, print_formatted_text


class FernetUtility():
    def __init__(self, pswd):
        self.suit = Fernet(pswd)

    def encrtext(self, data):
        return self.suit.encrypt(data.encode("utf8")).decode("utf8")

    def decrtext(self, data):
        return self.suit.decrypt(data.encode("utf8")).decode("utf8")


class HelperDisplay:
    """
    Utility Helper for Displaying Data
    Current methods:
        1. wrap_text
        2. wrap_conversational_text
        3. _get_width -> internal use
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


class GeneralWorking():
    def decorate(self, predname, predmesg):
        print_formatted_text(HTML("[" + self.obtntime() + "] " + "<b>" + self.formusnm(predname) + "</b>" + " > " + HelperDisplay().wrap_conversational_text(predmesg)))

    def simple_decorate(self, predname, predmesg):
        print("[" + self.obtntime() + "] " + style(self.formusnm(predname), bold=True) + " > " + HelperDisplay().wrap_conversational_text(predmesg))

    def obtntime(self):
        timestmp = time.localtime()
        timehour = str(timestmp.tm_hour)
        timemint = str(timestmp.tm_min)
        timesecs = str(timestmp.tm_sec)
        if int(timehour) < 10:  timehour = "0" + timehour
        if int(timemint) < 10:  timemint = "0" + timemint
        if int(timesecs) < 10:  timesecs = "0" + timesecs
        return timehour + ":" + timemint + ":" + timesecs

    def randgene(self):
        numb = 8
        randstrg = "".join(secrets.choice("ABCDEF" + "0123456789") for i in range(numb))
        return randstrg

    def chekroom(self, strg):
        if len(strg) != 8:
            return False
        else:
            try:
                geee = int(strg, 16)
                return strg.isupper()
            except ValueError:
                return False

    def chekpass(self, pswd):
        try:
            suit = Fernet(pswd)
            return True
        except:
            return False

    def formusnm(self, username):
        if len(username) < 10:
            return username + " " * (10 - len(username))
        elif len(username) > 10:
            return username[0:10]
        else:
            return username
