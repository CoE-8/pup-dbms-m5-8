import webapp2
from google.appengine.ext import ndb
import jinja2
import os
import logging
import json


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)



class Student(ndb.Model):
    Year = ndb.StringProperty(indexed=True)
    Title = ndb.StringProperty(indexed=True)
    Abstract = ndb.StringProperty(indexed=True)
    Adviser = ndb.StringProperty(indexed=True)
    Section = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)



class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('createStudent.html')
        self.response.write(template.render())

    def post(self):
        student = Student()
        student.Year = self.request.get('Year')
        student.Title = self.request.get('Title')
        student.Abstract = self.request.get('Abstract')
        student.Adviser = self.request.get('Adviser')
        student.Section = self.request.get('Section')
        student.put()
  
class APIStudentHandler(webapp2.RequestHandler):

    def get(self):
        #get all student
        students = Student.query().order(-Student.date).fetch()
        student_list = []

        for student in students:
            student_list.append({
                    'id' : student.key.urlsafe(),
                    'Year' : student.Year,
                    'Title' : student.Title,
                    'Abstract' : student.Abstract,
                    'Adviser' : student.Adviser,
                    'Section' : student.Section
                })
        #return list to client
        response = {
        'result' : 'OK',
        'data' : student_list
        }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response))

    def post(self):
        student = Student()
        student.Year = self.request.get('Year')
        student.Title = self.request.get('Title')
        student.Abstract = self.request.get('Abstract')
        student.Adviser = self.request.get('Adviser')
        student.Section = self.request.get('Section')
        student.put()
        
        self.response.headers['Content-Type'] = 'application/json'
        response = {
            'result' : 'OK',
            'data': {
                'id' : student.key.urlsafe(),
                    'Year' : student.Year,
                    'Title' : student.Title,
                    'Abstract' : student.Abstract,
                    'Adviser' : student.Adviser,
                    'Section' : student.Section
            }
        }
        self.response.out.write(json.dumps(response))

app = webapp2.WSGIApplication([
    ('/api/student', APIStudentHandler),
    ('/', MainPage)   

], debug=True)