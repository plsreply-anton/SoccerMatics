#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 18:51:47 2023

@author: antonlarsson
"""

import pandas as pd
import numpy as np
import json
# plotting
import matplotlib.pyplot as plt
#opening data
import os
import pathlib
import warnings
pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

#%% Open Data

# Opening events
path = os.path.join(str(pathlib.Path().resolve()), "data", "Wyscout", "events", "events_England.json")

with open(path) as f:
    data = json.load(f)
    
train_df = pd.DataFrame(data)
    
# Opening teamdata
path = os.path.join(str(pathlib.Path().resolve()), "data", "Wyscout", "teams.json")

with open(path) as f:
    data = json.load(f)

teams_df = pd.DataFrame(data)
teams_df = teams_df.rename(columns={"wyId": "teamId"})

#%% Preparing Dataset

#get corners
corners = train_df.loc[train_df["subEventName"] == "Corner"]
#print(corners)

#count corners by team
corners_by_team = corners.groupby(['teamId']).size().reset_index(name='counts')
#print(corners_by_team)

#merge with team name
summary = corners_by_team.merge(teams_df[["name", "teamId"]], how = "left", on = ["teamId"])
#print(summary)

#count corners by team by game
corners_by_game = corners.groupby(['teamId', "matchId"]).size().reset_index(name='counts')
#print(corners_by_game)

#merge with team name
summary2 = corners_by_game.merge(teams_df[["name", "teamId"]], how = "left", on = ["teamId"])
#print(summary2)

#%% Two Sided z-test
from statsmodels.stats.weightstats import ztest

# H0: Man City takes 8 corners per game
# Ha: Man City does not take 8 corners per game


#get city corners
city_corners = summary2.loc[summary2["name"] == 'Manchester City']["counts"]

#test
t, pvalue = ztest(city_corners,  value=8)

#checking outcome
# Using 0.05 as 5% chance of reject H0 wrongly
if pvalue < 0.05:
    print("P-value amounts to", pvalue, "- We reject null hypothesis - Manchester City do not take 8 corners per game")
    print("Test Statistics: ", t, " outside of: +-1.650")
else:
    print("P-value amounts to", pvalue, " - We do not reject null hypothesis - Manchester City take 8 corners per game")
    print("Test Statistics: ", t, " inside: +-1.650")

#%% One-sided z-test

# H0: Man City do not take more than 6 corners per game
# Ha: Man City takes more than 6 corners per game


t, pvalue = ztest(city_corners,  value=6, alternative = "larger")
if pvalue < 0.05:
    print("P-value amounts to", pvalue, "- We reject null hypothesis - Manchester City take more than 6 corners per game")
    print("Test Statistics: ", t, " above of: +1.650")
else:
    print("P-value amounts to", pvalue, " - We do not reject null hypothesis - Manchester City do not take 6 more corners per game")
    print("Test Statistics: ", t, " below: +1.650")

#%% One-sample two-sided t-test
mean = summary["counts"].mean()
std = summary["counts"].std()

# H0: Leicester takes the same nr of corners as league avarage
# Ha: Leicester do not take the same nr of corners as league avarage

from scipy.stats import ttest_1samp
leicester_corners = summary.loc[summary["name"] == "Leicester City"]["counts"].iloc[0]
t, pvalue = ttest_1samp(summary["counts"], leicester_corners)

if pvalue < 0.05:
    print("P-value amounts to", pvalue, "- We reject null hypothesis - Leicester City do not take average number of corners than league average")
    print("Test Statistics: ", t, " outside of: +-1.650")
else:
    print("P-value amounts to", pvalue, " - We do not reject null hypothesis - Leicester City take average number of corners than league average")
    print("Test Statistics: ", t, " inside: +-1.650")

#%% One-sample one-sided t-test
from scipy.stats import ttest_1samp
arsenal_corners = summary.loc[summary["name"] == "Arsenal"]["counts"].iloc[0]
t, pvalue = ttest_1samp(summary["counts"], arsenal_corners, alternative='less')

if pvalue < 0.05:
    print("P-value amounts to", pvalue, "- We reject null hypothesis - Arsenal take more corners than league average")
else:
    print("P-value amounts to", pvalue, " - We do not reject null hypothesis - Arsenal do not take more corners than league average")
    
#%% Two-sample two-sided t-test

#check if united takes the same average number of corners per game as liverpool
liverpool_corners = summary2.loc[summary2["name"] == 'Liverpool']["counts"]
united_corners = summary2.loc[summary2["name"] == 'Manchester United']["counts"]

from scipy.stats import ttest_ind
t, pvalue  = ttest_ind(a=liverpool_corners, b=united_corners, equal_var=True)

if pvalue < 0.05:
    print("P-value amounts to", pvalue, "- We reject null hypothesis - Liverpool took different number of corners per game than United")
else:
    print("P-value amounts to", pvalue, " - We do not reject null hypothesis - Liverpool took the same number of corners per game as United")


#%% Two-sample one-sided t-test

city_corners = summary2.loc[summary2["name"] == 'Manchester City']["counts"]
castle_corners = summary2.loc[summary2["name"] == 'Newcastle United']["counts"]

from scipy.stats import ttest_ind
t, pvalue  = ttest_ind(a=city_corners, b=castle_corners, equal_var=True, alternative = "greater")

if pvalue < 0.05:
    print("P-value amounts to", pvalue, "- We reject null hypothesis - City took more corners per game than Newcastle")
else:
    print("P-value amounts to", pvalue, " - We do not reject null hypothesis - City did not  take the more corners per game than Newcastle")


