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

class basic(webapp2.RequestHandler):
	