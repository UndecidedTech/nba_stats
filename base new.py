#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import random as rnd
import numpy as np 
import matplotlib.pyplot as plt
import sys




gdf = pd.read_csv('2019_scores.csv')


print(sys.argv);

gdf.columns

WASdf = gdf[gdf.Team == 'WAS']
GSWdf = gdf[gdf.Team == 'GSW']

WASmeanpts = WASdf.TeamPoints.mean()
GSWmeanpts = GSWdf.TeamPoints.mean()
WASsdpts = WASdf.TeamPoints.std()
GSWsdpts = GSWdf.TeamPoints.std()

WASmeaGSWpp = WASdf.OpponentPoints.mean()
GSWmeaGSWpp = GSWdf.OpponentPoints.mean()
WASsdopp = WASdf.OpponentPoints.std()
GSWsdopp = GSWdf.OpponentPoints.std()

print("WAS Points Mean ", WASmeanpts)
print("WAS Points SD ", WASsdpts)
print("GSW Points Mean ", GSWmeanpts)
print("GSW SD ", GSWsdpts)

print("WAS OppPoints Mean ", WASmeaGSWpp)
print("WAS OppPoints SD ", WASsdopp)
print("GSW OppPoints Mean ", GSWmeaGSWpp)
print("GSW OppPoints SD ", GSWsdopp)



def gameSim():
    WASScore = (rnd.gauss(WASmeanpts,WASsdpts)+ rnd.gauss(GSWmeaGSWpp,GSWsdopp))/2
    GSWScore = (rnd.gauss(GSWmeanpts,GSWsdpts)+ rnd.gauss(WASmeaGSWpp,WASsdopp))/2
    if int(round(WASScore)) > int(round(GSWScore)):
        return 1
    elif int(round(WASScore)) < int(round(GSWScore)):
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
    print('WAS Win ', team1win/(team1win+team2win+tie),'%')
    print('GSW Win ', team2win/(team1win+team2win+tie),'%')
    print('Tie ', tie/(team1win+team2win+tie), '%')
    return gamesout



gamesSim(10000)

