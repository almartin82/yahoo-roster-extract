# yahoo_roster_extract
use yahoo's fantasy API to download fantasy team / roster data

## auth
python support for yahoo oauth is...bad.  there's an [abandoned](https://github.com/project-fondue) github implementation which is pretty far and away the most robust, but uses older python libraries like urllib and httplib, not requests.  then there's the official yahoo [SDK](https://github.com/yahoo/yos-social-python), which has had two commits in the past six years.  right.  as for the actualy API documentation itself, well, it's [current](https://developer.yahoo.com/fantasysports/guide/#game-resource) as of 2012.

so the state of the state is not good.  I was able to get the OAuth flow up and [running](https://github.com/almartin82/yahoo_roster_extract/blob/31b72673b6982d173b5968f8c2a991aa4c47e955/auth.py) using `requests-oauthlib`; the [documentation](https://requests-oauthlib.readthedocs.org/en/latest/) there is really nice.

one wrinkle about yahoo's oauth 1.0 implementation is that tokens expire after 60 minutes.  the above, abandoned python wrapper had a refresh method, and the [documentation](https://developer.yahoo.com/oauth/guide/oauth-refreshaccesstoken.html) itself doesn't seem so bad, but I don't have any support for refreshing a token in [auth.py](https://github.com/almartin82/yahoo_roster_extract/blob/master/auth.py) yet.  when you complete oauth flow the tokens are saved to a file called `auth.yml`, and you won't have to do anything for an hour.  if you delete `auth.yml` you'll be prompted to complete oauth again when you make another call to `api_query`.  not ideal, but certainly enough to grab some data off of the API.

## querying the API
`query.py` is what I threw together to pull down 9 years worth of roster data for my league.  the league [keys](https://github.com/almartin82/yahoo_roster_extract/blob/31b72673b6982d173b5968f8c2a991aa4c47e955/query.py#L51) are specific to our leagues, but that dictionary of gameids is generic for fantasy baseball.  might be useful given that the official yahoo documentation doesn't have those ids [after 2012.](https://developer.yahoo.com/fantasysports/guide/#game-resource) 