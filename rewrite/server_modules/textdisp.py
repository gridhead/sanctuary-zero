import os
import textwrap
import time

from prompt_toolkit import HTML, print_formatted_text


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
        print_formatted_text(HTML("[" + self.obtntime() + "] " + predname + " > " + HelperDisplay().wrap_conversational_text(predmesg)))

    def obtntime(self):
        timestmp = time.localtime()
        timehour = str(timestmp.tm_hour)
        timemint = str(timestmp.tm_min)
        timesecs = str(timestmp.tm_sec)
        if int(timehour) < 10:  timehour = "0" + timehour
        if int(timemint) < 10:  timemint = "0" + timemint
        if int(timesecs) < 10:  timesecs = "0" + timesecs
        return timehour + ":" + timemint + ":" + timesecs

    def formusnm(self, username):
        if len(username) < 10:
            return username + " " * (10 - len(username))
        elif len(username) > 10:
            return username[0:10]
        else:
            return username