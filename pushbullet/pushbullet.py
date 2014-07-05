"""
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

import json
from urlparse import urljoin

import requests
import os
import magic

from . import __version__, __project_name__, __project_link__

class Pushbullet(object):
	
	def __init__(self, api_key,
		api_uri='https://api.pushbullet.com/v2/',
		verify_ssl=True):
		
		self.api_key = api_key
		self.api_uri = api_uri
		
		self.api_uri_devices = urljoin(api_uri, 'devices')
		self.api_uri_pushes = urljoin(api_uri, 'pushes')
		self.api_uri_upload_requests = urljoin(api_uri, 'upload-request')
		
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
							data=payload,
							files=files,
							auth=(self.api_key, ''),
							headers=self.headers,
							verify=self.verify_ssl
							)
		
		return r

	def _post_no_auth(self, url, payload={}, files={}):
		# TODO Add exceptions for the different HTTP Error codes.
		
		r = requests.post(url,
							data=payload,
							files=files,
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
	
	def bullet_file(self, device_iden, file, body=None):
		# TODO check if file exists

		# See http://docs.pushbullet.com/v2/upload-request/
		# 1. First request the permission to upload
		mimetype = magic.from_file(file, mime=True)
		payload_upload = {
			'file_name': os.path.basename(file),
			'file_type': mimetype,
		}

		upload_request = self._post(self.api_uri_upload_requests, payload_upload)
		upload_data = upload_request.json()

		# 2. Do the actual upload of the file
		files = {
			'file': open(file, 'rb')		
		}
	
		actual_upload = self._post_no_auth(upload_data['upload_url'], upload_data['data'], files)
		actual_upload.raise_for_status() # stop if there was a bad request

		# 3. Push the file to the device
		payload_push = {
			'type': 'file',
			'device_iden': device_iden,
			'file_name': upload_data['file_name'],
			'file_type': upload_data['file_type'],
			'file_url': upload_data['file_url'],
		}

		if isinstance(body, str) and len(body) > 0:
			payload_push['body'] = body

		r = self._post(self.api_uri_pushes, payload_push)

		return r.json()
