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