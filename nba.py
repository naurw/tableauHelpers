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
       'venue', 'starter', 'minutes', 'field_goals', 'field_goals_attempts', '3_point', '3_point_attempt', 'free_throw',
       'free_throw_attempt', 'offensive_rebound', 'defensive_rebound', 'total_rebound', 'assists', 'personal_fouls', 'steals', 'turnovers',
       'blocks', 'points', 'usage_rate', 'days_rest']

df['date'] = pd.to_datetime(df['date']).dt.date

# =============================================================================
# Questions to explore
# 1. Which NBA player has the highest 3PT avg? 
# 2. Which NBA player has the lowest FG avg? 
# 3. Which NBA player has the most rebounds? 
# 4. Which NBA player has the least turnovers? 
# =============================================================================

df.info()
print('The total number of players within this masterlist is: ', df.player.nunique(), '.', sep ='')
print('The total number of games within this masterlist is : ', df.game_id.nunique(), '.', sep = '')
df.date.value_counts()

games = df.groupby(['player'])['game_id'].count().sort_values(ascending = False).to_frame()
points = df.groupby(['player'])[['points', 'game_id']].sum().sort_values(by= 'points', ascending = False)
merge = pd.merge(games, test, how='left', on= 'player')
merged = games.merge(points, how='left', on='player')
merged.info()
merged.rename(columns= {'game_id_x': 'total_games', 'points': 'total_points', 'game_id_y' : 'game_id'})

# =============================================================================
# pandas.merge() vs DataFrame.merge() difference is wrapping vs chaining 
# - chaining is more efficient in the long run 
# - pd.merge(pd.merge(df1,df2), df3) vs df1.merge(df2).merge(df3) 
# =============================================================================
