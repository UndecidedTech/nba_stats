#!/usr/bin/env python
# coding: utf-8
import json
import pandas as pd 
import random as rnd
import numpy as np 
import matplotlib.pyplot as plt
import argparse
import requests
import nba_api
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import leaguestandings

parser = argparse.ArgumentParser()
parser.add_argument("--teams", "-t", help="Supply two teams to calculate against", nargs=2);
args = parser.parse_args()

# print(args.teams)

gdf = pd.read_csv('2019_scores.csv')
gdf.columns

team1 = args.teams[0]
team2 = args.teams[1]
# print("Teams", args.teams)


team1Return = teams.find_team_by_abbreviation(team1)
team2Return = teams.find_team_by_abbreviation(team2)
# print(team1Return)
# print(team2Return)

# Check for teams last 5 games results

gamefinder1 = leaguegamefinder.LeagueGameFinder(team_id_nullable=team1Return["id"])
# The first DataFrame of those returned is what we want.
games1 = gamefinder1.get_data_frames()[0]
#print(games1)
team1Record = games1.head()["WL"]

gamefinder2 = leaguegamefinder.LeagueGameFinder(team_id_nullable=team2Return["id"])
# The first DataFrame of those returned is what we want.
games2 = gamefinder2.get_data_frames()[0]

team2Record = games2.head()["WL"]
# LETS GOOOOOOOOOO
standings = leaguestandings.LeagueStandings(league_id="00", season="2019-20", season_type="Regular Season")
#Pulled in team stats -- calculate home/winloss depending on who is team1
print(standings.get_data_frames()[0].query("TeamID == %s" % team1Return["id"]))


def findAdvantage():
    team1Games = 0
    team2Games = 0
    for i in range(len(team1Record)):
        if team1Record[i] == "W":
            team1Games += 1
        if team2Record[i] == "W":
            team2Games += 1
    result = {}
    if team1Games > team2Games:
        result["team"] = team1
        result["diff"] = (team1Games - team2Games) * 2
    else:
        result["team"] = team2
        result["diff"] =  (team2Games - team1Games) * 2
    return result

    

# Rudimentary helper function to find the difference between each team's past 5 games
# print(findAdvantage())


# print(team1, team1Record)
# print(team2, team2Record)



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
    #PRINT and assign pure w/l
    team1WinPct = team1win/(team1win+team2win+tie)
    team2WinPct = team2win/(team1win+team2win+tie)
    print("\n")
    print("Raw Calculation")
    print("------------------------------------------")
    print('%s Pure Win '  % team1, team1WinPct,'%')
    print('%s Pure Win ' % team2, team2WinPct,'%')
    print('Tie ', tie/(team1win+team2win+tie), '%')
    #+ - percent from the return of findAdv() here before printing to console
    teamDiff = findAdvantage()
    if teamDiff["team"] == team1:
        team1WinPct = (team1win/(team1win+team2win+tie)) + (teamDiff["diff"]/100)
        team2WinPct = (team2win/(team1win+team2win+tie)) - (teamDiff["diff"]/100)
    else:
        team1WinPct = (team1win/(team1win+team2win+tie)) - (teamDiff["diff"]/100)
        team2WinPct = (team2win/(team1win+team2win+tie)) + (teamDiff["diff"]/100)
    print("\n")
    print("Adjusted Calculation")
    print("------------------------------------------")
    print('%s Win '  % team1, team1WinPct,'%')
    print('%s Win ' % team2, team2WinPct,'%')
    print('Tie ', tie/(team1win+team2win+tie), '%')
    return gamesout



gamesSim(10000)

