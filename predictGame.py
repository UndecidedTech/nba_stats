#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import random as rnd
import numpy as np 
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--teams", "-t", help="Supply two teams to calculate against", nargs=2);
args = parser.parse_args()

print(args.teams)

gdf = pd.read_csv('2019_scores.csv')


gdf.columns

team1 = args.teams[0]
team2 = args.teams[1]

Team1df = gdf[gdf.Team == team1]
Team2df = gdf[gdf.Team == team2]

Team1meanpts = Team1df.TeamPoints.mean()
Team2meanpts = Team2df.TeamPoints.mean()
Team1sdpts = Team1df.TeamPoints.std()
Team2sdpts = Team2df.TeamPoints.std()

Team1meaTeam2pp = Team1df.OpponentPoints.mean()
Team2meaTeam2pp = Team2df.OpponentPoints.mean()
Team1sdopp = Team1df.OpponentPoints.std()
Team2sdopp = Team2df.OpponentPoints.std()

# output = {}

# output["%s Points Mean" % team1] = Team1meanpts
# output["%s Points SD" % team1] = Team1sdpts
# output["%s Points Mean" % team2] = Team2meanpts
# output["%s Points Mean" % team2] = Team2sdpts
 

print("%s Points Mean " % team1, Team1meanpts)
print("%s Points SD " % team1, Team1sdpts)
print("%s Points Mean " % team2, Team2meanpts)
print("%s SD " % team2, Team2sdpts)

# output["%s OppPoints Mean" % team1] = Team1meaTeam2pp
# output["%s OppPoints SD" % team1] = Team1sdopp
# output["%s OppPoints Mean" % team2] = Team2meaTeam2pp
# output["%s OppPoints Mean" % team2] = Team2sdopp

print("%s OppPoints Mean " % team1, Team1meaTeam2pp)
print("%s OppPoints SD " % team1, Team1sdopp)
print("%s OppPoints Mean " % team2, Team2meaTeam2pp)
print("%s OppPoints SD " % team2, Team2sdopp)


def gameSim():
    Team1Score = (rnd.gauss(Team1meanpts,Team1sdpts)+ rnd.gauss(Team2meaTeam2pp,Team2sdopp))/2
    Team2Score = (rnd.gauss(Team2meanpts,Team2sdpts)+ rnd.gauss(Team1meaTeam2pp,Team1sdopp))/2
    if int(round(Team1Score)) > int(round(Team2Score)):
        return 1
    elif int(round(Team1Score)) < int(round(Team2Score)):
        return -1
    else: return 0


def gamesSim(ns):
    gamesout = []
    team1win = 0
    team2win = 0
    tie = 0
    for i in range(ns):
        gm = gameSim()
        gamesout.append(gm)
        if gm == 1:
            team1win +=1
        elif gm == -1:
            team2win +=1
        else: tie +=1
    print('%s Win '  % team1, team1win/(team1win+team2win+tie),'%')
    print('%s Win ' % team2, team2win/(team1win+team2win+tie),'%')
    print('Tie ', tie/(team1win+team2win+tie), '%')
    return gamesout



gamesSim(10000)

