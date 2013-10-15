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
import xml.etree.ElementTree as ET


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])



class MainHandler(webapp2.RequestHandler):
  def get(self):
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render())


class CseHandler(webapp2.RequestHandler):
  def get(self):


    #api_key = open(".freebase_api_key").read()
    api_key = 'AIzaSyDOtKtaEkS2HLzn38knX6FDwtbP61G84ig'
    service_url = 'https://www.googleapis.com/freebase/v1/topic'
    #topic_id = '/m/010q36'
    topic_id = self.request.get('mid')
    params = {
      'key': api_key,
      'filter': 'suggest',
      'filter': '/common/topic/topic_equivalent_webpage'
    }
    url = service_url + topic_id + '?' + urllib.urlencode(params)
    topic = json.loads(urllib.urlopen(url).read())

    #print topic
    """
    for property in topic['property']:
      print property + ':'
      for value in topic['property'][property]['values']:
        print ' - ' + value['text']
    """

    template = jinja_environment.get_template('annotations.xml')

    root = ET.Element("html")

    head = ET.SubElement(root, "head")

    title = ET.SubElement(head, "title")
    title.text = "Page Title"

    body = ET.SubElement(root, "body")
    body.set("bgcolor", "#ffffff")

    body.text = "Hello, World!"

    # wrap it in an ElementTree instance, and save as XML
    tree = ET.ElementTree(root)
    print dir(ET)

    xmlstr = ET.dump(tree)
    print xmlstr



    values = topic['property']['/common/topic/topic_equivalent_webpage']['values']
    for value in values:
      pass
      #print value['value']
      #o = urlparse(value['value'])
      #print '%s/' % o['netloc']
      #print o.path.split('/')[1:-1]
      #print '%s%s*' % (o.netloc, '/'.join(o.path.split('/')[:-1]))



    self.response.headers['Content-Type'] = 'application/xml'

    self.response.out.write(template.render(topic=topic, values=values))







app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/cse', CseHandler)
], debug=True)
