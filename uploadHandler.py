import webapp2
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import main
import logging
import photo
#import homepage

class uploadHandler (blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		upload_file = self.get_uploads('image')
		if upload_file != []:
			blob_info = upload_file[0]
			img_key=blob_info.key()
			photo.basic(self.request,self.response).post(img_key=blob_info.key())
		else:
			photo.basic(self.request,self.response).post()