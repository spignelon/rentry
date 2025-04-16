#!/usr/bin/env python3

import getopt
import sys
import urllib.parse
from os import environ
import json
from . import client

def usage():
    print('''
Usage: rentry {new | edit | raw | fetch | delete} [options] [text]

Commands:
  new     create a new entry
  edit    edit an existing entry
  raw     get raw markdown text of an existing entry
  fetch   fetch details about an entry
  delete  delete an entry
    
Options:
  -h, --help                 show this help message and exit
  -u, --url URL              url for the entry, random if not specified
  -p, --edit-code EDIT-CODE  edit code for the entry, random if not specified
  -m, --metadata METADATA    metadata for the entry (new/edit)
  -a, --auth AUTH            authentication header for raw endpoint
    
Examples:
  rentry new 'markdown text'               # new entry with random url and edit code
  rentry new -p pw -u example 'text'       # with custom edit code and url 
  rentry edit -p pw -u example 'text'      # edit the example entry
  cat FILE | rentry new                    # read from FILE and paste it to rentry
  cat FILE | rentry edit -p pw -u example  # read from FILE and edit the example entry
  rentry raw -u example                    # get raw markdown text
  rentry raw -u https://rentry.co/example  # -u accepts absolute and relative urls
  rentry fetch -u example -p pw            # fetch all details about an entry
  rentry delete -u example -p pw           # delete an entry
    ''')

def main():
    try:
        environ.pop('POSIXLY_CORRECT', None)
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hu:p:m:a:", ["help", "url=", "edit-code=", "metadata=", "auth="])
    except getopt.GetoptError as e:
        sys.exit(f"error: {e}")

    command, url, edit_code, text, metadata, auth = None, '', '', None, '', ''

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-u", "--url"):
            url = urllib.parse.urlparse(a).path.strip('/')
        elif o in ("-p", "--edit-code"):
            edit_code = a
        elif o in ("-m", "--metadata"):
            metadata = a
        elif o in ("-a", "--auth"):
            auth = a

    command = (args[0:1] or [None])[0]
    if not command:
        usage()
        sys.exit(1)
        
    valid_commands = ['new', 'edit', 'raw', 'fetch', 'delete']
    if command not in valid_commands:
        sys.exit(f'error: command must be one of: {", ".join(valid_commands)}')

    # Get text from arguments or stdin
    text = (args[1:2] or [None])[0]
    if not text and command in ['new', 'edit']:
        text = sys.stdin.read().strip()
        if not text:
            sys.exit('error: text is required')

    try:
        if command == 'new':
            response = client.new(text, url, edit_code, metadata)
            if response['status'] != '200':
                handle_error(response)
            else:
                print(f'Url:        {response["url"]}')
                print(f'Edit code:  {response["edit_code"]}')

        elif command == 'edit':
            if not url:
                sys.exit('error: url is required')
            if not edit_code:
                sys.exit('error: edit code is required')

            response = client.edit(url, edit_code, text, metadata)
            if response['status'] != '200':
                handle_error(response)
            else:
                print('Ok')

        elif command == 'raw':
            if not url:
                sys.exit('error: url is required')
            response = client.raw(url, auth)
            if response['status'] != '200':
                sys.exit(f'error: {response["content"]}')
            print(response['content'])

        elif command == 'fetch':
            if not url:
                sys.exit('error: url is required')
            if not edit_code:
                sys.exit('error: edit code is required')
            
            response = client.fetch(url, edit_code)
            if response['status'] != '200':
                handle_error(response)
            else:
                print(json.dumps(response['content'], indent=2))

        elif command == 'delete':
            if not url:
                sys.exit('error: url is required')
            if not edit_code:
                sys.exit('error: edit code is required')
            
            response = client.delete(url, edit_code)
            if response['status'] != '200':
                handle_error(response)
            else:
                print('Entry deleted successfully')

    except Exception as e:
        sys.exit(f"Error: {str(e)}")

def handle_error(response):
    print(f'error: {response["content"]}')
    try:
        for i in response['errors'].split('.'):
            if i:
                print(i)
        sys.exit(1)
    except:
        sys.exit(1)

if __name__ == '__main__':
    main()
