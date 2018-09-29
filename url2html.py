# -*- coding: UTF-8 -*-

import requests
import os
import sys
import argparse
import pdb
from readability import Document
from subprocess import call

def saveHTML(url, prefix=''):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:10.0) Gecko/20100101 Firefox/10.0'}
    response = requests.get(url, headers=headers)
    doc = Document(response.text)
    filename = os.path.join(prefix, doc.title().encode('utf-8') + '.html')
    with open(filename, 'w') as f:
        f.write(doc.summary().encode('utf-8'))
    return filename

def html2mobi(filename):
    call(["./kindlegen", filename])

def main(args):
    html_file = saveHTML(args.url, args.prefix)
    if args.mobi:
        html2mobi(html_file)

if __name__ == '__main__':
    parsers = argparse.ArgumentParser(
        description = "send local file to kindle",
        formatter_class=argparse.RawTextHelpFormatter)

    parsers.add_argument('--url', help = "url you want to save.")
    parsers.add_argument('--prefix', default='', help = "output prefix dir.")
    parsers.add_argument('--mobi', action="store_true", default=False, help = "convert to mobi or not.")
    parsers.set_defaults(func=main)

    argslist = sys.argv[1:]
    if len(argslist) > 0:
        args = parsers.parse_args(argslist)
        args.func(args)
    else:
        parsers.print_help()
        os._exit(0)
