from datetime import datetime

from errbot import BotPlugin, botcmd
from errbot.utils import format_timedelta


class StalkerBot(BotPlugin):
    def callback_message(self, msg):
        message = msg.body
        if not message:
            return

        username = msg.frm.nick
        self.log.debug("Recording presence of %s", username)

        self[username] = {
            "time": datetime.now(),
            "msg": message,
        }

    @botcmd
    def seen(self, msg, args):
        """find out when someone last said something"""
        requester = msg.frm
        username = str(args)

        self.log.debug("%s looking for %s" % (requester, username))

        if username == requester:
            return "I can see you now"

        if username == "":
            return "Hmm... seen whom?"

        try:
            last_seen = self[username]["time"]
            last_msg = self[username]["msg"]
            return 'I last saw {0} {1} ago (on {2}) which said "{3}"'.format(
                username,
                format_timedelta(datetime.now() - last_seen),
                datetime.strftime(last_seen, "%A, %b %d at %H:%M"),
                last_msg,
            )
        except KeyError:
            return "I have no record of %s" % args
