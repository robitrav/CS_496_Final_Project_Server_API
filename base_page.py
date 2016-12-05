import webapp2
import os
import jinja2

class BaseHandler(webapp2.RequestHandler):
	
	@webapp2.cached_property
	def jinja2(self):
		return jinja2.Environment(
		loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
		extensions=['jinja2.