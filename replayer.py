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
parser.add_argument(
    '--host',
    help='host to send requests',
    default='localhost',
)
parser.add_argument(
    '--dry-run',
    action='store_true',
    help='don\'t actually hit the `host`',
)

script_args = parser.parse_args()

def replay_request(url):
    if script_args.dry_run:
        sys.stdout.write('{}\n'.format(url))
    else:
        requests.get(url)

def main():
    starting = None
    for line in open(script_args.logfile):
        bits = line.split()
        timestamp = dateutil.parser.parse(bits[0])
        if not starting:
            starting=timestamp
        offset = timestamp - starting
        if offset.total_seconds() < 0:
            # ignore past requests
            continue
        method = bits[11].lstrip('"')
        url = urlparse(bits[12])
        if method != 'GET':
            continue
        request_path = 'http://{}{}{}'.format(
            script_args.host,
            url.path,
            url.query
        )
        reactor.callLater(offset.total_seconds(), replay_request, request_path)

    reactor.callLater(offset.total_seconds() + 4, reactor.stop)
    reactor.run()

if __name__ == "__main__":
    main()
