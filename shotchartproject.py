from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leaguedashteamstats
from nba_api.stats.static import teams
import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from ipywidgets import interact_manual
from ipywidgets import widgets
import urllib.request
from PIL import Image
from IPython.display import display, HTML

def get_player_list():
    active_player_list = []
    active_players = players.get_active_players()
    for p in active_players:
        if p['full_name'] not in active_player_list:
            active_player_list.append(p['full_name'])
    return active_player_list
  
def get_player_id(nba_player):
    active_players = players.get_active_players()
    for p in active_players:
        if p['full_name'] == nba_player:
            p_id = p['id']
    return p_id

def get_team_id(nba_player, season, p_id):
    nba_career = playercareerstats.PlayerCareerStats(player_id=p_id)
    nba_career_df = nba_career.get_data_frames()[0]
    t_id = nba_career_df[nba_career_df['SEASON_ID'] == season]['TEAM_ID']
    return t_id

def getShotChartDetail(nba_player,season, p_id, t_id):
    shot_chart_stats = shotchartdetail.ShotChartDetail(player_id=p_id, team_id=t_id,season_nullable=season,
                                                   season_type_all_star='Regular Season',
                                                   context_measure_simple= 'FGA')
    shot_chart_df = shot_chart_stats.get_data_frames()[0]
    return shot_chart_df

def getActionList(shot_chart_df):
    action_list = shot_chart_df['ACTION_TYPE'].tolist()
    action_stat = {}
    for c in action_list:
        action_stat[c] = action_list.count(c)
        top_five = dict(list(sorted(action_stat.items(), 
                                    key=lambda x:x[1], reverse=True))[0:5])
     
    return top_five

def getTeamList():
    team = teams.get_teams()
    team_list = []
    for t in team:
        if t['full_name'] not in team_list:
            team_list.append(t['full_name'])
    return team_list
