import sys
import argparse
from typing import Tuple
import requests
from bs4 import BeautifulSoup
import subprocess

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print('it a comand line utility to manage wordlist from other servers\n-h for more help')
        sys.exit()
    argparser = argparse.ArgumentParser(
        description='Set wallet on auto craking')
    argparser.add_argument('--location', type=str,
                           help='WebServer for all files to download', required=True)
    argparser.add_argument('--host', type=str,
                           help='WebServer for all files to download', required=True)
    argparser.add_argument('--output', type=str,
                           help='WebServer for all files to download')
    argparser.add_argument('--clean', type=str,
                           help='clean for all wordlist if no folder specified\n all for all wordlist')
    argparser.add_argument('--delete', type=str,
                           help='delete wordlist from a specific folder')
    args = argparser.parse_args()
    location = str(args.location)
    host = args.host
    output = args.output
    clean = args.clean
    delete = args.delete
    if(clean is not None):
        if(clean == 'all'):
            subprocess.run('rm -rf wordlist/*', shell=True)
            print('All wordlist has been deleted')
        else:
            subprocess.run(f'rm -rf wordlist/{clean}/*', shell=True)
        sys.exit()
    if(delete is not None):
        subprocess.run(f'rm {delete}', shell=True)
        print(f'{delete} has been deleted successfully')
        sys.exit()
    if(output is not None):
        folder = output
    else:
        folder = location.split('/')
        folder = folder[len(folder) - 1]
    url = f'http://{host}/{location}/'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        urls.append(link.get('href'))
    included_extensions = ['txt']
    file_names = [fn for fn in urls
                  if any(fn.endswith(ext) for ext in included_extensions)]
    subprocess.run(f'mkdir wordlist/{folder}', shell=True)
    for file in file_names:
        print(f'Downloading {file}...')
        command = f'wget http://{host}/{location}/{file} -o wordlist/{folder}/{file}'
        subprocess.run('command', shell=True)
    print('All files are reterived from server')
    sys.exit()
