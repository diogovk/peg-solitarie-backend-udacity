
"""main.py - Contains handlers for cronjobs. """

import webapp2
from google.appengine.api import mail, app_identity
from models import Game
from datetime import datetime, timedelta


REMINDER_MESSAGE_PLAIN = """
It's been a while since your last movement in this game of Peg Solitarie.
Please finish your game.
Remember that you can cancel or give up at any time.
Current board:
{}
"""
REMINDER_MESSAGE_HTML = "<pre>{}</pre>".format(REMINDER_MESSAGE_PLAIN)

BOARD_HTML_TEMPLATE = """
<pre style="font-family: 'Courier New', Courier, monospace;">{}</pre>
"""

SENDER='noreply@{}.appspotmail.com'.format(app_identity.get_application_id())
REMINDER_SUBJECT="Please finish your game"

class NotifyInactiveUsers(webapp2.RequestHandler):
    def get(self):
        """
        Sends notification for users which have active games, with no movement
        for over 12 hours.
        One notification per game.
        """
        twelve_hours_ago = datetime.now() - timedelta(hours=12)
        # Get games with no change in the last 12 hours
        games = Game.query(Game.changed_at < twelve_hours_ago)
        for game in games:
            user = game.user.get()
            board = "\n".join(game.board)
            board_html = BOARD_HTML_TEMPLATE.format(board)
            message = mail.EmailMessage(sender=SENDER,
                                        subject=REMINDER_SUBJECT)
            message.to = user.email
            message.body = REMINDER_MESSAGE_PLAIN.format(board)
            message.html = REMINDER_MESSAGE_HTML.format(board_html)
            message.send()


app = webapp2.WSGIApplication([
    ('/crons/notify_inactive_users', NotifyInactiveUsers)
    ], debug=True)
