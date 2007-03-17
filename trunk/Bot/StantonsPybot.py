#libs
import irclib
import ircbot
from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr
#main
class Stanpybot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        
    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "")
        
    def on_welcome(self, c, e):
        c.join(self.channel)
        
    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments()[0])
    
    def on_pubmsg(self, c, e):
        a = e.arguments()[0].split(":", 1)
        if len(a) > 1 and irc_lower(a[0]) == irc_lower(self.connection.get_nickname()):
            self.do_command(e, a[1].strip())
        return
    
    def on_dccmsg(self, c, e):
        c.privmsg("you said: " + e.arguments()[0])
        
    def on_dccchat(self, c, e):
        if len(e.arguments()) != 2:
            return
        args = e.arguments()[1].split()
        if len(args) ==4:
            try:
                adress = ip_numstr_to_quad(args[2])
                port = int(args[3])
            except ValueError:
                return
            self.doc_connect(adress, port)
    def do_command(self, e, cmd):
        nick = nm_to_n(e.source())
        c = self.connection
        if cmd == "disconnect992233":
            self.disconnect()
        elif cmd == "test3":
            self.ctcp(msg, "TBG testing script")
        elif cmd == "die992233":
            self.die()
        elif cmd == "help":
            c.notice(nick, "commands: stats. DCC[not working].")
        elif cmd == "test2":
            (c,"this is a automaticed bot i am runing a test script please standby")
        elif cmd == "stats":
            for chname, chobj in self.channels.items():
                c.notice(nick, "---channel statistics ---")
                c.notice(nick, "channel: " + chname)
                users = chobj.users()
                users.sort()
                c.notice(nick, "Users: " + ", ".join(users))
                opers = chobj.opers()
                opers.sort()
                c.notice(nick, "Opers: " + ", ".join(opers))
                voiced = chobj.voiced()
                voiced.sort()
                c.notice(nick, "Voiced: " + ", ".join(voiced))
        elif cmd == "dcc":
                dcc = self.dcc_listen()
                c.ctcp("DCC", nick, "CHAT chat %s %d" % (
                    ip_quad_to_numstr(dcc.localadress),
                    dcc.localport))
        else:
                c.notice(nick, "Command Unknown: " + cmd)

def main():
    import sys
    if len(sys.argv) != 4:
        print "Usage: Stanpybot <server[:port]> <channel> <nickname>"
        print "                  server:port channel nickname in command line"
        print "-----------------------------------------------------------------"
        print "--------------------Please follow instructions!------------------"
        print "if you dont understand them then heres an more indepth"
        print "go to command line type python or what ever you use to run python"
        print "then stantonspybot.py server:port channel nickname"
        print "should look like this"
        print "python stantonspybot.py irc.adress.com:6667 #channame mynick"
        print "remmber in irc type /msg nick cmd eg: /msg nick help"
        print "---------------------------------------------------------------- "
        print "thank you for useing Stantons Python Bot! ver 0.1"
        print "please note this is ALPHA!"
        print "------------END of Program run program as said above-------------"
        sys.exit(1)
        
    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print "Error: Erroneous port."
            sys.exit(1)
    else:
        port = 6667
    channel = sys.argv[2]
    nickname = sys.argv[3]
    
    bot = Stanpybot(channel, nickname, server, port)
    bot.start()
if __name__ == "__main__":
    main()