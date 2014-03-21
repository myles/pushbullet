#!/usr/bin/env python
"""
A Python Library for Pushbullet: <https://www.pushbullet.com>.

Copyright (c) 2014, Myles Braithwaite <me@mylesbraithwaite.com>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

* Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in
  the documentation and/or other materials provided with the
  distribution.

* Neither the name of the Monkey in your Soul nor the names of its
  contributors may be used to endorse or promote products derived
  from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

__version__ = '0.1'
__project_name__ = 'PushbulletPythonLibrary'
__project_link__ = 'https://gist.github.com/myles/9688926'

import json
import argparse
from urlparse import urljoin

import requests

from clint.textui import puts, indent

class Pushbullet(object):
	
	def __init__(self, api_key,
		api_uri='https://api.pushbullet.com/api/',
		verify_ssl=True):
		
		self.api_key = api_key
		self.api_uri = api_uri
		
		self.api_uri_devices = urljoin(api_uri, 'devices')
		self.api_uri_pushes = urljoin(api_uri, 'pushes')
		
		self.headers = {
			'User-Agent': "%s/%s +%s" % (
				__project_name__,
				__version__,
				__project_link__
			)
		}
		
		self.verify_ssl = verify_ssl
	
	def _get(self, url):
		# TODO Add exceptions for the different HTTP Error codes.
		
		r = requests.get(url,
							auth=(self.api_key, ''),
							headers=self.headers,
							verify=self.verify_ssl
							)
		
		return r
	
	def _post(self, url, payload={}, files={}):
		# TODO Add exceptions for the different HTTP Error codes.
		
		r = requests.post(url,
							params=payload,
							files=files,
							auth=(self.api_key, ''),
							headers=self.headers,
							verify=self.verify_ssl
							)
		
		return r
	
	def list_devices(self):
		r = self._get(self.api_uri_devices)
		
		return r.json()
	
	def bullet_note(self, device_iden, title, body=''):
		payload = {
			'type': 'note',
			'device_iden': device_iden,
			'title': title,
			'body': body,
		}
		
		r = self._post(self.api_uri_pushes, payload)
		
		return r.json()
	
	def bullet_link(self, device_iden, title, link):
		payload = {
			'type': 'link',
			'device_iden': device_iden,
			'title': title,
			'link': link,
		}
		
		r = self._post(self.api_uri_pushes, payload)
		
		return r.json()
	
	def bullet_address(self, device_iden, name, address):
		payload = {
			'type': 'address',
			'device_iden': device_iden,
			'name': name,
			'address': address,
		}
		
		r = self._post(self.api_uri_pushes, payload)
		
		return r.json()
	
	def bullet_list(self, device_iden, title, items):
		payload = {
			'type': 'list',
			'device_iden': device_iden,
			'title': title,
			'items': items,
		}
		
		r = self._post(self.api_uri_pushes, payload)
	
	def bullet_file(self, device_iden, file):
		payload = {
			'type': 'file',
			'device_iden': device_iden,
		}
		
		files = {
			'file': file,
		}
		
		r = self._post(self.api_uri_pushes, payload, files)
		
		return r.json()

def main(args):
	
	pushbullet = Pushbullet(api_key=args.api_key)
	
	if args.list_devices:
		devices = pushbullet.list_devices()['devices']
		
		puts("Pushbullet devices:")
		
		with indent(4):
			for device in devices:
				puts("%(nickname)s: %(iden)s" % {
					'nickname': device['extras']['nickname'],
					'iden': device['iden']
				})
		
	elif args.device:
		if args.type == 'note':
			if args.title or args.body:
				title = args.title
				body = args.body
			else:	
				title = raw_input('Title: ')
				body = raw_input('Body: ')
			
			response = pushbullet.bullet_note(args.device, title, body)
			
		elif args.type == 'link':
			if args.title or args.url:
				title = args.title
				url = args.url
			else:
				title = raw_input('Title: ')
				url = raw_input('URL: ')
			
			response = pushbullet.bullet_link(args.device, title, url)
			
		elif args.type == 'address':
			if args.title and args.body:
				name = args.title
				address = args.body
			else:
				name = raw_input('Name: ')
				address = raw_input('Address: ')
			
			response = pushbullet.bullet_address(args.device, name, address)
			
		elif args.type == 'list':
			if args.title or args.items:
				title = args.title
				_items = args.items
			else:
				title = raw_input('Title: ')
				_items = raw_input('Items: ')
			
			items = _items.split(', ')
			
			response = pushbullet.bullet_list(args.device, title, items)
			
		elif args.type == 'file':
			response = pushbullet.bullet_file(args.device, args.file)

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser()
	
	parser.add_argument('-a', '--apikey', required=True, action='store',
		dest='api_key', help="What is your Pushbullet API key?")
	
	parser.add_argument('-d', '--device', action='store', dest='device',
		help="What device do you want to send the bullet to?")
	
	parser.add_argument('-t', '--type', action='store', dest='type', default="note",
		choices=['note', 'link', 'address', 'list', 'file'],
		help="What type of bullet do you want to send?")
	
	parser.add_argument('-n', '--name', '--title', action='store', dest='title',
		help="The title/name of the note, link, address, or list.")
	parser.add_argument('-b', '--body', '--address', action='store', dest='body',
		help="The body/address of the note or address.")
	parser.add_argument('-i', '--items', action='store', dest='items',
		help="The items in a list.")
	parser.add_argument('-f', '--file', action='store', dest='file',
		type=argparse.FileType('rb'), help="The file to push.")
	
	parser.add_argument('-l', '--list-devices', action='store_true',
		dest='list_devices', help="Get a list of devices.")
	
	args = parser.parse_args()
	
	main(args)