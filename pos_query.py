import auth
import data_prep
import csv
import pandas as pd

csv.register_dialect('ALM', delimiter=',', quoting=csv.QUOTE_ALL)

#yahoo session
y = auth.yahoo_session()

prev_auction = pd.read_csv('input/2014_auctioned_players.csv')
query = data_prep.basic_player_req(prev_auction['player_key'])

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

#write data
auth.data_to_csv(
    target_dir="data",
    data_to_write=player_pos,
    desired_name='2014_auction_pos'
)