# yahoo_roster_extract
use yahoo's fantasy API to download fantasy team / roster data

## auth
authenticating against the yahoo api is quite easy using the [yahoo_oauth](https://github.com/josuebrunel/yahoo-oauth) package.  my understanding is that yahoo no longer supports OAuth 1 flow - you'll need to use OAuth2, and `https` requests for all resources.

## querying the API
`query.py` is what I threw together to pull down 9 years worth of roster data for my league.  the league [keys](https://github.com/almartin82/yahoo_roster_extract/blob/31b72673b6982d173b5968f8c2a991aa4c47e955/query.py#L51) are specific to our leagues, but that dictionary of gameids is generic for fantasy baseball.  might be useful given that the official yahoo documentation doesn't have those ids [after 2012.](https://developer.yahoo.com/fantasysports/guide/#game-resource) 