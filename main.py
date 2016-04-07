
"""main.py - Contains handlers for cronjobs. """

import webapp2
from google.appengine.api import mail, app_identity
from models import Game
from datetime import datetime, timedelta


class NotifyInactiveUsers(webapp2.RequestHandler):
    def get(self):
        """
        Sends notification for users which have active games, with no movement
        for over 12 hours.
        One notification per game.
        """
        app_id = app_identity.get_application_id()
        twelve_hours_ago = datetime.now() - timedelta(hours=12)
        # Get games with no change in the last 12 hours
        games = Game.query(Game.changed_at < twelve_hours_ago)
        for game in games:
            user = game.user.get()
            subject = "Please finish your game"
            board = "\n".join(game.board)
            body = """It's been a while since your last movement in this
            game of Peg Solitarie.
            Please finish the game.
            Remember that you can cancel or give up at any time.
            Current board:
                {}
            """.format(board)
            mail.send_mail('noreply@{}.appspotmail.com'.format(app_id),
                           user.email,
                           subject,
                           body)

app = webapp2.WSGIApplication([
    ('/crons/notify_inactive_users', NotifyInactiveUsers)
    ], debug=True)
