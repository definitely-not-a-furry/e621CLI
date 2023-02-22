"Bulk download files from e621.net"
import json
import os
import platform
import sys

import requests

import download

if len(sys.argv) > 1:
    print('Usage: e621.exe <tags seperated by "+"> <amount (max 320)>')
    sys.exit()

TAGS = sys.argv[1]
AMOUNT = sys.argv[2]

with open('config.json',encoding='UTF-8') as f:
    config=json.load(f)

header_name=config['header-name']
header_version=config['header-version']
username=config['username']

if config['clear-terminal']:
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

URL=f"https://e621.net/posts.json?tags={TAGS}&limit={AMOUNT}"
headers={'User-Agent': f'{header_name}/{header_version} (by {username})'}
if config['debug-mode']:
    print(f'url: {URL}')
    print(f'headers: {headers}')

request=requests.get(URL, headers=headers, timeout=10)

if os.path.exists('tmp\\posts.json'):
    os.system('del tmp\\posts.json')

if not config['silent-mode'] or config['debug-mode']:
    print(request)

request=request.json()

with open('tmp\\posts.json','w',encoding='UTF-8') as f:
    json.dump(request, f)

with open('tmp\\posts.json',encoding='UTF-8') as f:
    posts=json.load(f)

links=[]

for i in posts['posts']:
    links.append(i['file']['url'])
    if config['debug-mode'] is True:
        print(i['file']['url'])

if config['debug-mode']:
    print(f'Links: {str(links)}')

download.Download(links)