def getTeamLogo(nba_team):    
    url = "https://api-nba-v1.p.rapidapi.com/teams"

    headers = {
        "X-RapidAPI-Key": "8a7b792068msh1f8924af1a899a1p16b946jsn786aa3ea3473",
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    teams1 = response.json()
    return teams1
        
def getTeamID(nba_team):
    regex_pattern = nba_team
    team = teams.find_teams_by_full_name(regex_pattern)
    t_id2 = team[0]['id']
    return t_id2

def getTeamStats(season, nba_team,t_id2):
    team_stats = leaguedashteamstats.LeagueDashTeamStats(season=season, season_type_all_star= 'Regular Season', team_id_nullable=t_id2)
    team_stats_df = team_stats.get_data_frames()[0]
    new_team_stats_df = team_stats_df[['GP', 'W', 'L', 'W_PCT', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS']]
    FT = new_team_stats_df[['FTM', 'FTA']]
    FG3 = new_team_stats_df[['FG3M', 'FG3A']]
    FG=new_team_stats_df[['FGM','FGA' ]]
    team_dict = new_team_stats_df.to_dict('records')
    win_loss=new_team_stats_df[['W','L']]
    win_loss_n=win_loss.T
    return new_team_stats_df, FT, FG3, FG, team_dict, win_loss_n
def getTeamShotChart(nba_team, t_id2, season):
    team_shot_chart_stats = shotchartdetail.ShotChartDetail(player_id=0, team_id=t_id2,season_nullable=season,
                                                       season_type_all_star='Regular Season',
                                                       context_measure_simple= 'FGA')
    team_shot_chart_df = team_shot_chart_stats.get_data_frames()[0]
    return team_shot_chart_df

def getTeamTopFive(team_shot_chart_df, nba_team,t_id2 , season):
    team_action_list = team_shot_chart_df['ACTION_TYPE'].tolist()
    team_action_stat = {}
    for v in team_action_list:
        team_action_stat[v] = team_action_list.count(v)
        team_top_five = dict(list(sorted(team_action_stat.items(), 
                                    key=lambda x:x[1], reverse=True))[0:5])
    return team_top_five


season_list = ["1996-97",
            "1997-98",
            "1998-99",
            "1999-00",
            "2000-01",
            "2001-02",
            "2002-03",
            "2003-04",
            "2004-05",
            "2005-06",
            "2006-07",
            "2007-08",
            "2008-09",
            "2009-10",
            "2010-11",
            "2011-12",
            "2012-13",
            "2013-14",
            "2014-15",
            "2015-16",
            "2016-17",
            "2017-18",
            "2018-19",
            "2019-20",
            "2020-21",
            "2021-22"] 

display(HTML("<h1>NBA Season Statistics</h1>"))
print("Choose player or team.")

options = ['nba_team', 'nba_player']
@interact_manual(choice = options)
def main(choice):
    if choice == 'nba_player':
        print("Type in or click on a current player and season")
        active_player_list = get_player_list()
        @interact_manual(nba_player=widgets.Combobox(placeholder='Choose Someone',options=active_player_list, description='Combobox:'), season = widgets.Combobox(placeholder='Choose Season',options=season_list, description='Combobox:'))
        def main(nba_player, season):
            try:
                p_id = get_player_id(nba_player)
                t_id = get_team_id(nba_player, season, p_id)
                shot_chart_df = getShotChartDetail(nba_player,season, p_id, t_id)
                top_five = getActionList(shot_chart_df)
                display(HTML(f"<h1>{nba_player}</h1>"))
                print(f"Player Profile: https://www.nba.com/player/{p_id}")
                print('2022-21 Player Photo')
                urllib.request.urlretrieve(f"https://cdn.nba.com/headshots/nba/latest/1040x760/{p_id}.png",
                                           "headshots.png")
                img = Image.open("headshots.png")
                headshot = img.resize((208, 152))
                headshot.show()        

                urllib.request.urlretrieve('https://i.postimg.cc/0jjwmPws/halfcourt2.png',
                                           'halfcourt2.png')
                img = plt.imread('halfcourt2.png')
                plt.rcParams["figure.figsize"] = [10, 9.4]

                miss = shot_chart_df[shot_chart_df['SHOT_MADE_FLAG'] == 0]
                make = shot_chart_df[shot_chart_df['SHOT_MADE_FLAG'] == 1]

                ax = miss.plot(x='LOC_X', y='LOC_Y', kind='scatter', c='r', s=8, label='miss')
                make.plot(x='LOC_X', y='LOC_Y', kind='scatter', ax=ax, c='g', s=8, label = 'make')
                plt.title('Regular Season Shot Chart', fontsize = 20)
                ax.imshow(img, extent=[ -250, 250,422, -48 ])
                plt.legend()
                plt.show()

                names = list(top_five.keys())
                values = list(top_five.values())
                plt.rcParams["figure.figsize"] = [6, 5]
                plt.bar(np.arange(len(top_five)), height=values, tick_label=names, color = 'navy')
                plt.xticks( rotation=20, fontweight='bold', fontsize='11', horizontalalignment='right')
                plt.yticks( fontweight='bold', fontsize='8')
                plt.title('Five Most Shot Shot Types', fontsize=20)
                for l in range(len(top_five)):
                    plt.text(l,values[l], values[l], ha='center', bbox = dict(facecolor = 'orange', alpha=1))
                plt.show()

            except json.decoder.JSONDecodeError as e:
                print( f"Player was not active during this season. Try a more recent season. ({e})")

    elif choice == 'nba_team':
        print("Choose a team and season.")
        team_list = getTeamList()
        @interact_manual(nba_team=team_list, season = season_list)
        def main(nba_team, season):
               
                t_id2 = getTeamID(nba_team)
                teams1=getTeamLogo(nba_team)
                new_team_stats_df, FT, FG3, FG, team_dict, win_loss_n = getTeamStats(season, nba_team,t_id2)
                team_shot_chart_df = getTeamShotChart(nba_team, t_id2, season)
                team_top_five = getTeamTopFive(team_shot_chart_df, t_id2, nba_team, season)
                for k in teams1['response']:

                    if nba_team == k['name']:
                        team_logo = k['logo']    
                        urllib.request.urlretrieve(f"{team_logo}",
                                   "logo.png")
                        img2 = Image.open("logo.png")
                        newsize= (150,150)
                        logo = img2.resize(newsize) 

                        logo.show()
                        print(f"{nba_team} Stats Website Link: https://www.nba.com/stats/team/{t_id2}/traditional/?Season={season}&SeasonType=Regular%20Season&PerMode=Totals")
                        urllib.request.urlretrieve('https://i.postimg.cc/0jjwmPws/halfcourt2.png',
                           'halfcourt2.png')
                        img3 = plt.imread('halfcourt2.png')
                        miss2 = team_shot_chart_df[team_shot_chart_df['SHOT_MADE_FLAG'] == 0]
                        make2 = team_shot_chart_df[team_shot_chart_df['SHOT_MADE_FLAG'] == 1]
                        plt.rcParams["figure.figsize"] = [6.25, 5.875]

                        ax1 = miss2.plot(x='LOC_X', y='LOC_Y', kind='scatter', c='r', s=4, label='miss')
                        make2.plot(x='LOC_X', y='LOC_Y', kind='scatter', ax=ax1, c='g', s=4, label = 'make')
                        plt.title('Regular Season Shot Chart', fontsize = 10)
                        ax1.imshow(img3, extent=[ -250, 250,422, -48 ])
                        plt.legend()
                        plt.show()
                        plt.rcParams["figure.figsize"] = [6, 3]

                        names2 = list(team_top_five.keys())
                        values2 = list(team_top_five.values())
                        plt.rcParams["figure.figsize"] = [5, 3]
                        plt.bar(np.arange(len(team_top_five)), height=values2, tick_label=names2, color = 'navy')
                        plt.xticks( rotation=20, fontweight='bold', fontsize='11', horizontalalignment='right')
                        plt.yticks( fontweight='bold', fontsize='8')
                        plt.title('Five Most Shot Shot Types', fontsize=20)
                        for x in range(len(team_top_five)):
                            plt.text(x,values2[x], values2[x], ha='center', bbox = dict(facecolor = 'orange', alpha=1))
                        plt.show()


                        plt.rcParams["figure.figsize"] = [2, 2]
                        win_loss_n.plot.pie(y=0)
                        plt.title('Win Lose Stats', fontsize = 10)
                        print(f"Win Percentage: {team_dict[0]['W_PCT']}\nWin: {team_dict[0]['W']} Loss: {team_dict[0]['L']}")
                        plt.show()
                        plt.rcParams["figure.figsize"] = [6, 3]
                        fig, axs = plt.subplots(1, 3)
                        N=1
                        barWidth = 0.5
                        xloc = np.arange(N)
                        axs[0].bar(xloc, FG['FGM'], width=barWidth)
                        axs[0].bar(xloc, FG['FGA'], bottom= FG['FGM'], width=barWidth)
                        axs[0].set_title('Field Goal', fontsize = 10)
                        print(f"\nField Goal Percentage: {team_dict[0]['FG_PCT']}\nField Goal Attempt: {team_dict[0]['FGA']} - Field Goal Made: {team_dict[0]['FGM']}")

                        N2=1
                        barWidth = 0.5
                        xloc = np.arange(N2)
                        axs[1].bar(xloc, FG3['FG3M'], width=barWidth)
                        axs[1].bar(xloc, FG3['FG3A'], bottom= FG3['FG3M'], width=barWidth)
                        axs[1].set_title('3PT Field Goal', fontsize = 10)
                        print(f"\n3PT Field Goal Percentage: {team_dict[0]['FG3_PCT']}\n3PT Field Goal Attempt: {team_dict[0]['FG3A']} - 3PT Field Goal Made: {team_dict[0]['FG3M']}")
                        
                        N3=1
                        barWidth = 0.5
                        xloc = np.arange(N2)
                        axs[2].bar(xloc, FT['FTM'], width=barWidth)
                        axs[2].bar(xloc, FT['FTA'], bottom= FT['FTM'], width=barWidth)
                        axs[2].set_title('Free Throw', fontsize = 10)
                        fig.legend(['Made', 'Attempt'], loc=4)
                        print(f"\nFree Throw Percentage: {team_dict[0]['FT_PCT']}\nFree Throw Attempt: {team_dict[0]['FTA']} - Free Throw Made: {team_dict[0]['FTM']}")
                        plt.tight_layout()
                        plt.show()
                    
            
