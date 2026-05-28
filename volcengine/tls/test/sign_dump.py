# coding: utf-8
"""Dump SignerV4 deterministic signing output for the shared fixture.

Pure offline: builds a SignParam with a fixed date and writes the resulting
Authorization header (and related signed-headers metadata) to disk. No HTTP
request is sent.
"""
import datetime
import json
import os
import sys
import tempfile
from collections import OrderedDict

# Allow running as a plain script: ensure repo root is on sys.path.
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

FIXTURE_RELATIVE_PATH = (
    'cospec/changes/check-tls-sdk-contract-alignment/context/l4-snapshots/fixture.json'
)


def resolve_fixture_path(fixture_path=None, start_dir=None):
    fixture_path = fixture_path or os.environ.get('SIGN_FIXTURE_PATH') or os.environ.get('L4_FIXTURE_PATH')
    if fixture_path:
        return os.path.abspath(fixture_path)

    current = os.path.abspath(start_dir or os.getcwd())
    while True:
        candidate = os.path.join(current, FIXTURE_RELATIVE_PATH)
        if os.path.exists(candidate):
            return candidate
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent


def resolve_output_path(out_dir=None):
    out_dir = out_dir or os.environ.get('SIGN_OUT_DIR') or os.environ.get('L4_OUT_DIR')
    if not out_dir:
        out_dir = tempfile.mkdtemp(prefix='sign-dump-python-')
    else:
        out_dir = os.path.abspath(out_dir)
        os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, 'sign-python.txt')


def main():
    fixture_path = resolve_fixture_path()
    if not fixture_path or not os.path.exists(fixture_path):
        sys.stderr.write('sign fixture not found; set SIGN_FIXTURE_PATH to run dump\n')
        return 0

    from volcengine.Credentials import Credentials
    from volcengine.auth.SignParam import SignParam
    from volcengine.auth.SignerV4 import SignerV4

    with open(fixture_path, 'r') as f:
        fixture = json.load(f)

    body = fixture['body']
    if isinstance(body, str):
        body = body.encode('utf-8')

    query = OrderedDict()
    for key in sorted(fixture['query'].keys()):
        query[key] = fixture['query'][key]

    headers = OrderedDict()
    headers['Content-Type'] = fixture['content_type']
    headers['Host'] = fixture['host']

    param = SignParam()
    param.is_sign_url = False
    param.method = fixture['method']
    param.host = fixture['host']
    param.path = fixture['path']
    param.body = body
    param.query = query
    param.header_list = headers
    param.date = datetime.datetime.strptime(fixture['x_date'], '%Y%m%dT%H%M%SZ')

    credentials = Credentials(
        ak=fixture['ak'],
        sk=fixture['sk'],
        service=fixture['service'],
        region=fixture['region'],
        session_token='',
    )

    result = SignerV4.sign_only(param, credentials)

    lines = [
        'Authorization: %s' % result.authorization,
        'ContentType: %s' % headers.get('Content-Type', ''),
        'Host: %s' % param.host,
        'XContentSha256: %s' % result.xContextSha256,
        'XDate: %s' % result.xdate,
        '',
    ]
    output_path = resolve_output_path()
    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))

    sys.stdout.write('\n'.join(lines))
    sys.stdout.write('Output: %s\n' % output_path)
    return 0


if __name__ == '__main__':
    sys.exit(main())
