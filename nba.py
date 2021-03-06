#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 16:41:22 2022

@author: William
"""

import pandas as pd 
import csv
import xlrd 
import os 
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches 
import seaborn as sns 

def excel_to_csv(): 
    wb = xlrd.open_workbook('/Users/William/Desktop/01-31-2022-nba-season-player-feed.xlsx')
    sh = wb.sheet_by_name('NBA-PLAYER-FEED')
    path = os.getcwd() 
    convert = path + '/Desktop/nba_player_feed.csv'
    csvFile = open(convert, 'w')
    wr = csv.writer(csvFile, quoting = csv.QUOTE_ALL)
    
    for rownum in range(sh.nrows): 
        wr.writerow(sh.row_values(rownum))
        
    csvFile.close() 
    
excel_to_csv() 

df = pd.read_csv('/Users/William/Desktop/nba_player_feed.csv')
df.info()
df.columns
''' ['BIGDATABALL\nDATASET', 'GAME-ID', 'DATE', 'PLAYER-ID',
       'PLAYER \nFULL NAME', 'POSITION', 'OWN \nTEAM', 'OPPONENT \nTEAM',
       'VENUE\n(R/H)', 'STARTER\n(Y/N)', 'MIN', 'FG', 'FGA', '3P', '3PA', 'FT',
       'FTA', 'OR', 'DR', 'TOT', 'A', 'PF', 'ST', 'TO', 'BL', 'PTS',
       'USAGE \nRATE (%)', 'DAYS\nREST'] '''
    
df.columns = ['dataset', 'game_id', 'date', 'player_id',
       'player', 'position', 'home_team', 'away_team',
       'venue', 'starter', 'minutes', 'field_goals', 'field_goals_attempts', '3_point', '3_point_attempts', 'free_throw',
       'free_throw_attempts', 'offensive_rebound', 'defensive_rebound', 'total_rebound', 'assists', 'personal_fouls', 'steals', 'turnovers',
       'blocks', 'points', 'usage_rate', 'days_rest']

#df['date'] = pd.to_datetime(df['date']).dt.date
df['date'] = pd.to_datetime(df['date']).dt.strftime('%m-%d-%Y')
df['date'].describe
df['date'].describe()

df.to_csv('/Users/William/Desktop/nba_player_feed.csv')

# Alternatively use pandas module to convert multiple sheets within an excel file into separate csv files 
# - passing `sheet_name=None` returns a dictionary 
# - with the form {sheet_name: dataframe}
data = pd.read_excel('file.xlsx', sheet_name=None)

# loop through the dictionary and save csv
for sheet_name, df in data.items():
    df.to_csv(f'{sheet_name}.csv')

# =============================================================================
# Questions to answer --> results were collected from WHOLE NUMBER ROUNDING
# 1. Which NBA player has the highest 3PT avg?
#       - Stephen Curry --> 5 per game 
# 2. Which NBA player has the lowest FG avg? 
#       - 73 NBA players; see dataframe --> 0 per game 
# 3. Which NBA player has the most rebounds? 
#       - Rudy Gobert --> 663 season rebounds; 15 per game 
# 4. Which NBA player has the least turnovers?
#       - 52 NBA players
# =============================================================================
# =============================================================================
# Steps to approach: 
#    - Find the total number of games each player played 
#    - Find the total count/sum of values per player 
#    - Find the average/min/max 
# =============================================================================

print('The total number of players within this masterlist is: ', df.player.nunique(), '.', sep ='')
print('The total number of games within this masterlist is: ', df.game_id.nunique(), '.', sep = '')
print('The total number of game days within this masterlist is: ', df.date.nunique(), '.', sep='')
print('The 5 most popular dates with the most games played are: \n', df.date.value_counts().head(5))
print('The top 5 players with the most games this NBA season: \n', df.player.value_counts().head(5))
df.columns

# =============================================================================
# Cleaning the initial dataframe into separate dataframes for analysis
# =============================================================================

player_games = df['player'].value_counts().reset_index()
player_games.columns = ['player', 'games_played']
threePts = df[['game_id', 'date', 'player', '3_point', '3_point_attempts']]
twoPts = df[['game_id', 'date', 'player', 'field_goals', 'field_goals_attempts']]
freePts = df[['game_id', 'date', 'player', 'free_throw', 'free_throw_attempts']]
rebound = df[['game_id', 'date', 'player', 'offensive_rebound', 'defensive_rebound', 'total_rebound']]
turnover = df[['game_id', 'date', 'player', 'turnovers']]

pd.options.mode.chained_assignment = None  # default='warn'

# =============================================================================
# Transforming threePts
# =============================================================================

threePts['accuracy'] = (threePts['3_point']/threePts['3_point_attempts'])
threePts['game_success_%'] = ((threePts['3_point']/threePts['3_point_attempts'])*100).round(2)
list(threePts.columns)
threePts.drop(['accuracy'], axis = 1, inplace= True)
threePts['game_success_%'].value_counts()
threePts['game_success_%'].describe()

# Sum up all the 3 points based on players to show seasonal performance by player 
cthreePts = threePts.groupby('player')[['3_point', '3_point_attempts']].sum() 
cthreePts['season_%'] = ((cthreePts['3_point']/cthreePts['3_point_attempts'])*100).round(2)
cthreePts = cthreePts.merge(player_games, how ='left', on='player')
cthreePts.columns
cthreePts['3_point_avg'] = (cthreePts['3_point']/cthreePts['games_played']).round(2)
cthreePts.rename(columns={'3_point':'cum_3_points', '3_point_attempts': 'cum_3_point_attempts'}, inplace=True)

cthreePts['3_point_avg'].describe()
cthreePts['season_%'].describe()

cthreePts.sort_values(by= '3_point_avg', ascending = False).head(1)

demo = cthreePts.sort_values(by='cum_3_points', ascending = False).head(5).reset_index()

# Single bar plot 
plt.figure(figsize=(10,5))
sns.set(style="darkgrid")
fig = sns.barplot(x='player', y='season_%', data=demo, color = 'lightblue')
plt.title('NBA 2021-2022 Top Five 3-Point Performance')
fig.set_xticklabels(fig.get_xticklabels(), rotation=0, horizontalalignment='center')
fig.set(xlabel='Player Name', ylabel='Seasonal Performance')
plt.show()

# Stacked bar plot
plt.figure(figsize=(10,5))
sns.set(style="darkgrid")
bar1 = sns.barplot(x='player', y='cum_3_point_attempts', data=demo, color = 'lightblue')
bar2 = sns.barplot(x='player', y='cum_3_points', data=demo, color = 'darkblue')
top_bar = mpatches.Patch(color= 'darkblue', label='3 Points Made')
bottom_bar = mpatches.Patch(color= 'lightblue', label='3 Points Attempts')
plt.legend(handles=[top_bar, bottom_bar])
plt.xlabel('Player Name')
plt.ylabel('3-Point Shots')
plt.title('NBA 2021-2022 Top Five 3-Point Performance')
plt.show()

demo.set_index('player').plot(kind='bar', stacked=True, color=['steelblue', 'red', 'cyan'])

# =============================================================================
# Transforming twoPts  
# =============================================================================
twoPts['game_success_%'] = ((twoPts['field_goals']/twoPts['field_goals_attempts'])*100).round(2)
list(twoPts.columns)
twoPts['game_success_%'].value_counts()
twoPts['game_success_%'].describe()

# Sum up all the 3 points based on players to show seasonal performance by player 
ctwoPts = twoPts.groupby('player')[['field_goals', 'field_goals_attempts']].sum().reset_index() 
ctwoPts['season_%'] = ((ctwoPts['field_goals']/ctwoPts['field_goals_attempts'])*100).round(2)
ctwoPts = ctwoPts.merge(player_games, how ='left', on='player')
ctwoPts.columns
ctwoPts['field_goal_avg'] = (ctwoPts['field_goals']/ctwoPts['games_played']).round(2)
ctwoPts.rename(columns={'field_goals':'cum_field_goals', 'field_goals_attempts': 'cum_field_goals_attempts'}, inplace=True)

ctwoPts['field_goal_avg'].describe()
ctwoPts['season_%'].describe()

ctwoPts[ctwoPts['season_%'] == 0]
len(ctwoPts[ctwoPts['season_%'] == 0])
ctwoPts.sort_values(by= 'field_goal_avg', ascending = True)
len(ctwoPts[ctwoPts['field_goal_avg'] == 0])
lowest = ctwoPts.loc[ctwoPts['field_goal_avg'] == 0]

demo2 = ctwoPts.sort_values(by='field_goal_avg', ascending = True).head(73).reset_index()

# =============================================================================
# Transforming rebounds 
# =============================================================================

crebound = rebound.groupby('player')[['total_rebound']].sum() 
crebound.sort_values(by='total_rebound', ascending = False).head(1)
crebound = crebound.merge(player_games, how= 'left', on= 'player')
crebound['rebound_avg'] = (crebound['total_rebound']/crebound['games_played']).round(2)
crebound.rename(columns={'total_rebound':'cum_rebound'}, inplace=True)

crebound['rebound_avg'].describe()
crebound['cum_rebound'].describe()

# =============================================================================
# Transforming turnovers 
# =============================================================================

cturnover = turnover.groupby('player')['turnovers'].sum().reset_index()
cturnover.sort_values(by='turnovers', ascending = True).head(52)
cturnover = cturnover.merge(player_games, how= 'left', on= 'player')
cturnover['turnover_avg'] = (cturnover['turnovers']/cturnover['games_played']).round(2)
cturnover.rename(columns={'turnovers':'cum_turnovers'}, inplace=True)

cturnover['turnover_avg'].describe()
cturnover['cum_turnovers'].describe()

len(cturnover[cturnover['cum_turnovers'] == 0])
len(cturnover[cturnover['turnover_avg'] == 0])

# =============================================================================
# Testing for-loop automation/iteration
# =============================================================================

data = ['Will', '123', 3, 10], ['Marin', '234', 5, 5], ['Hants', '345', 10, 11], ['Will', '765', 4, 4], ['Marin', '836', 4, 20], ['Hants', '169', 0, 2]
temp = pd.DataFrame(data, columns= ['player', 'game_id', 'free_throw', 'free_throw_attempts'])
temp['success_%'] = ((temp['free_throw']/temp['free_throw_attempts'])*100).round(2)
temp['total_games'] = temp.groupby(['player'])['free_throw'].transform('sum')
temp.drop(columns='total_games', axis =1, inplace = True)

temp2 = temp.groupby('player')['free_throw'].transform('sum').reset_index()
temp3 = temp.groupby('player')['free_throw_attempts'].transform('sum').reset_index()
temp4 = temp2.merge(temp3, how = 'left', on= 'index')

# Change data into an array (2 dimensional object)
data = [
    ["Will", "123", 3, 10, 0.3],
    ["Marin", "234", 5, 5, 1],
    ["Hants", "345", 10, 11, 0.91],
    ["Will", "765", 4, 4, 1],
    ["Marin", "836", 4, 20, 0.2],
    ["Hants", "169", 0, 2, 0],
]

# Pass the values into a dictionary 
# Iterate based on occurences 
player_dic = {}
for i in range(len(data)):
    player_name = data[i][0]

    if player_name not in player_dic:
        player_dic[player_name] = [data[i][4], 1]
    else:
        player_dic[player_name][0] += data[i][4]
        player_dic[player_name][1] += 1
print(player_dic)
res = [
    (player_name, player_data[0] / player_data[1])
    for player_name, player_data in player_dic.items()
]

# =============================================================================
# for arr in data:
#     print(arr[0])
# =============================================================================

print(res)


# Double check with boolean condition and column name to replace any nan values present 
len(threePts[(threePts == 'nan').any(axis=1)])
threePts.loc[threePts['success_%'] == 'nan', 'success_%'] = 0
threePts['game_id'].count()

twoPts['accuracy'] = (twoPts['field_goals']/twoPts['field_goals_attempts'])
twoPts['success_%'] = ((twoPts['field_goals']/twoPts['field_goals_attempts'])*100).round(2)
list(twoPts.columns)
twoPts.drop(['accuracy'], axis = 1, inplace= True)
twoPts['success_%'].value_counts()
twoPts['success_%'].describe()

freePts['accuracy'] = (freePts['free_throw']/freePts['free_throw_attempts'])
freePts['success_%'] = ((freePts['free_throw']/freePts['free_throw_attempts'])*100).round(2)
list(freePts.columns)
freePts.drop(['accuracy'], axis = 1, inplace= True)
freePts['success_%'].value_counts()
freePts['success_%'].describe()

test = df.groupby('game_id')['game_id'].sum()

games = df.groupby(['player'])['game_id'].count().sort_values(ascending = False)
points = df.groupby(['player'])[['points', 'game_id']].sum().sort_values(by= 'points', ascending = False)
merged = games.merge(points, how='left', on='player')
merged.info()
merged.rename(columns= {'game_id_x': 'total_games', 'points': 'total_points', 'game_id_y' : 'game_id'}, inplace = True)

# =============================================================================
# pandas.merge() vs DataFrame.merge() difference is wrapping vs chaining 
# - chaining is more efficient in the long run 
# - pd.merge(pd.merge(df1,df2), df3) vs df1.merge(df2).merge(df3) 
# =============================================================================
