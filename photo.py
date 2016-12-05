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

class get_single_photo(webapp2.RequestHandler):
	def get(self,**kwargs):
		if 'userKey' in kwargs and 'photoKey' in kwargs:
#			results = {'hello':'goodbye'}
			userKey = kwargs['userKey']
			photoKey = kwargs['photoKey']
			results = []
			try:
				user = ndb.Key(urlsafe=userKey).get()#verify actual user
			except:
				results = {'result':'fail','cause':'You must log in with a valid user'}
			try:
				photo = ndb.Key(urlsafe=photoKey).get()#verify actual user
			except:
				results = {'result':'fail','cause':'You must request a valid photo'}
			if results == [] and user and photo:
				results = {'result':'success','description':photo.photoDescription,'uploadDate':str(photo.uploadDate),'key':photo.key.urlsafe(),'image':images.get_serving_url(photo.image),'taggedPeople':[i.urlsafe() for i in photo.taggedPeople]}
			else:
				results = {'result':'fail','cause':'You must log in with a valid user, and request a valid photo'}	
		else:
			results = {'result':'fail','cause':'You must be logged in'}
		self.response.write(json.dumps(results))

class basic(webapp2.RequestHandler):
	def get(self, **kwargs):#get a listing of photos for this user, along with their serving URL
		logging.info("getting photos")
		results = []
		if 'userKey' in kwargs and 'photoKey' not in kwargs:
			key=kwargs['userKey']
			try:
				user = ndb.Key(urlsafe=key).get()#verify actual user
			except:
				results = {'result':'fail','cause':'You must log in with a valid user'}	
			if results == []:#if results not filled by except, then fill with photos
				results = [{'description':i.photoDescription,'uploadDate':str(i.uploadDate),'key':i.key.urlsafe(), 'image':images.get_serving_url(i.image)} for i in db_entities.photo.query(ancestor=ndb.Key(urlsafe=key)).fetch()]			
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
		new_photo = db_entities.photo(parent=ndb.Key(urlsafe=key))
		new_photo.photoDescription = self.request.get('photoDescription')
		new_photo.uploadDate=datetime.datetime.now().date()
		new_photo.image=str(img_key)
		#verify photo doesn't already exist
		for i in db_entities.photo.query(ancestor=ndb.Key(urlsafe=key)).fetch():
			if i.photoDescription == new_photo.photoDescription and i.uploadDate == new_photo.uploadDate:
				results = {'result':'fail','cause':'That photo already exists. If you\'re sure it doesn\'t, upload the photo with a new description'}
		if results == []:
			new_photo.put()
			results = {'result':'success','description':new_photo.photoDescription,'uploadDate':str(new_photo.uploadDate),'key':new_photo.key.urlsafe(),'image':images.get_serving_url(new_photo.image)}
		self.response.write(json.dumps(results))

class getUploadURL(webapp2.RequestHandler):#send upload URL to client
	def get(self, **kwargs):
		if 'userKey' in kwargs:
			try:
				user = ndb.Key(urlsafe=kwargs['userKey']).get()#verify actual user
				upload_url = blobstore.create_upload_url('/upload_photo')
				results = {'uploadurl':upload_url}
			except:
				results = {'result':'fail','cause':'You must log in with a valid user'}
		else:
			results = {'result':'fail','cause':'You must be logged in'}
		self.response.write(json.dumps(results))			

#the following two classes could be put into one change/alter class, but I'm keeping them seperate at this time to make routing easier (this way I can use a photo delete url, and a photo edit url)
class edit(webapp2.RequestHandler):
	def put(self, **kwargs):#should use patch, currently put due to GAE/webapp2 not having patch functionality
		userKey=kwargs['userKey']
		photoKey=kwargs['photoKey']
		results = []
		try:
			user = ndb.Key(urlsafe=userKey).get()#verify actual user
		except:
			results = {'result':'fail','cause':'You must log in with a valid user'}
		try:
			photo = ndb.Key(urlsafe=photoKey).get()
		except:
			results = {'result':'fail','cause':'You must proivde a valid photo'}
		if self.request.get('photoDescription'):
			oldDescription = photo.photoDescription
			photo.photoDescription = self.request.get('photoDescription')
			results = {'result':'success','changed':'photoDescription','from':oldDescription,'to':photo.photoDescription}	
			photo.put()		
		else:
			results = {'result':'fail','cause':'Must provide photo detail to change'}
		self.response.write(json.dumps(results))

class delete(webapp2.RequestHandler):
	def delete(self,**kwargs):
		userKey=kwargs['userKey']
		photoKey=kwargs['photoKey']
		results = []
		try:
			user = ndb.Key(urlsafe=userKey).get()#verify actual user
		except:
			results = {'result':'fail','cause':'You must log in with a valid user'}
		try:
			photo = ndb.Key(urlsafe=photoKey).get()
		except:
			results = {'result':'fail','cause':'You must proivde a valid photo'}
		if results == [] and photo and user:
			for i in photo.taggedPeople:
				person = i.get()
				person.taggedPhotos = [x for x in person.taggedPhotos if x != photo.key]
				person.put()
			photoDescription = photo.photoDescription
			uploadDate = photo.uploadDate
			photo.key.delete()
			results = {'result':'success','deleted':photoDescription}
		else:
			results = {'result':'fail','cause':'You must log in with a valid user, and provide a valid photo to delete'}
		self.response.write(json.dumps(results))		