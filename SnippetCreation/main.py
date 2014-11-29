import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.db import polymodel

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

class Snippet(polymodel.PolyModel):
    author = ndb.UserProperty()
	snippet_title = StringProperty(repeated=True)
    snippet_tags = StringProperty(repeated=True)

def Snippet_Quiz_Question_Key(snippet_name='Snippet_Quiz_Question'):
    return ndb.Key('Snippet_Quiz_Question', snippet_name)
	
class Snippet_Quiz_Question(Snippet):
	question = ndb.StringProperty()
	answer = ndb.StringProperty()

def Snippet_Event_Key(snippet_name='Snippet_Event'):
    return ndb.Key('Snippet_Event', snippet_name)

class Snippet_Event(Snippet):
	event_date = ndb.DateProperty()
	event_time = ndb.TimeProperty()
	event_content = ndb.StringProperty()

class Main(webapp2.RequestHandler):
    def get(self):
        
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class Snippet_Insert(webapp2.RequestHandler):
    def post(self):
        		
		#set correct properties depending on kind of entry
		
		#if form type == q_question then make new that snippet
		#else if form type == event_snippet then make new event_snippet
		 
		#if self.request.get('value') == 'q_question'
		
		snippet_name = self.request.get('snippet_name','Snippet_Quiz_Question')
			
		snippet_Qstion = Snippet_Quiz_Question(parent=Snippet_Quiz_Question_Key(snippet_name))
		
		if users.get_current_user():
			snippet_Qstion.author = users.get_current_user()
			
		snippet_Qstion.snippet_title = self.request.get('snippet_title')
		snippet_Qstion.snippet_tags = self.request.get('snippet_tags')
		snippet_Qstion.question = self.request.get('question')
		snippet_Qstion.answer = self.request.get('answer')
				
		snippet_Qstion.put()
		
		
		query_params = {'snippet_name': snippet_name}
        self.redirect('/?' + urllib.urlencode(query_params))
		
		#else if self.request.get('value') == 'event_snippet'
		#	snippet_Event = Snippet_Event()
			
		#	if users.get_current_user():
		#		snippet_Event.author = users.get_current_user()
			
		#snippet_Event.snippet_title = self.request.get('snippet_title')
		#snippet_Event.snippet_tags = self.request.get_all('snippet_tags')
		#snippet_Event.event_date = self.request.get('event_date')
		#snippet_Event.event_time = self.request.get('event_time')
		#snippet_Event.event_content = self.request.get('event_content')
			
	    #snippet_Event.put()

app = webapp2.WSGIApplication([('/', Main),('/sign', Snippet),], debug=True)
