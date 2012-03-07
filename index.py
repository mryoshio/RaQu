import cgi,logging, os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

from datetime import datetime
from model import QUser, QTask

class MainPage(webapp.RequestHandler):

    def get(self):
        c_user = ''
        assigned_tasks = []
        created_tasks = []
        if users.get_current_user():
            q = QUser.gql("WHERE g_user = :1 LIMIT 1", users.get_current_user())
            if q.count() < 1:
                c_user = QUser(g_user=users.get_current_user())
                c_user.put()
            else:
                c_user = q.get()
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'logout'
            created_tasks = c_user.created_tasks.filter('deadline > ', datetime.now())
            assigned_tasks = c_user.assigned_tasks.filter('deadline > ', datetime.now())
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'login'

        template_values = {
            'quser': c_user,
            'assigned': assigned_tasks,
            'created': created_tasks,
            'url': url,
            'url_linktext': url_linktext,
            }

        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, template_values))

def main():
    application = webapp.WSGIApplication([('/', MainPage)], debug=True)
    run_wsgi_app(application)
    logging.getLogger().setLevel(logging.DEBUG)

if __name__ == "__main__":
    main()
