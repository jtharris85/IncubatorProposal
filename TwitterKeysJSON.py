#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

# create a dictionary to store your twitter credentials

twitter_cred = dict()

# Enter your own consumer_key, consumer_secret, access_key and access_secret
# Replacing the stars ("********")

twitter_cred['CONSUMER_KEY'] = 'dDdJrXAyHqypC7gDSes2cj2iN'
twitter_cred['CONSUMER_SECRET'] = 'aeiBVfVWeeQ5wGKqAo2wWTbcNo3CxxYR0e6o3494GfYnxrvbqq'
twitter_cred['ACCESS_KEY'] = '1254999889-dkgXKeqKfG8baje4KDYWYcm1EprUtntJ97s6OuC'
twitter_cred['ACCESS_SECRET'] = 'FeQpps1lOO6xaPjafMp60w5Ms7AdL52TpAg9hohcGvcT9'

# Save the information to a json so that it can be reused in code without exposing
# the secret info to public

with open('twitter_credentials.json', 'w') as secret_info:
    json.dump(twitter_cred, secret_info, indent=4, sort_keys=True)
