import yaml
import requests_oauthlib
import requests
import urlparse
import os.path
import xmltodict
import oauth2
from httplib2 import Http

#read in credentials
with open("credentials.yml", 'r') as ymlfile:
    creds = yaml.load(ymlfile)

key = creds['consumer_key']
secret = creds['consumer_secret']

#yahoo OAuth URLs
request_token_url = 'https://api.login.yahoo.com/oauth/v2/get_request_token'
authorization_base_url = 'https://api.login.yahoo.com/oauth/v2/request_auth'
access_token_url = 'https://api.login.yahoo.com/oauth/v2/get_token'
callback = 'oob'

def user_auth():
    #make the initial oauth call
    oauth = requests_oauthlib.OAuth1(key, client_secret=secret, callback_uri=callback)
    r = requests.post(url=request_token_url, auth=oauth)

    #parse the response
    response = urlparse.parse_qs(r.content)
    owner_key = response.get('oauth_token')[0]
    owner_secret = response.get('oauth_token_secret')[0]

    #get the verification code (interactive)
    authorize_url = authorization_base_url + '?oauth_token='
    authorize_url = authorize_url + owner_key
    print 'Please go here and authorize,', authorize_url
    verifier = raw_input('Please input the verifier, ')

    #get the final token
    oauth = requests_oauthlib.OAuth1Session(key, client_secret=secret,
        resource_owner_key=owner_key, resource_owner_secret=owner_secret, verifier=verifier)

    #write response to yaml
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    with open('auth.yml', 'w') as outfile:
        outfile.write(yaml.dump(oauth_tokens))

def session_from_auth(auth_dict):
    #print oauth_tokens
    res_owner_key = auth_dict['oauth_token']
    res_owner_secret  = auth_dict['oauth_token_secret']
    return requests_oauthlib.OAuth1Session(
        key,
        client_secret=secret,
        resource_owner_key=res_owner_key,
        resource_owner_secret=res_owner_secret
    )

def read_stored_auth():
    with open("auth.yml", 'r') as ymlfile:
        final_auth = yaml.load(ymlfile)
    return final_auth


def test_stored_auth():
    return os.path.exists("auth.yml")


def yahoo_session():
    if(test_stored_auth()):
        return session_from_auth(read_stored_auth())
    else:
        user_auth()
        return session_from_auth(read_stored_auth())

def api_query(y_session, query):
    r = y_session.get(query)
    return xmltodict.parse(r.content)
