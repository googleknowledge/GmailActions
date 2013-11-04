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
import webapp2
import logging
import datetime
from time import strftime, gmtime

from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.api import channel


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(['templates', 'templates/examples']),
    extensions=['jinja2.ext.autoescape'])


class MainHandler(webapp2.RequestHandler):

  def get(self):
    """Serves the homepage"""
    template = jinja_environment.get_template('index.html')
    logout_url = users.create_logout_url('/')
    user = users.get_current_user()
    token = channel.create_channel(user.user_id())
    self.response.out.write(template.render(user=user.email(),
                                            token=token,
                                            logout_url=logout_url))

  def post(self):
    """Sends email with embedded structured data."""
    email = users.get_current_user().email()
    if not mail.is_email_valid(email):
      self.response.out.write('Invalid email.')
    else:
      subject = "Testing Gmail Actions " + datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
      content = self.request.get('content')
      body = content
      mail.send_mail(email, email, subject, body='', html=body)
      self.response.out.write('The email was sent.')


class SampleHandler(webapp2.RequestHandler):
  def get(self, sample, token):
    """Returns the content of a sample email with embedded structured data.

    Args:
      sample: The type of the sample email to return.
      token: Channel Client token. It is used to construct a callback url for actions.
    """
    google_now_date = self.request.get('googleNowDate')
    template = jinja_environment.get_template(sample + '.html')
    self.response.out.write(template.render(token=token, google_now_date=google_now_date))


class FailureHandler(webapp2.RequestHandler):
    def get(self, token):
      """An example implementation of a Gmail action's handler url.

      In this example it is a static url, always returns status 400. It also notifies
      the UI via the channel service that this call was received.
      """
      msg = ('Searver encounter an error! <span class="failure">400 Bad Request</span> ' +
             '<span class="path">/failure/token</span>')
      channel.send_message(token, msg)
      self.error(400)
      self.response.out.write('failure')


class SuccessHandler(webapp2.RequestHandler):
    def get(self, token):
      """An example implementation of a Gmail action's handler url.

      In this example it is a static url, always returns status 200. It also notifies
      the UI via the channel service that this call was received.
      """
      msg = ('Received a call! <span class="success">200 OK</span> ' +
             '<span class="path">/success/token</span>')
      channel.send_message(token, msg)
      self.response.out.write('success')

    def post(self, token):
      """An example implementation of a Gmail action's handler url.

      In this example it is a static url, always returns status 200. It also notifies
      the UI via the channel service that this call was received.
      """
      msg = ('Received a call! <span class="success">200 OK</span> ' +
             '<span class="path">/success/token</span>')
      if self.request.POST.items():
        msg = msg + ' Params: '
      for param in self.request.POST.items():
        msg = msg + (' %s=%s' % param)
      channel.send_message(token, msg)
      self.response.out.write('success')


app = webapp2.WSGIApplication([
    webapp2.Route('/success/<token>', handler=SuccessHandler, name='success'),
    webapp2.Route('/failure/<token>', handler=FailureHandler, name='failure'),
    webapp2.Route('/examples/<sample>/<token>', handler=SampleHandler, name='sample'),
    ('/', MainHandler),
], debug=True)
