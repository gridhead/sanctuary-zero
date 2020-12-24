import socket

from cryptography.fernet import Fernet
from prompt_toolkit.validation import ValidationError, Validator

from . import textdisp


class emtyfind(Validator):
    def validate(self, document):
        if document.text.strip() == "":
            raise ValidationError(message="You cannot send an empty message ")


gnrlwork = textdisp.GeneralWorking()


class ValidityChecking():
    def check_socket_validity(self, servaddr):
        addr = [x.strip().strip("/") for x in servaddr.split(":")]
        # ['ws',ip, port_no]
        if addr[0] == "ws":
            try:
                addr[2]= int(addr[2])
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(1)
                    if sock.connect_ex((addr[1], addr[2])) == 0:
                        return servaddr
                    else:
                        gnrlwork.decorate("SNCTRYZERO", "<red>Server was not found at '" + servaddr + "</red>")
                        raise KeyboardInterrupt
            except ValueError:
                gnrlwork.decorate("SNCTRYZERO", "<red>Invalid port number > '" + addr[2] + "'</red>")
                raise KeyboardInterrupt
            except Exception:
                gnrlwork.decorate("SNCTRYZERO", "<red>Attempted connection failed due to invalid provided URI</red>")
                raise KeyboardInterrupt
        gnrlwork.decorate("SNCTRYZERO", "<red>The URI entered is not WebSockets-protocol compliant</red>")
        raise KeyboardInterrupt

    def check_chatroom_validity(self, roomload):
        chatroom = roomload
        if chatroom == "":
            gnrlwork.decorate("SNCTRYZERO", "<green>A new chatroom was generated</green>")
            chatroom = gnrlwork.randgene()
        else:
            if gnrlwork.chekroom(chatroom) is True:
                gnrlwork.decorate("SNCTRYZERO", "<green>A valid chatroom identity was entered</green>")
            elif not chatroom.isupper():
                chatroom = chatroom.upper()
                if gnrlwork.chekroom(chatroom) is True:
                    gnrlwork.decorate("SNCTRYZERO", "<green>A valid chatroom identity was entered</green>")
                else:
                    gnrlwork.decorate("SNCTRYZERO", "<red>An invalid chatroom identity was entered</red>")
                    raise KeyboardInterrupt
            else:
                gnrlwork.decorate("SNCTRYZERO", "<red>An invalid chatroom identity was entered</red>")
                raise KeyboardInterrupt
        return chatroom

    def check_password_validity(self, passload):
        password = passload
        if password == "":
            gnrlwork.decorate("SNCTRYZERO", "<green>A new password was generated</green>")
            password = Fernet.generate_key().decode("utf8")
        else:
            if gnrlwork.chekpass(password) is True:
                gnrlwork.decorate("SNCTRYZERO", "<green>A valid chatroom password was entered</green>")
            else:
                gnrlwork.decorate("SNCTRYZERO", "<red>An invalid chatroom password was entered</red>")
                raise KeyboardInterrupt
        return password

    def check_username_validity(self, username):
        if username.strip() != "" and " " not in username and len(username) <= 15:
            return username
        else:
            gnrlwork.decorate("SNCTRYZERO", "<red>An invalid username was entered</red>")
            raise KeyboardInterrupt
