#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import jinja2
import os

import json

#import xmltodict

import webapp2
import logging

import urllib
import urllib2

from urlparse import urlparse
#import elementtree.ElementTree as ET

from google.appengine.api import users
from google.appengine.api import mail

from webapp2_extras import sessions



jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])


class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)


class MainHandler(BaseHandler):
  def get(self):
    template = jinja_environment.get_template('index.html')
    login_url = users.create_login_url('/')
    logout_url = users.create_logout_url('/')
    self.session['foo'] = 'bar'
    foo = self.session.get('foo')
    logging.info(foo)
    self.session.add_flash('value', level=None, key='_flash')

    user = users.get_current_user()
    logging.info(user.email())

    self.response.out.write(template.render(user=user.email(), logout_url=logout_url, flash=self.session.get_flashes(key='_flash')))


  def post(self):
    email = users.get_current_user().email()
    if not mail.is_email_valid(email):
      pass
    else:
      subject = "Confirm your registration"
      content = self.request.get('content')
      body = content
      mail.send_mail(email, email, subject, body='', html=body)
    self.redirect('/')

  @webapp2.cached_property
  def session(self):
      # Returns a session using the default cookie key.
      return self.session_store.get_session()


class FailureHandler(webapp2.RequestHandler):
    def get(self):
      self.error(502)
      self.response.out.write('failure')


class SuccessHandler(webapp2.RequestHandler):
    def get(self):
      self.response.out.write('success')




config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/success', SuccessHandler),
    ('/failure', FailureHandler),
], config=config, debug=True)
