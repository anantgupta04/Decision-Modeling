# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 12:06:52 2020

@author: akhilg
"""

PATH = ""
assert len(PATH)>0,"Please set where the folder has been unzipped"

import operator
import pandas as pd


def setup(path):
    data = {}
    # reading a CSV
    df = pd.read_csv(path+"\\data.csv",header=None)
    
    # finding the total votes casted
    total_votes = df[0].sum()
    
    data["total_votes"] = total_votes
    data["votes"] = df
    return data

def sum_round1_votes(data):
    df = data.loc[:,0:1].values
    round1_score = {candidate:0 for candidate in data.loc[0,1:]}
    
    for i in df:
        round1_score[i[1]]  += i[0]
    return round1_score

def majortity(params):
    data = params.get("votes")
    total_votes = params.get("total_votes")
    pref1_score = sum_round1_votes(data)
    winner, max_votes = max(pref1_score.items(), key=operator.itemgetter(1))
    if max_votes < 0.5*total_votes:
        winner = "Not possible "
    print("According to the Majority Voting principe, the winning candidate is: ",winner)
    
    
def plurality(params):
    data = params.get("votes")  
    pref1_score = sum_round1_votes(data)
    winner, max_votes = max(pref1_score.items(), key=operator.itemgetter(1))
    print("According to the Plurality Voting principe, the winning candidate is: ",winner)
   
    
def plurality_runoff(params):
    data = params.get("votes")
    total_votes = params.get("total_votes")
    pref1_score = sum_round1_votes(data)
    c2,c1 = [{k: v }for k, v in sorted(pref1_score.items(), key=lambda item: item[1])][-2:]
    
    # getting the top-2 people recieving max votes
    candidate1 = c1.popitem()
    candidate2 = c2.popitem()
    
    #Checking for majority
    if candidate1[1] > 0.5*total_votes:
       winner = candidate1[0] 
    else :
        newC1_score, newC2_score = counting(candidate1[0],candidate2[0],data)
    winner  = candidate1[0] if newC1_score > newC2_score else candidate2[0]
    print("According to the Plurality Run-Off Voting principe, the winning candidate is: ",winner)


def condorcet(params):
    data = params.get("votes")
    candidates = data.loc[0,1:]
    
    for candidate1 in candidates:
        check = True 
        for candidate2 in (candidates):
            if candidate1 != candidate2:
                preference1,preference2 = counting(candidate1, candidate2, 
                                                 data)
                if preference1 < preference2:
                    check = False
                    break
        if check:
            print("According to the Condorcet Voting principe, the winning candidate is: ",candidate1)


def counting(candidate1, candidate2, data):
        candidate1_score = 0
        candidate2_score = 0
        total = len(data[0])
        for i in range(1,total):
            pref_list = data.loc[i,:].to_list()
            if pref_list.index(candidate1) < pref_list.index(candidate2):
                candidate1_score += pref_list[0]
            else:
                candidate2_score += pref_list[0]
        return(candidate1_score,candidate2_score)
    

def borda_voting(params):
    data = params.get("votes")
    pref_list = data.loc[:,1:].values
    
    borda_score = {candidate:0 for candidate in data.loc[0,1:]}
    for inner_list in pref_list:
        for i, candidate in enumerate(inner_list):
            borda_score[candidate] += i+1
    winner = min(borda_score.items(), key=operator.itemgetter(1))[0]
    print("According to the Borda Voting principe, the winning candidate is: ",winner)


if __name__ == "__main__":
    params = setup(PATH)
    
    majortity(params)
    plurality(params)
    plurality_runoff(params)
    condorcet(params)
    borda_voting(params)