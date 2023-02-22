"module to download files from links"
import json
import os
import sys
from time import sleep

import requests

with open('config.json',encoding='UTF-8') as f:
    config=json.load(f)

silent_mode=config['silent-mode']
debug_mode=config['debug-mode']
rate_limit=config['rate-limit']
path=config['path']

filenames=[]

class Download():
    "Downloads files from urls"
    def __init__(self,urls: list):
        if urls=='':
            if not silent_mode:
                print('No posts found')
                os.system('pause')
                print('exiting...')
            sys.exit()

        if not os.path.exists(path): #create folder if it does not exist
            os.makedirs(path)

        for i in urls:
            file_path=(os.path.join(path,self.removeprefix(i)))
            try:
                request=requests.get(i, stream=True,timeout=10)
            except ConnectionError as exc:
                raise ConnectionError('''Was unable to access file.
Check if the website is accessible using a browser.''') from exc
            if request.ok:
                if debug_mode:
                    print(f'Downloading "{i}" to "{file_path}"')
                elif not silent_mode:
                    print(i)
                with open(file_path, 'wb') as file:
                    for chunk in request.iter_content(chunk_size=1024 * 8):
                        if chunk:
                            file.write(chunk)
                            file.flush()
                            os.fsync(file.fileno())
            else:
                print(f"Download failed: status code {request.status_code}\n{request.text}")
            if debug_mode:
                print(f'Sleeping for {rate_limit} second...')
            sleep(rate_limit)

    def removeprefix(self,item):
        "Removes domain and directory from url"
        filename=item[36:]
        return filename
