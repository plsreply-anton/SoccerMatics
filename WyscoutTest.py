#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 17:38:15 2023

@author: antonlarsson
"""

#importing necessary libraries
import pathlib
import os
import pandas as pd
import json
import codecs

#%% Competions

#path to data
path = os.path.join(str(pathlib.Path().resolve()), 'data', 'Wyscout', 'competitions.json')

#open data
with open(path) as f:
    data = json.load(f)
    
#save it in dataframe
df_competitions = pd.DataFrame(data)
#structure of data
df_competitions.info()

#%% Matches

#path to data
path = os.path.join(str(pathlib.Path().resolve()), 'data', 'Wyscout', 'Matches' ,'matches_England.json')

with open(path) as f:
    data = json.load(f)
    
#save it in a dataframe
df_matches = pd.DataFrame(data)
#structure of data
df_matches.info()

#%% Players

#path to data
path = os.path.join(str(pathlib.Path().resolve()), 'data', 'Wyscout', 'players.json')

#open data
with open(path) as f:
    data = json.load(f)
    
#save it in a dataframe
df_players = pd.DataFrame(data)
#structure of data
df_players.info()

#%% Events

path = os.path.join(str(pathlib.Path().resolve()), 'data','Wyscout', 'events','events_England.json')
with open(path) as f: 
    data = json.load(f)
df_events = pd.DataFrame(data) 

#structure of data
df_events.info()

#%% Referees

# DISCLAIMER
# Deleted last input to json file due to being incomplete

path = os.path.join(str(pathlib.Path().resolve()), 'data', 'Wyscout', 'referees.json')

with open(path) as f:
    data = json.load(f)
    
df_referees = pd.DataFrame(data)

df_referees.info()

#%% Teams

path = os.path.join(str(pathlib.Path().resolve()), 'data', 'Wyscout', 'teams.json')

with open(path) as f:
    data = json.load(f)

df_teams = pd.DataFrame(data)

df_teams.info()

#%% Coaches

path = os.path.join(str(pathlib.Path().resolve()), 'data', 'Wyscout', 'coaches.json')

with open(path) as f:
    data = json.load(f)

df_coaches = pd.DataFrame(data)

df_coaches.info()

#%% Playerrank

path = os.path.join(str(pathlib.Path().resolve()), 'data', 'Wyscout', 'playerank.json')

with open(path) as f:
    data = json.load(f)
    
df_playerank = pd.DataFrame(data)

df_playerank.info()

#%% Printing top scorer or something

df_playerank_sorted = df_playerank.sort_values('goalScored', ascending=False)
best_goalscorer = df_playerank_sorted.iloc[0]


best_goalscorer_id = best_goalscorer['playerId']

# Find the player's information in the players DataFrame
best_goalscorer_info = df_players[df_players['wyId'] == best_goalscorer_id]

# Print the best goalscorer's information
print("Best Goalscorer Info:")
for column, value in best_goalscorer_info.iloc[0].items():
    if isinstance(value, dict): #i.e if contains substrings
        print(f"{column}:")
        for sub_key, sub_value in value.items():
            if isinstance(sub_value, str):
                print(f"  {sub_key}: {codecs.decode(sub_value, 'unicode_escape')}")
            else:
                print(f"  {sub_key}: {sub_value}")
    else:
        if isinstance(value, str):
            print(f"{column}: {codecs.decode(value, 'unicode_escape')}")
        else:
            print(f"{column}: {value}")

























