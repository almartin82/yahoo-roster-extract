import auth
import csv
import pandas as pd

csv.register_dialect('ALM', delimiter=',', quoting=csv.QUOTE_ALL)

#yahoo session
y = auth.yahoo_session()

def basic_player_req(playerid):
    return 'http://fantasysports.yahooapis.com/fantasy/v2/player/' + playerid

players = pd.read_csv('input/auction_results.csv')
query = basic_player_req(players['yahoo_code'])

#list to store api data
player_data = []

#loop over players and look up data
for i in range(0, len(players)):
    p = auth.api_query(y, basic_player_req(players.iloc[i]['yahoo_code']))
    #some players dont exist in a given year.  skip them
    if 'error' in p.keys():
        print 'errored on:'
        print players.iloc[i]
        continue

    print players.iloc[i]['year']
    print p['fantasy_content']['player']['name']['full']

    #process the response and pull out some fields
    p = p['fantasy_content']['player']
    p['full_name'] = p['name']['full']
    p['first_name'] = p['name']['first']
    p['last_name'] = p['name']['last']
    p.pop('name', None)
    p['elig_positions'] = p['eligible_positions']['position']
    p.pop('eligible_positions', None)

    #these fields are inconsistent - don't need them
    p.pop("headshot", None)
    p.pop("position", None)
    p.pop("has_player_notes", None)
    p.pop("has_recent_player_notes", None)
    p.pop("status", None)
    p.pop("on_disabled_list", None)
    player_data.append(p)

#write data
auth.data_to_csv(
    target_dir="data",
    data_to_write=player_data,
    desired_name='player_data'
)
