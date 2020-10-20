import locale
import re
import platform
import os
import sys
import termcolor
import time

isNotWindows = platform.system() != "Windows"

if isNotWindows:
    from dialog import Dialog
    os.system("clear")
else:
    os.system("cls")


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Ui:
    translation = {
        'enterUrl': "Please specify target address (http://example.com)",
        'enterPort': 'Please specify target server port (80)',
        'exampleWebsite': 'https://example.com',
        'checkUrl': "Please check address and try again",
        'checkPort': 'Please check port and try again',
        'bye': 'Bye!',
        'introText': """
Hello,
You can use this script for making a DDoS (or Strongly, DrDoS) attak on a server.

\"we're irresponsible about this script\"
"""
    }

    def __init__(self):
        self.file_name = resource_path("License.txt")
        locale.setlocale(locale.LC_ALL, '')
        if isNotWindows:
            self.d = Dialog(dialog="dialog")
            self.d.set_background_title("DrDoSer Script")
        self.siteUrl = self.translation['exampleWebsite']
        self.sitePort = 80
        self.intro()

    def check_width(self, text=""):
        if not text:
            with open(self.file_name, "r") as base:
                read_lines = base.readlines()
                len_list = []
                for line in read_lines:
                    len_list.append(len(line))
                len_list.sort()
                width = len_list[-1]
            return width
        else:
            return len(text)

    def intro(self):
        if isNotWindows:
            dialog = self.d.msgbox(text=self.translation['introText'])
        else:
            print(termcolor.colored(self.translation['introText'], color="green"))

        self.agreement()

    def agreement(self):
        if isNotWindows:
            dialog = self.d.textbox(self.file_name, height=None, width=self.check_width())
        else:
            print(termcolor.colored("Under GNU GENERAL PUBLIC LICENSE v2", color="red"))
            i = input("enter \"LICENSE\" for reading license" + ":\t")
            if i == "LICENSE":
                with open(resource_path("License.txt")) as License:
                    print(termcolor.colored(License.read(), color="yellow"))
                    License.close()

        self.inputUrl()

    def inputUrl(self):
        dialog = [""]
        if isNotWindows:
            dialog = self.d.inputbox(init=self.translation["exampleWebsite"], text=self.translation['enterUrl'])
            text = dialog[1]
        else:
            text = input(self.translation['enterUrl'] + ":\t")

        if re.findall(
                r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+"
                r"|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))",
                str(text)):
            self.siteUrl = text
            self.inputPort()
        elif dialog[0] == "cancel":
            self.error(self.translation['bye'])
        else:
            self.error(self.translation['checkUrl'])

    def inputPort(self):
        dialog = [""]
        if isNotWindows:
            dialog = self.d.inputbox(init="80", text=self.translation['enterPort'])
            text = dialog[1]
        else:
            text = input(self.translation['enterPort'] + ":\t")

        if re.findall(r"^[-+]?[0-9]+$", str(text)):
            self.sitePort = text
            self.DDoS()
        elif dialog[0] == "cancel":
            self.error(self.translation['bye'])
        else:
            self.error(self.translation['checkPort'])

    def error(self, text):
        if isNotWindows:
            dialog = self.d.msgbox(text, width=self.check_width(text) + 10)
            print(termcolor.colored(text, color="red"))
        if dialog:
            self.__exit__()

    def DDoS(self):
        self.goOut()
        os.environ['port'] = str(self.sitePort)
        os.environ['url'] = self.siteUrl
        print(termcolor.colored("starting DDoS...", color='green'))
        time.sleep(2)
        import DDoS

    def goOut(self):
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    def __exit__(self):
        self.goOut()
        sys.exit(1)


if __name__ == "__main__":
    raise Exception('RunError\n' + termcolor.colored('Please run main.py!', 'red'))
