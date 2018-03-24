import xmltodict
import time
import os
from collections import OrderedDict
import unicodecsv
from yahoo_oauth import OAuth2

def yahoo_session():
    #use yahoo_oauth library to authenticate via oauth 2.0
    #note that yahoo (apparently) no longer supports oauth 1.0
    oauth = OAuth2(None, None, from_file='oauth2.json')
    if not oauth.token_is_valid():
        oauth.refresh_access_token()
    return oauth

def api_query(y_session, query):
    r = y_session.session.get(query)
    time.sleep(2)
    if (r.status_code >= 500):
        print('bad response from yahoo: status code {0}.  retrying...'.format(r.status_code))
        r = y_session.session.get(query)
    return xmltodict.parse(r.content)

def data_to_csv(target_dir, data_to_write, desired_name):
    """Convenience function to write a dict to CSV with appropriate parameters."""
    #generate directory if doesn't exist
    global d
    if len(data_to_write) == 0:
        return None
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    if type(data_to_write) == dict:
        #order dict by keys
        d = OrderedDict(sorted(data_to_write.items()))
        keys = d.keys()
    if type(data_to_write) == list:
        d = data_to_write
        keys = data_to_write[0].keys()
    with open("%s/%s.csv" % (target_dir, desired_name), 'wb') as f:
        dw = unicodecsv.DictWriter(f, keys, dialect='ALM', extrasaction='ignore')
        dw.writeheader()
        if type(data_to_write) == dict:
            dw.writerow(d)
        if type(data_to_write) == list:
            dw.writerows(d)
    f.close()