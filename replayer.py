#!/usr/bin/env python
import argparse
import sys

import dateutil.parser
import requests
from urlparse import urlparse

from twisted.internet import task
from twisted.internet import reactor

description='ELB Log Replayer (ELR)'

parser = argparse.ArgumentParser(description=description)
parser.add_argument('logfile', help='the logfile to replay')
parser.add_argument('--host',
                    help='host to send requests',
                    default='localhost',
                )

script_args = parser.parse_args()

def replay_request(url):
    requests.get(url)

def main():
    for line in open(script_args.logfile):
        bits = line.split()
        timestamp = dateutil.parser.parse(bits[0])
        method = bits[11].lstrip('"')
        url = urlparse(bits[12])
        if method != 'GET':
            continue
        request_path = 'http://{}{}{}'.format(
            script_args.host,
            url.path,
            url.query
        )


if __name__ == "__main__":
    main()
