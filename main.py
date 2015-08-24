import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import urllib
import logging
import json


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)


class Thesis(ndb.Model):
    username = ndb.StringProperty(indexed=False)
    userId = ndb.StringProperty(indexed=False)
    Year = ndb.StringProperty(indexed=True)
    Title = ndb.StringProperty(indexed=True)
    Abstract = ndb.StringProperty(indexed=True)
    Adviser = ndb.StringProperty(indexed=True)
    Section = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        # template = JINJA_ENVIRONMENT.get_template('thesisForm.html')
        # self.response.write(template.render())

        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'

        template_data = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext
        }
        if user:
            template = JINJA_ENVIRONMENT.get_template('thesisForm.html')
            self.response.write(template.render(template_data))
        else:
            self.redirect(users.create_login_url(self.request.uri))

    # def post(self):
    #     thesis = Thesis()
    #     thesis.Year = self.request.get('Year')
    #     thesis.Title = self.request.get('Title')
    #     thesis.Abstract = self.request.get('Abstract')
    #     thesis.Adviser = self.request.get('Adviser')
    #     thesis.Section = self.request.get('Section')
    #     thesis.put()

class ThesisDelete(webapp2.RequestHandler):
    def get(self, thesisId):
        d = Thesis.get_by_id(int(thesisId))
        d.key.delete()
        self.redirect('/')

class ThesisEdit(webapp2.RequestHandler):
    def get(self,thesisId):
        s = Thesis.get_by_id(int(thesisId))
        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        template_data = {
            'thesis': s,
            'user': user,
            'url': url,
            'url_linktext': url_linktext
        }
        template = JINJA_ENVIRONMENT.get_template('editThesis.html')
        self.response.write(template.render(template_data))
    
    def post(self,thesisId):
        thesis = Thesis.get_by_id(int(thesisId))      
        # user = users.get_current_user()
        thesis.Year = self.request.get('Year')
        thesis.Title = self.request.get('Title')
        thesis.Abstract = self.request.get('Abstract')
        thesis.Adviser = self.request.get('Adviser')
        thesis.Section = self.request.get('Section')
        # thesis.username = user.nickname()
        thesis.put()
        self.redirect('/')
  
class APIThesisHandler(webapp2.RequestHandler):

    def get(self):
        #get all student
        thesis = Thesis.query().order(-Thesis.date).fetch()
        thesis_list = []

        for th in thesis:
            thesis_list.append({
                    'id' : th.key.id(),
                    'Year' : th.Year,
                    'Title' : th.Title,
                    'Abstract' : th.Abstract,
                    'Adviser' : th.Adviser,
                    'Section' : th.Section,
                    'username' : th.username
                })
        #return list to client
        response = {
            'result' : 'OK',
            'data' : thesis_list
        }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response))

    def post(self):
        user = users.get_current_user()
        th = Thesis()
        th.Year = self.request.get('Year')
        th.Title = self.request.get('Title')
        th.Abstract = self.request.get('Abstract')
        th.Adviser = self.request.get('Adviser')
        th.Section = self.request.get('Section')
        th.username = user.nickname()
        th.userId = user.user_id()
        th.put()
        
        self.response.headers['Content-Type'] = 'application/json'
        response = {
            'result' : 'OK',
            'data': {
                'id' : th.key.id(),
                'Year' : th.Year,
                'Title' : th.Title,
                'Abstract' : th.Abstract,
                'Adviser' : th.Adviser,
                'Section' : th.Section,
                'username' : th.username
            }
        }
        self.response.out.write(json.dumps(response))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/api/thesis', APIThesisHandler),
    ('/thesis/delete/(.*)', ThesisDelete),
    ('/thesis/edit/(.*)', ThesisEdit)
], debug=True)