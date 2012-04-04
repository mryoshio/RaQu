import datetime
import unittest

from model import QUser, QTask
from reminder import Reminder

from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import testbed

class ReminderTestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        #self.testbed.init_taskqueue_stub()
        self.testbed.init_mail_stub()
        self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)

    def tearDown(self):
        self.testbed.deactivate()

    def testReminder_001(self):
        deadline = datetime.datetime.today() + datetime.timedelta(2)
        u = QUser(g_user=users.User(email='test@example.com'))
        u.put()
        title = 'chips and beer'
        t = QTask(creator=u, assignee=u, title=title, description='', deadline=deadline, done=False)
        t.put()
        r = Reminder()
        r.get()
        messages = self.mail_stub.get_sent_messages(to='test@example.com')
        self.assertEqual(0, len(messages))

    def testReminder_002(self):
        deadline = datetime.datetime.today() + datetime.timedelta(hours=6)
        u = QUser(g_user=users.User(email='test@example.com'))
        u.put()
        title = 'chips and beer'
        t = QTask(creator=u, assignee=u, title=title, description='', deadline=deadline, done=True)
        t.put()
        r = Reminder()
        r.get()
        messages = self.mail_stub.get_sent_messages(to='test@example.com')
        self.assertEqual(0, len(messages))

        
    def testReminder_003(self):
        deadline = datetime.datetime.today() + datetime.timedelta(hours=6)
        u = QUser(g_user=users.User(email='test@example.com'))
        u.put()
        title = 'chips and beer'
        t = QTask(creator=u, assignee=u, title=title, description='', deadline=deadline, done=False)
        t.put()
        r = Reminder()
        r.get()
        messages = self.mail_stub.get_sent_messages(to='test@example.com')
        self.assertEqual(1, len(messages))
        self.assertEqual('test@example.com', messages[0].to)
        self.assertEqual('Reminder: ' + title, messages[0].subject)
