from errbot.utils import format_timedelta
from datetime import datetime
import logging

# Backward compatibility
from errbot.version import VERSION
from errbot.utils import version2array
if version2array(VERSION) >= [1, 6, 0]:
    from errbot import botcmd, BotPlugin
else:
    from errbot.botplugin import BotPlugin
    from errbot.jabberbot import botcmd


class StalkerBot(BotPlugin):
    def callback_message(self, mess):
        message = mess.body
        username = str(mess.nick)

        if not message or username == 'None':
            return

        logging.info('Saving entry for {0}'.format(username))

        self.shelf[username] = {
            'time': datetime.now(),
            'msg': message,
        }
        self.shelf.sync()

    @botcmd
    def seen(self, mess, args):
        """ find out when someone last said something """
        requester = str(mess.nick)
        username = str(args)

        logging.info('{0} looking for {1}'.format(requester, username))

        if username == '':
            return 'Hmm... seen whom?'

        if requester == username:
            return 'I can see you now'

        try:
            last_seen = self.shelf[username]['time']
            last_msg = self.shelf[username]['msg']
            return 'I last saw {0} {1} ago (on {2}) which said "{3}"'.format(
                args,
                format_timedelta(datetime.now() - last_seen),
                datetime.strftime(last_seen, '%A, %b %d at %H:%M'),
                last_msg
            )
        except KeyError:
            return 'I have no record of %s' % args
