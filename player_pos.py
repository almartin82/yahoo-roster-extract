import auth
import csv
import pandas as pd

csv.register_dialect('ALM', delimiter=',', quoting=csv.QUOTE_ALL)

#yahoo session
y = auth.yahoo_session()

def basic_player_req(playerid):
    return 'http://fantasysports.yahooapis.com/fantasy/v2/player/' + playerid

def process_player_dict(p):
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
    p.pop("has_recent_player_notes", None)
    p.pop("status", None)
    p.pop("on_disabled_list", None)
    return p

cur_yahoo = pd.read_csv('input/yahoo_players.csv')
query = basic_player_req(cur_yahoo['yahoo_code'])

yahoo_resp = []
player_pos = []

for i in range(0, len(query)):
    print query[i]
    p = auth.api_query(y, query[i])
    #some players dont exist in a given year.  skip them
    if 'error' in p.keys():
        continue
    #just player pos
    elig_pos = p['fantasy_content']['player']['eligible_positions']['position']
    playerid = p['fantasy_content']['player']['player_id']
    #if it's a string, not a list, make it a list
    if not hasattr(elig_pos, '__iter__'):
        elig_pos = [elig_pos]
    for j in range(0, len(elig_pos)):
        print j
        player_pos.append({'playerid': playerid, 'pos': elig_pos[j]})

    p_data = process_player_dict(p)
    yahoo_resp.append(p_data)

#write data
auth.data_to_csv(
    target_dir="data",
    data_to_write=yahoo_resp,
    desired_name='yahoo_cur_yr'
)

#write data
auth.data_to_csv(
    target_dir="data",
    data_to_write=player_pos,
    desired_name='player_pos'
)