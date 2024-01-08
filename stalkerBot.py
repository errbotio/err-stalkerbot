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
            time_ago_relative = format_timedelta(datetime.now() - last_seen)
            time_ago = datetime.strftime(last_seen, "%A, %b %d at %H:%M")
            return f"I last saw '{username}' {time_ago_relative} ago (on {time_ago}) which said '{last_msg}'"
        except KeyError:
            return f"I have no record of {args}."
