from google.appengine.ext import ndb

class user(ndb.Model):
	userName = ndb.StringProperty(required=True)
	password = ndb.StringProperty(required=ndb.Model)

class photo(ndb.Model):
	photoDescription = ndb.StringProperty(required=True)
	uploadDate = ndb.DateProperty(required=True)
	image = ndb.BlobProperty()
	taggedPeople = ndb.KeyProperty(repeated=True)

class person(ndb.Model):
	firstName = ndb.StringProperty(required=True)
	lastName = ndb.StringProperty(required=True)
	dob = ndb.DateProperty(required=True)
	taggedPhotos = ndb.KeyProperty(repeated=True)