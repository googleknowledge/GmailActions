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



jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])



class MainHandler(webapp2.RequestHandler):
  def get(self):
    template = jinja_environment.get_template('index.html')
    login_url = users.create_login_url('/')
    logout_url = users.create_logout_url('/')
    self.response.out.write(template.render(login_url=login_url, logout_url=logout_url))


  def post(self):
    email = users.get_current_user().email()
    if not mail.is_email_valid(email):
      pass
    else:
      subject = "Confirm your registration"
      content = self.request.get('email-content')
      body = content
      mail.send_mail(email, email, subject, body='', html=body)







app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
