import secrets, socket, time
from prompt_toolkit import print_formatted_text, HTML
from cryptography.fernet import Fernet
from prompt_toolkit.validation import Validator, ValidationError


class emtyfind(Validator):
    def validate(self, document):
        if document.text.strip() == "":
            raise ValidationError(message="You cannot send an empty message ")


class fernetst():
    def __init__(self, pswd):
        self.suit = Fernet(pswd)

    def encrjson(self, data):
        return self.suit.encrypt(data.encode("utf8")).decode("utf8")

    def decrjson(self, data):
        return self.suit.decrypt(data.encode("utf8")).decode("utf8")


def obtntime():
    timestmp = time.localtime()
    timehour = str(timestmp.tm_hour)
    timemint = str(timestmp.tm_min)
    timesecs = str(timestmp.tm_sec)
    if int(timehour) < 10:  timehour = "0" + timehour
    if int(timemint) < 10:  timemint = "0" + timemint
    if int(timesecs) < 10:  timesecs = "0" + timesecs
    return timehour + ":" + timemint + ":" + timesecs


def randgene():
    numb = 8
    randstrg = "".join(secrets.choice("ABCDEF" + "0123456789") for i in range(numb))
    return randstrg


def chekroom(strg):
    if len(strg) != 8:
        return False
    else:
        try:
            geee = int(strg, 16)
            return strg.isupper()
        except ValueError:
            return False


def chekpass(pswd):
    try:
        suit = Fernet(pswd)
        return True
    except:
        return False


def formusnm(username):
    if len(username) < 10:
        return username + " " * (10 - len(username))
    elif len(username) > 10:
        return username[0:10]
    else:
        return username


def check_socket(servaddr):
    addr = [x.strip().strip("/") for x in servaddr.split(":")]
    # ['ws',ip, port_no]
    if addr[0] == "ws":
        try:
            addr[2]= int(addr[2])
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                if sock.connect_ex((addr[1], addr[2])) == 0:
                    return True
                else:
                    print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <red>Server was not found at '" + servaddr + "</red>"))
                    return False
        except ValueError:
            print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <red>Invalid port number > '"+addr[2]+"'</red>"))
            return False
        except Exception:
            return False
    print_formatted_text(HTML("[" + obtntime() + "] " + "SNCTRYZERO > <red>The URI entered is not WebSockets-protocol compliant</red>"))
    return False
