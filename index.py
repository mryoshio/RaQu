import cgi, datetime, logging, os, ast
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext.db import Query

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

class MainPage(Base):
    def get(self):
        if users.get_current_user():
            c_user = self.get_current_quser()
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'logout'
            created_tasks = c_user.created_tasks.filter('deadline >', datetime.datetime.now())
            assigned_tasks = c_user.assigned_tasks.filter('deadline >', datetime.datetime.now())
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

class AddTask(Base):
    def post(self):
        if self.request.get("deadline") == None or self.request.get("deadline") == '':
            # default deadline = now + 1week
            deadline = datetime.datetime.today() + datetime.timedelta(7)
        else:
            # TODO modify to process input
            deadline = datetime.datetime.today() + datetime.timedelta(3)
        t = QTask(creator=self.get_current_quser(), assignee=self.get_current_quser(), title=self.request.get("title"), description=self.request.get("description"), deadline=deadline, done=False)
        t.put()
        self.redirect('/')

class UpdateStatus(Base):
    def post(self):
        key = self.request.get("key")
        sta = self.request.get("status")
        if key == None or key == '':
            pass
        else:
            qtask = QTask.get(key)
            qtask.done = ast.literal_eval(sta)
            qtask.put()

class DeleteTask(Base):
    def post(self):
        key = self.request.get("key");
        if key == None or key == '':
            pass
        else:
            qtask = QTask.get(key)
            logging.debug(qtask)
            qtask.delete()
        self.redirect('/')

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([('/', MainPage), ('/add', AddTask), ('/delete', DeleteTask), ('/update', UpdateStatus)], debug=True)
    run_wsgi_app(application)

