# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.appengine.ext import ndb
import webapp2
import webapp2_extras.routes#needed for strict slashing-not used below due to other slashes
import photo
import uploadHandler
import person_photo_tagging

config = {'user-group':'user-data'}

app = webapp2.WSGIApplication([], debug=True,config=config)

#routes for user creation/verification
app.router.add(webapp2.Route(r'/user_login',handler='user_verification.user_login',name='user_login'))
app.router.add(webapp2.Route(r'/user_create_account',handler='user_verification.user_create_account',name='create_account'))

#routes for photos
app.router.add(webapp2.Route(r'/photo',handler='photo.basic',name='basic_photo_actions'))
app.router.add(webapp2.Route(r'/photo/<userKey:[0-9,a-z,A-Z,/-]+>',handler='photo.basic',name='basic_photo_actions'))
app.router.add(webapp2.Route(r'/photo_get_single/<userKey:[0-9,a-z,A-Z,/-]+>/<photoKey:[0-9,a-z,A-Z,/-]+>',handler='photo.get_single_photo',name='get_single_photo'))
app.router.add(webapp2.Route(r'/edit_photo/<userKey:[0-9,a-z,A-Z,/-]+>/<photoKey:[0-9,a-z,A-Z,/-]+>',handler='photo.edit',name='edit_photo_action'))
app.router.add(webapp2.Route(r'/delete_photo/<userKey:[0-9,a-z,A-Z,/-]+>/<photoKey:[0-9,a-z,A-Z,/-]+>',handler='photo.delete',name='delete_photo_action'))

#routes for photo uploading
app.router.add(webapp2.Route(r'/photo_get_upload_url/<userKey:[0-9,a-z,A-Z,/-]+>',handler='photo.getUploadURL',name='getUploadURL'))
app.router.add(webapp2.Route(r'/upload_photo',handler='uploadHandler.uploadHandler',name='upload_photo'))

#routes for persons
app.router.add(webapp2.Route(r'/person',handler='person.basic',name='basic_person_actions'))
app.router.add(webapp2.Route(r'/person/<userKey:[0-9,a-z,A-Z,/-]+>',handler='person.basic',name='basic_person_actions'))
app.router.add(webapp2.Route(r'/person_get_single/<userKey:[0-9,a-z,A-Z,/-]+>/<personKey:[0-9,a-z,A-Z,/-]+>',handler='person.get_single_person',name='get_single_person'))
app.router.add(webapp2.Route(r'/edit_person/<userKey:[0-9,a-z,A-Z,/-]+>/<personKey:[0-9,a-z,A-Z,/-]+>',handler='person.edit',name='edit_person_action'))
app.router.add(webapp2.Route(r'/delete_person/<userKey:[0-9,a-z,A-Z,/-]+>/<personKey:[0-9,a-z,A-Z,/-]+>',handler='person.delete',name='delete_person_action'))

#routes for adding/removing people to/from photos
app.router.add(webapp2.Route(r'/tag_person/<userKey:[0-9,a-z,A-Z,/-]+>/photo/<photoKey:[0-9,a-z,A-Z,/-]+>/person/<personKey:[0-9,a-z,A-Z,/-]+>',handler='person_photo_tagging.person_photo_tagging',name='tagging_people'))
#app.router.add(webapp2.Route(r'/tag_person',handler='person_photo_tagging.photo_tagging',name='tagging_people'))

#app.router.add(webapp2.Route(r'/stuff',handler='person_photo_tagging.photo_tagging',name='photo_tagging'))
