#!/usr/bin/env python3

import argparse
from mastodon import Mastodon


def main():
    args = parse_args()
    # mastodon = init_mastodon(
    #     args.email,
    #     args.password,
    #     args.client_secret,
    #     args.api_base_url
    # )
    print(args)


def parse_args():
    parser = argparse.ArgumentParser(description='Download media from a Mastodon feed.')
    parser.add_argument('-u', '--email', help='Email address for login')
    parser.add_argument('-p', '--password', help='Password for login')
    parser.add_argument('-s', '--secret-file', help='Path to API client secret file')
    parser.add_argument('--api-base-url', default='https://mastodon.social',
                        help='URL for Mastodon instance where client is registered')
    return parser.parse_args()


def init_mastodon(email, password, client_secret, api_base_url):
    mastodon = Mastodon(
        client_id=client_secret,
        api_base_url=api_base_url
    )
    mastodon.log_in(
        email,
        password=password
    )
    return mastodon


def register_app():
    """
    Mastodon.create_app(
        'example',
        api_base_url='https://mastodon.social',
        to_file='example-clientcred.secret'
    )
    """


if __name__ == '__main__':
    main()
