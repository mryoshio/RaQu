import datetime, os, sys, unittest2

from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore_file_stub
from google.appengine.api import user_service_stub
from google.appengine.api import users
from google.appengine.ext import testbed
from model import QUser, QTask

APP_ID="raqu_test"
AUTH_DOMAIN="gmail.com"

class TestModelBase(unittest2.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
#        self.testbed.setup_env(app_id=APP_ID)
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()
#        os.environ['APPLICATION_ID'] = APP_ID
#        os.environ['AUTH_DOMAIN'] = AUTH_DOMAIN

    def tearDown(self):
        self.testbed.deactivate()


class TestQUser(TestModelBase):
    def testInsertQUser(self):
        u = users.User("mryoshio@gmail.com")
        user = QUser(g_user=u, t_name="mryoshio")
        user.put()
        hit = user.gql("WHERE t_name = :1", "mryoshio")
        self.assertEqual(u"mryoshio@gmail.com", hit.get().g_user.email())
        self.assertEqual(u"mryoshio", hit.get().t_name)


class TestQTask(TestModelBase):
    def testInsertQTask(self):
        u = QUser(g_user=users.User("mryoshio@gmail.com"), t_name="mryoshio")
        u.put()
        task = QTask(creator=u, assignee=u, title="test_title", description="test_description", deadline=datetime.datetime.today() + datetime.timedelta(3), done=False)
        task.put()
        hit = task.gql("WHERE assignee = :1", u)
        self.assertEqual(u"mryoshio@gmail.com", hit.get().creator.g_user.email())
        self.assertEqual(u"mryoshio@gmail.com", hit.get().assignee.g_user.email())
        self.assertEqual(u"test_title", hit.get().title)
        self.assertEqual(u"test_description", hit.get().description)
        self.assertFalse(hit.get().done)


