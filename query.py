import auth
import csv
import datetime

csv.register_dialect('ALM', delimiter=',', quoting=csv.QUOTE_ALL)

y = auth.yahoo_session()

def make_league_code(gameid, leagueid):
    return str(gameid) + '.l.' + str(leagueid)

def make_team_code(gameid, leagueid, teamid):
    return str(gameid) + '.l.' + str(leagueid) + '.t.' + str(teamid)

def league_data(league_code):
    return "http://fantasysports.yahooapis.com/fantasy/v2/league/" + league_code

def team_data(team_code):
    return "http://fantasysports.yahooapis.com/fantasy/v2/team/" + team_code

def roster_data(team_code, date_wanted):
    return "http://fantasysports.yahooapis.com/fantasy/v2/team/" + team_code + "/roster;date=" + date_wanted.isoformat()


hpk = [
    #2014
    {'gameid': 328, 'leagueid': 69518},
    #2013
    {'gameid': 308, 'leagueid': 54481},
    #2012
    {'gameid': 268, 'leagueid': 14615},
    #2011
    {'gameid': 253, 'leagueid': 27468},
    #2010
    {'gameid': 238, 'leagueid': 432962},
    #2009
    {'gameid': 215, 'leagueid': 67870},
    #2008
    {'gameid': 195, 'leagueid': 168490},
    #2007 (we were 'pro' this year
    {'gameid': 172, 'leagueid': 5643},
    #2006
    {'gameid': 147, 'leagueid': 72277},
    #2005
    {'gameid': 113, 'leagueid': 58563}
]

leagues = []
teams = []
rosters = []

for i in hpk:
    #get league data
    league_code = make_league_code(i['gameid'], i['leagueid'])
    l = auth.api_query(y, league_data(league_code))
    #grab relevant part of dict
    this_league = l['fantasy_content']['league']
    leagues.append(this_league)
    last_day = datetime.datetime.strptime(this_league['end_date'], "%Y-%m-%d")
    #go one beyond last day to make sure you get all the roster moves.
    last_day = last_day + datetime.timedelta(days=1)

    #iterate over teams
    num_teams = int(this_league['num_teams'])
    for j in range(1, num_teams + 1):
        #get basic team data
        team_code = make_team_code(i['gameid'], i['leagueid'], j)
        t = auth.api_query(y, team_data(team_code))
        #just relevant response
        this_team = t['fantasy_content']['team']
        #include season in dict
        this_team['season'] = this_league['season']
        this_team['logo'] = this_team['team_logos']['team_logo']['url']

        #handle co-managers
        this_manager = this_team['managers']['manager']
        if type(this_manager) == list:
            this_manager = this_manager[0]

        this_team['manager_id'] = this_manager['manager_id']

        this_team['manager_nickname'] = this_manager['nickname']
        if 'guid' in this_manager: manager_guid = this_manager['guid']
        if 'guid' not in this_manager: manager_guid = None
        this_team['manager_guid'] = manager_guid
        if 'email' in this_manager: manager_email = this_manager['email']
        if 'email' not in this_manager: manager_email = None
        this_team['manager_email'] = manager_email
        if "is_owned_by_current_login" not in this_team: this_team["is_owned_by_current_login"] = None
        #drop some keys
        this_team.pop("managers", None)
        this_team.pop("team_logos", None)
        this_team.pop("roster_adds", None)

        print str(this_manager['nickname'])
        teams.append(this_team)

        #get team roster
        r = auth.api_query(y, roster_data(team_code, last_day))
        this_roster = r['fantasy_content']['team']['roster']['players']['player']
        for k in this_roster:
            k['owner_email'] = manager_email
            k['owner_guid'] = manager_guid
            k['team_code'] = team_code
            k['date_captured'] = last_day
            k['season'] = this_league['season']
            k['full_name'] = k['name']['full']
            k['first_name'] = k['name']['ascii_first']
            k['last_name'] = k['name']['ascii_last']
            k['image_url'] = k['headshot']['url']
            k['eligible_positions'] = k['eligible_positions']['position']
            k['selected_position'] = k['selected_position']['position']
            if "status" not in k: k["status"] = None
            if "starting_status" not in k: k["starting_status"] = None
            if "has_player_notes" not in k: k["has_player_notes"] = None
            if "has_recent_player_notes" not in k: k["has_recent_player_notes"] = None
            if "on_disabled_list" not in k: k["on_disabled_list"] = None
            if "is_editable" not in k: k["is_editable"] = None
            k.pop("headshot", None)
            k.pop("name", None)
            k.pop("editorial_player_key", None)
            k.pop("editorial_team_key", None)
            rosters.append(k)

#write data
auth.data_to_csv(
    target_dir="data",
    data_to_write=leagues,
    desired_name='leagues'
)

auth.data_to_csv(
    target_dir="data",
    data_to_write=teams,
    desired_name='teams'
)

data_to_csv(
    target_dir="data",
    data_to_write=rosters,
    desired_name='rosters'
)