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

class person_photo_tagging(webapp2.RequestHandler):
	def put(self, **kwargs):
		userKey = kwargs['userKey']
		photoKey = kwargs['photoKey']
		personKey = kwargs['personKey']
		user = photo = person = []
		results = []
		try:
			user = ndb.Key(urlsafe=userKey).get()#verify actual user
		except:
			results = {'result':'fail','cause':'You must log in with a valid user'}
		try:
			photo = ndb.Key(urlsafe=photoKey).get()
		except:
			results = {'result':'fail','cause':'You must proivde a valid photo'}
		try:
			person = ndb.Key(urlsafe=personKey).get()
		except:
			results = {'result':'fail','cause':'You must proivde a valid person'}
		if person and photo and user:
			person.taggedPhotos.append(photo.key)
			photo.taggedPeople.append(person.key)
			results = {'result':'success','photoDescription':photo.photoDescription,'personName':person.firstName + ' ' + person.lastName,'personKey':person.key.urlsafe(),'photoKey':photo.key.urlsafe()}
			photo.put()
			person.put()
		if results == []:
			results = {'result':'fail','cause':'You must be logged in with a valid user, and provide a valid person and valid photo'}
		self.response.write(json.dumps(results))


	def delete(self, **kwargs):
		userKey = kwargs['userKey']
		photoKey = kwargs['photoKey']
		personKey = kwargs['personKey']
		user = photo = person = []
		try:
			user = ndb.Key(urlsafe=userKey).get()#verify actual user
		except:
			results = {'result':'fail','cause':'You must log in with a valid user'}
		try:
			photo = ndb.Key(urlsafe=photoKey).get()
		except:
			results = {'result':'fail','cause':'You must proivde a valid photo'}
		try:
			person = ndb.Key(urlsafe=personKey).get()
		except:
			results = {'result':'fail','cause':'You must proivde a valid person'}
		if person and photo and user:
			person.taggedPhotos = [i for i in person.taggedPhotos if i != photo.key]
			photo.taggedPeople = [i for i in photo.taggedPeople if i != person.key]
			photo.put()
			person.put()
			results = {'result':'success','photoDescription':photo.photoDescription, 'personName':person.firstName + ' ' + person.lastName,'personKey':person.key.urlsafe(),'photoKey':photo.key.urlsafe()}
		self.response.write(json.dumps(results))
