from google.appengine.ext import db

class QUser(db.Model):
    g_user = db.UserProperty() # google
    t_name = db.StringProperty() # twitter

class QTask(db.Model):
    creator = db.ReferenceProperty(reference_class=QUser, collection_name="created_tasks")
    assignee = db.ReferenceProperty(reference_class=QUser, collection_name="assigned_tasks")
    title = db.StringProperty(multiline=False)
    description = db.StringProperty(multiline=True)
    deadline = db.DateTimeProperty()
    done = db.BooleanProperty()

