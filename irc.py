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

    debug = False
    encoding = "utf-8"
    irc = socket.socket()

    def __init__(self, debug=False):
        """
        Initialize the IRC object.
        """

        self.debug = debug
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, server, port, nickname, userpassword="", channel=""):
        """
        Connects to `server` and `port` using the nickname in `nickname`.
        """

        print(f"Connecting to: {server}:{port}")
        self.irc.connect((server, port))


        self.send(f"USER {nickname.lower()} {nickname.lower()} {nickname.lower()} :python")
        self.send(f"NICK {nickname}")

        time.sleep(5)

        self.ping_pong_auth()

        time.sleep(5)

        if nickname and userpassword:
            self.login(nickname, userpassword)
            time.sleep(5)

        if channel:
            self.join(channel)

    def join(self, channel):
        """
        Joins `channel`.
        """

        self.send(f"JOIN {channel}")

    def login(self, username, password):
        """
        Login to the Undernet X bot.
        """

        self.msg("x@channels.undernet.org", f"LOGIN {username} {password}")

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

        self.pong(code)

    def ping_response(self):
        """
        Backwards compatible method for `pong()`.
        """

        self.pong()

    def pong(self, code=""):
        """
        Responds to a server `PING` message with the appropriate `PONG` message response.
        """

        try:
            print(f"Sending PONG {code}")
            self.send(f"PONG {code}")
        except Exception as e:
            print(e)

    def receive(self):
        """
        Receives data from the server and returns it as an array of lines.
        """

        time.sleep(1)

        try:
            response = self.irc.recv(2040).decode(self.encoding)
            lines = response.split("\r\n")

            if self.debug:
                for line in lines:
                    print(line)

            return lines
        except Exception as e:
            print(e)
            pass

    def send(self, message):
        """
        Sends `message` directly to the server.
        """

        if self.debug:
            print(message)

        self.irc.send(bytes(message + "\n", self.encoding))

class Message:
    """
    Represents a message received from the IRC server.
    """

    def __init__(self, message):
        self.text = message

    def __str__(self) -> str:
        return self.text
