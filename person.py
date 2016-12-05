from google.appengine.ext import ndb
import webapp2
import os
import logging
import db_entities
from google.appengine.ext import blobstore
from google.appengine.api import images
import datetime
import calendar
import json
class get_single_person(webapp2.RequestHandler):
	def get(self,**kwargs):
		results = []
		if 'userKey' in kwargs and 'personKey' in kwargs:
			userKey = kwargs['userKey']
			personKey = kwargs['personKey']
			try:
				user = ndb.Key(urlsafe=userKey).get()
			except:
				results = {'result':'fail','cause':'You must log in with a valid user'}				
			try:
				person = ndb.Key(urlsafe=personKey).get()
			except:
				results = {'result':'fail','cause':'You requeset a valid person'}
			if results == [] and user and person:
				results = {'result':'sucess','firstName':person.firstName,'lastName':person.lastName,'dob':str(person.dob),'key':person.key.urlsafe()}

		else:
			results = {'result':'fail','cause':'You must be logged in and provide a valid person'}
		self.response.write(json.dumps(results))

class basic(webapp2.RequestHandler):
	def get(self, **kwargs):#get a listing of photos for this user, along with their serving URL
		results = []
		if 'userKey' in kwargs:
			key=kwargs['userKey']
			try:
				user = ndb.Key(urlsafe=key).get()#verify actual user
			except:
				results = {'result':'fail','cause':'You must log in with a valid user'}	
			if results == []:#if results not filled by except, then fill with photos
				results = {'result':'success','people':[{'firstName':i.firstName, 'lastName':i.lastName,'dob':str(i.dob),'key':i.key.urlsafe(),'taggedPhotos':[x.urlsafe() for x in i.taggedPhotos]} for i in db_entities.person.query(ancestor=ndb.Key(urlsafe=key)).fetch()]}
		else:
			results = {'result':'fail','cause':'You must be logged in'}
		self.response.write(json.dumps(results))

	def post(self,img_key=None):#post a new photo
		key = self.request.get('userKey')
		results = []
		try:
			user = ndb.Key(urlsafe=key).get()#verify actual user
		except:
			results = {'result':'fail','cause':'You must log in with a valid user'}
		new_person = db_entities.person(parent=ndb.Key(urlsafe=key))
		new_person.firstName = self.request.get('firstName')
		new_person.lastName = self.request.get('lastName')
		new_person.dob = datetime.datetime.strptime(self.request.get('dob').replace('/','-').replace('.','-'),'%Y-%m-%d')#get date to proper format
		#verify new person doesn't exist
		for i in db_entities.person.query(ancestor=ndb.Key(urlsafe=key)).fetch():
			if i.firstName == new_person.firstName and i.lastName == new_person.lastName and i.dob == new_person.dob.date():
				results = {'result':'fail','cause':'That person already exists.'}
		if results ==[]:#if results not filled by except above, then fill with photo
			new_person.put()
			results = {'result':'success','firstName':new_person.firstName,'lastName':new_person.lastName,'dob':str(new_person.dob),'key':new_person.key.urlsafe()}
		self.response.write(json.dumps(results))


#the following two classes could be put into one change/alter class, but I'm keeping them seperate at this time to make routing easier (this way I can use a photo delete url, and a photo edit url)
class edit(webapp2.RequestHandler):
	def put(self, **kwargs):#should use patch, currently put due to GAE/webapp2 not having patch functionality
		userKey=kwargs['userKey']
		personKey=kwargs['personKey']
		results = {}
		try:
			user = ndb.Key(urlsafe=userKey).get()#verify actual user
		except:
			results = {'result':'fail','cause':'You must log in with a valid user'}
		try:
			person = ndb.Key(urlsafe=personKey).get()
		except:
			results = {'result':'fail','cause':'You must proivde a valid person'}
		if self.request.get('firstName') and self.request.get('firstName') != person.firstName and person and user:
			oldFirstName = person.firstName
			person.firstName = self.request.get('firstName')
			results = results
			results['changed'] = 'yes'
			results['oldFirstName'] = oldFirstName
			results['newFirstname'] = person.firstName
		if self.request.get('lastName') and self.request.get('lastName') != person.lastName and person and user:
			oldLastname = person.lastName
			person.lastName = self.request.get('lastName')
			results['changed'] = 'yes'
			results['oldLastName'] = oldLastname
			results['newLastname'] = person.lastName
		if self.request.get('dob') and datetime.datetime.strptime(self.request.get('dob').replace('/','-').replace('.','-'),'%Y-%m-%d').date() != person.dob and person and user:
			oldDob = person.dob
			person.dob = datetime.datetime.strptime(self.request.get('dob').replace('/','-').replace('.','-'),'%Y-%m-%d')
			results['changed'] = 'yes'
			results['oldDob'] = datetime.date.isoformat(oldDob)
			results['newDob'] = datetime.date.isoformat(person.dob)
		#verify person changed
		if 'changed' not in results:
			results['changed'] = 'no'
			results['result'] = 'fail'
			results['cause'] = 'You haven\'t changed anything on that person.'
		#verify not editing a person to be a copy of another person
		elif person and user:
			for i in db_entities.person.query(ancestor=ndb.Key(urlsafe=userKey)).fetch():
				if i.firstName == person.firstName and i.lastName == person.lastName and i.dob == person.dob and i != person:
					results = {'result':'fail','cause':'That person already exists.'}
		if 'result' not in results:
			results['result'] = 'success'
			person.put()

		self.response.write(json.dumps(results))

class delete(webapp2.RequestHandler):
	def delete(self,**kwargs):
		userKey=kwargs['userKey']
		personKey=kwargs['personKey']
		results = []
		try:
			user = ndb.Key(urlsafe=userKey).get()#verify actual user
		except:
			results = {'result':'fail','cause':'You must log in with a valid user'}
		try:
			person = ndb.Key(urlsafe=personKey).get()
		except:
			results = {'result':'fail','cause':'You must proivde a valid person'}
		if results == [] and person and user:
			for i in person.taggedPhotos:
				photo = i.get()
				photo.taggedPeople = [x for x in photo.taggedPeople if x != person.key]
				photo.put()
			name = person.firstName + ' ' + person.lastName
			person.key.delete()
			results = {'result':'success','deleted':name}
		else:
			results = {'result':'fail','cause':'You must log in with a valid user and provide a valid person to delete'}
		self.response.write(json.dumps(results))