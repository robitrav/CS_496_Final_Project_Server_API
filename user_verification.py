from google.appengine.ext import ndb
import webapp2
#import jinja2
#import base_page
import logging
import db_entities
from google.appengine.ext import blobstore#TBD
from google.appengine.api import images#TBD
import json

class user_login(webapp2.RequestHandler):

	def get(self):
		self.response.write("Congrats. The site is currently running")

	def post(self):
		if self.request.get('userName') and self.request.get('password'):#ensure req'd components present
			query = db_entities.user.query(db_entities.user.userName == self.request.get('userName'))
			for i in query:
				if self.request.get('userName') == i.userName:
					if self.request.get('password') == i.password:
						key = i.key.urlsafe()
						results = {'result':'success','key':key}
						self.response.write(json.dumps(results))
						return
					else:
						results = {'result':'fail','cause':'password fail'}
						self.response.write(json.dumps(results))
						return
			results = {'result':'fail','cause':'User name not in use'}
			self.response.write(json.dumps(results))
		else:
			results = {'result':'fail','cause':'Missing username or password'}
			self.response.write(json.dumps(results))

class user_create_account(webapp2.RequestHandler):
	def post(self):
		if self.request.get('userName') and self.request.get('password'):#verify required components present
			new_user = db_entities.user(parent=ndb.Key(db_entities.user,self.app.config.get('user-group')))
			new_user.userName = self.request.get('userName')#assign values
			new_user.password = self.request.get('password')
			query = db_entities.user.query(db_entities.user.userName == new_user.userName)#make search to determine that values available
			userNameAvailable = True
			for i in query:
				if new_user.userName == i.userName:
					userNameAvailable = False
					break
			if userNameAvailable == False:#if not, inform that user name is used
				results = {'result':'fail','cause':'That user name already exists. Please select another'}
			else:#else add new user
				key = new_user.put().urlsafe()
				results = {'result':'success','key':key}
		else:
			results = {'result':'fail','cause':'Missing username or password'}
		self.response.write(results)