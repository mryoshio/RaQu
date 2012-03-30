import cgi, datetime, logging, os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext.db import Query
from google.appengine.ext import db
from google.appengine.api import mail

from model import QUser, QTask

class Base(webapp.RequestHandler):
    def get_quser(self, u):
        q = QUser.gql("WHERE g_user = :1 LIMIT 1", u)
        if q.count() < 1:
            u = QUser(g_user=users.get_current_user())
            u.put()
        else:
            u = q.get()
        return u

    def get_current_quser(self):
        return self.get_quser(users.get_current_user())

class Reminder(Base):
    def get(self):
        # TODO
        d = datetime.datetime.now() + datetime.timedelta(hours=24 + 9)
        list = db.GqlQuery("SELECT * FROM QTask where deadline < datetime(%d,%d,%d,%d,%d,%d)" %
                              (d.year, d.month, d.day, d.hour, d.minute, d.second))
        for u in list:
            if (u.done == False):
                mail.send_mail(sender="hoge@example.com",
                               to="fuga@example.com",
                               subject="Reminder: %s" % u.title,
                               body="""deadline is comming in next 24 hours.""")
                    
if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([('/reminder', Reminder)], debug=True)
    run_wsgi_app(application)
