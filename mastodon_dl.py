#!/usr/bin/env python3

import argparse
from mastodon import Mastodon
import os
import requests


def main():
    args = parse_args()
    mastodon = init_mastodon(
        args.email,
        args.password,
        args.secret_file,
        args.api_base_url
    )

    if args.account is not None:
        timeline = timeline_from_username(
            args.account,
            max_id=args.max_id,
            since_id=args.since_id,
            limit=args.limit,
            mastodon=mastodon
        )
    else:
        timeline = mastodon.timeline(
            timeline=args.timeline,
            max_id=args.max_id,
            since_id=args.since_id,
            limit=args.limit
        )

    page = timeline
    while page is not None:
        process_page(page, args.output_dir)
        page = mastodon.fetch_next(page)

    print('Done!')


def parse_args():
    parser = argparse.ArgumentParser(description='Download media from a Mastodon feed.')
    parser.add_argument('account', help='(Optional) Username to look up. '
                                        'If unspecified, use timeline instead.')
    parser.add_argument('-o', '--output-dir',
                        default=os.path.join(os.curdir, 'downloads'),
                        help='Directory to save files')
    parser.add_argument('-u', '--email', help='Email address for login')
    parser.add_argument('-p', '--password', help='Password for login')
    parser.add_argument('-s', '--secret-file', help='Path to API client secret file')
    parser.add_argument('--api-base-url', default='https://mastodon.social',
                        help='URL for Mastodon instance where client is registered')
    parser.add_argument('--timeline', default='home',
                        help='home, local, public, or hashtag')
    parser.add_argument('--max-id', type=int, help='Latest status ID to fetch')
    parser.add_argument('--since-id', type=int, help='Oldest status ID to fetch')
    parser.add_argument('--limit', type=int, help='Maximum number of statuses to fetch')
    return parser.parse_args()


def init_mastodon(email, password, client_secret, api_base_url):
    mastodon = Mastodon(
        client_id=client_secret,
        api_base_url=api_base_url,
        ratelimit_method='pace'
    )
    mastodon.log_in(
        email,
        password=password
    )
    return mastodon


def timeline_from_username(username, max_id, since_id, limit, mastodon):
    users = mastodon.account_search(username)
    if users is not None and len(users) > 0:
        return mastodon.account_statuses(
            users[0]['id'],
            max_id=max_id,
            since_id=since_id,
            limit=limit
        )
    else:
        return None


def process_page(page, output_dir):
    for toot in page:
        media_attachments = toot['media_attachments']
        if media_attachments is not None:
            for media_attachment in media_attachments:
                url = media_attachment['url']
                remote_url = media_attachment['remote_url']

                if remote_url is not None:
                    out_filename = os.path.basename(remote_url)
                else:
                    out_filename = os.path.basename(url)

                os.makedirs(output_dir, exist_ok=True)

                out_path = os.path.join(output_dir, out_filename)
                if os.path.exists(out_path):
                    print('Skipping %s -- %s exists' % (url, out_path))
                else:
                    stream_to_file(url, out_path)


def stream_to_file(url, out_path):
    """
    Download to a file.
    http://docs.python-requests.org/en/master/user/quickstart/#raw-response-content
    :param url: URL to download
    :param out_path: Path to output file.
    """
    with requests.get(url, stream=True) as r:
        try:
            with open(out_path, 'wb') as fd:
                for chunk in r.iter_content(chunk_size=128):
                    fd.write(chunk)
            print('Downloaded %s to %s' % (url, out_path))
        except KeyboardInterrupt:
            print('Error downloading %s to %s' % (url, out_path))
            os.remove(out_path)


if __name__ == '__main__':
    main()
