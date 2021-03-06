#!/usr/bin/env python
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

import argparse

from clint.textui import puts, indent, prompt

from pushbullet import Pushbullet


def list_devices(pushbullet):
    devices = pushbullet.list_devices()['devices']

    puts("Pushbullet devices:")

    with indent(4):
        for device in devices:
            nickname = device.get('nickname', 'unknown')

            puts("%(nickname)s: %(iden)s" % {
                'nickname': nickname,
                'iden': device['iden']
            })


def push_note(args, pushbullet):
    if args.title or args.url:
        title = args.title
        body = args.body
    else:
        title = prompt.query('Title: ')
        body = prompt.query('Body (optional): ', validators=[])

    return pushbullet.bullet_note(args.device, title, body)


def push_link(args, pushbullet):
    if args.title or args.url:
        title = args.title
        url = args.url
    else:
        title = prompt.query('Title: ')
        url = prompt.query('URL: ')

    return pushbullet.bullet_link(args.device, title, url)


def push_list(args, pushbullet):
    if args.title or args.items:
        title = args.title
        _items = args.items
    else:
        title = prompt.query('Title: ')
        _items = prompt.query('Items (separate by comma): ')

    items = _items.split(', ')

    return pushbullet.bullet_list(args.device, title, items)


def push_address(args, pushbullet):
    if args.title and args.body:
        name = args.title
        address = args.body
    else:
        name = prompt.query('Name: ')
        address = prompt.query('Address: ')

    return pushbullet.bullet_address(args.device, name, address)


def push_file(args, pushbullet):
    return pushbullet.bullet_file(
        args.device, args.file, args.body)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--apikey', required=True, action='store',
                        dest='api_key',
                        help="What is your Pushbullet API key?")

    parser.add_argument('-d', '--device', action='store', dest='device',
                        help="What device do you want to send the bullet to?")

    parser.add_argument('-t', '--type', action='store', dest='type',
                        default="note",
                        choices=['note', 'link', 'address', 'list', 'file'],
                        help="What type of bullet do you want to send?")

    parser.add_argument('-n', '--name', '--title', action='store',
                        dest='title',
                        help="The title/name of the note, link, address, " +
                             " or list.")

    parser.add_argument('-b', '--body', '--address', action='store',
                        dest='body',
                        help="The body, address of the note or additional " +
                             "data for a file.")
    parser.add_argument('-u', '--url', action='store', dest='url',
                        help="The referenced url of the link.")
    parser.add_argument('-i', '--items', action='store', dest='items',
                        help="The items in a list.")
    parser.add_argument('-f', '--file', action='store', dest='file',
                        type=argparse.FileType('rb'), help="The file to push.")

    parser.add_argument('-l', '--list-devices', action='store_true',
                        dest='list_devices', help="Get a list of devices.")

    args = parser.parse_args()

    pushbullet = Pushbullet(api_key=args.api_key)

    if args.list_devices:
        list_devices(pushbullet)

    elif args.device:
        if args.type == 'note':
            response = push_note(args, pushbullet)

        elif args.type == 'link':
            response = push_link(args, pushbullet)

        elif args.type == 'address':
            response = push_address(args, pushbullet)

        elif args.type == 'list':
            response = push_list(args, pushbullet)

        elif args.type == 'file':
            response = push_file(args, pushbullet)

        if response.get('error', None):
            puts(response['error']['message'])
