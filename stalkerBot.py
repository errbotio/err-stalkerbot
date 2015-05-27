from errbot.utils import format_timedelta
from datetime import datetime
from errbot import botcmd, BotPlugin
import logging
log = logging.getLogger(__name__)

class StalkerBot(BotPlugin):
    def callback_message(self, mess):
        message = mess.getBody()
        if not message:
            return

        username = mess.frm.node
        log.debug("Recording presence of %s", username)
        self[username] = datetime.now()

    @botcmd
    def seen(self, mess, args):
        """ find out when someone last said something """
        username = mess.frm.node
        if username == args:
            return 'I can see you now'
        try:
            last_seen = self[str(args)]
            return 'I last saw %s %s ago (on %s)' % (args, format_timedelta(datetime.now() - last_seen), datetime.strftime(last_seen, '%A, %b %d at %H:%M'))
        except KeyError:
            return 'I have no record of %s' % args

