"""
IRC utility class.
"""

import socket
import time

class IRC:
    """
    An IRC helper class specifically for working with the Undernet IRC
    network.
    """

    encoding = "utf-8"
    irc = socket.socket()

    def __init__(self):
        """
        Initialize the IRC object.
        """

        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, server, port, botnick, botpass="", botnickpass="", channel=""):
        """
        Connects to `server` and `port` using the nickname in `botnick`.
        """

        print(f"Connecting to: {server}:{port}")
        self.irc.connect((server, port))

        self.send(f"USER {botnick} {botnick} {botnick} :python")
        self.send(f"NICK {botnick}")

        if botnickpass and botpass:
            self.send(f"NICKSERV IDENTIFY {botnickpass} {botpass}")

        time.sleep(5)

        self.ping_pong_auth()

        time.sleep(5)

        self.login()

        time.sleep(5)

        if channel:
            self.join(channel)

    def join(self, channel):
        """
        Joins `channel`.
        """

        self.send(f"JOIN {channel}")

    def login(self):
        """
        Login to the Undernet X bot.
        """

        self.msg("x@channels.undernet.org", "LOGIN hostname and password goes here")

    def msg(self, channel_or_nick, text):
        """
        Sends the `text` to `channel_or_nick` as an IRC `PRIVMSG` command.
        """

        self.send(f"PRIVMSG {channel_or_nick} :{text}")

    def ping_pong_auth(self):
        """
        Handles the initial PING-PONG handshake from the server.
        """

        lines = self.receive()
        code = ""

        for line in lines:
            if line.find('PING') != -1:
                code = line.split(':')[1]
                break

        print(f"Sending PONG {code}")
        self.send(f"PONG {code}")

    def receive(self):
        """
        Receives data from the server and returns it as an array of lines.
        """

        time.sleep(1)

        try:
            response = self.irc.recv(2040).decode(self.encoding)
            lines = response.split("\r\n")
            return lines
        except Exception as e:
            print(e)
            pass

    def send(self, message):
        """
        Sends `message` directly to the server.
        """

        self.irc.send(bytes(message + "\n", self.encoding))
