from errbot.utils import get_jid_from_message,format_timedelta
from datetime import datetime

# Backward compatibility
from errbot.version import VERSION
from errbot.utils import version2array
if version2array(VERSION) >= [1,6,0]:
    from errbot import botcmd, BotPlugin
else:
    from errbot.botplugin import BotPlugin
    from errbot.jabberbot import botcmd


class StalkerBot(BotPlugin):
    def callback_message(self, conn, mess):
        message = mess.getBody()
        if not message:
            return

        username = str(get_jid_from_message(mess)).encode('ascii', 'replace')
        self.shelf[username] = datetime.now()
        self.shelf.sync()


    @botcmd
    def seen(self, mess, args):
        """ find out when someone last said something """
        username = get_jid_from_message(mess)
        if username == args:
            return 'I can see you now'
        try:
            last_seen = self.shelf[str(args)]
            return 'I last saw %s %s ago (on %s)' % (args, format_timedelta(datetime.now() - last_seen), datetime.strftime(last_seen, '%A, %b %d at %H:%M'))
        except KeyError:
            return 'I have no record of %s' % args

