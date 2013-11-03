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
import datetime
from time import strftime, gmtime

import urllib
import urllib2

from urlparse import urlparse


from google.appengine.api import users
from google.appengine.api import mail

from webapp2_extras import sessions

from google.appengine.api import channel




jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(['templates', 'templates/examples']),
    extensions=['jinja2.ext.autoescape'])


class MainHandler(webapp2.RequestHandler):
  def get(self):
    template = jinja_environment.get_template('index.html')
    login_url = users.create_login_url('/')
    logout_url = users.create_logout_url('/')
    user = users.get_current_user()
    token = channel.create_channel(user.user_id())
    self.response.out.write(template.render(user=user.email(),
                                            token=token,
                                            logout_url=logout_url))


  def post(self):
    email = users.get_current_user().email()
    if not mail.is_email_valid(email):
      pass
    else:
      subject = "Testing Gmail Actions " + datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
      content = self.request.get('content')
      body = content
      mail.send_mail(email, email, subject, body='', html=body)
    self.response.out.write('The email was sent.')


  @webapp2.cached_property
  def session(self):
      # Returns a session using the default cookie key.
      # send_message(client_id, message)
      return self.session_store.get_session()


class SampleHandler(webapp2.RequestHandler):
    def get(self, sample, token):
      google_now_date = self.request.get('googleNowDate')
      template = jinja_environment.get_template(sample + '.html')
      self.response.out.write(template.render(token=token, google_now_date=google_now_date))



class FailureHandler(webapp2.RequestHandler):
    def get(self, token):
      channel.send_message(token, 'Searver encounter an error! 400 Bad Request ' + self.request.path)
      self.error(400)
      self.response.out.write('failure')


class SuccessHandler(webapp2.RequestHandler):
    def get(self, token):
      channel.send_message(token, 'Received a call! 200 OK ' + self.request.path)
      self.response.out.write('success')

    def post(self, token):
      channel.send_message(token, 'Received a call! 200 OK ' + self.request.path + ' \n' + str(self.request.POST.items()))
      self.response.out.write('success')





config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}


app = webapp2.WSGIApplication([

    webapp2.Route('/success/<token>', handler=SuccessHandler, name='success'),
    webapp2.Route('/failure/<token>', handler=FailureHandler, name='failure'),
    webapp2.Route('/examples/<sample>/<token>', handler=SampleHandler, name='sample'),
    ('/', MainHandler),
], config=config, debug=True)
