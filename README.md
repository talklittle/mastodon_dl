Mastodon_dl
===========

Download media from [Mastodon](https://github.com/tootsuite/mastodon).

Built using [Mastodon.py](https://github.com/halcy/Mastodon.py).


Usage
-------

1. Clone this repo
2. Install [pipenv](https://docs.pipenv.org/) if not yet installed
3. `cd mastodon_dl`
4. Register a Mastodon API client
    1. `pipenv run python3`
    2. Call `Mastodon.create_app()` with arguments as described at https://mastodonpy.readthedocs.io/en/latest/#app-registration-and-user-authentication
5. `pipenv run python3 mastodon_dl.py --email YOUREMAIL@EXAMPLE.COM --password YOURPASS --secret-file PATH/TO/CLIENTCRED.SECRET`

Run `pipenv run python3 mastodon_dl.py -h` for more command line arguments.

Use `--api-base-url` to point to your Mastodon instance. Defaults to `https://mastodon.social`.


License
-------

[MIT License](LICENSE).