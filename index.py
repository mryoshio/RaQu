import cgi, logging, os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

from datetime import datetime
from model import QUser, QTask

class Base(webapp.RequestHandler):
    def get_current_quser(self):
        q = QUser.gql("WHERE g_user = :1 LIMIT 1", users.get_current_user())
        if q.count() < 1:
            u = QUser(g_user=users.get_current_user())
            u.put()
        else:
            u = q.get()
        return u

class MainPage(Base):
    def get(self):
        logging.debug("MainPage#get")
        if users.get_current_user():
            c_user = self.get_current_quser()
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'logout'
            created_tasks = c_user.created_tasks.filter('deadline >', datetime.now())
            assigned_tasks = c_user.assigned_tasks.filter('deadline >', datetime.now())
            template_values = {
                'quser': c_user,
                'assigned': assigned_tasks,
                'created': created_tasks,
                'url': url,
                'url_linktext': url_linktext,
                }
            path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
            self.response.out.write(template.render(path, template_values))
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'login'
            template_values = {
                'url': url,
                'url_linktext': url_linktext,
                }
            path = os.path.join(os.path.dirname(__file__), 'templates/login.html')
            self.response.out.write(template.render(path, template_values))

class AddPage(Base):
    def get(self):
        logging.debug("AddPage#get")
        template_values = {
            'quser': self.get_current_quser()
            }
        path = os.path.join(os.path.dirname(__file__), 'templates/add_task.html')
        self.response.out.write(template.render(path, template_values))

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([('/', MainPage), ('/go_add', AddPage)], debug=True)
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
