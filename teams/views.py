from tkinter.tix import DECREASING
from django.http import HttpResponse
from django.shortcuts import render
from zeep import Client

client = Client(wsdl='https://www.openligadb.de/Webservices/Sportsdata.asmx?wsdl')
lastmatch = client.service.GetLastMatch('bl1')
season = lastmatch['leagueSaison']

def win_loss(allTeams,all_matches):
    for team in allTeams:
        all_matches_home = []
        all_matches_away = []
        win_counter = 0
        lose_counter = 0
        for i in all_matches:
            if i['idTeam1'] == team['teamID']:
                all_matches_home.append(i)
            elif i['idTeam2'] == team['teamID']:
                all_matches_away.append(i)

        for z in all_matches_home:
            if z['pointsTeam1'] > z['pointsTeam2']:
                win_counter += 1
            elif z['pointsTeam1'] < z['pointsTeam2']:
                lose_counter += 1

        for y in all_matches_away:
            if y['pointsTeam1'] > y['pointsTeam2']:
                lose_counter += 1
            elif y['pointsTeam1'] < y['pointsTeam2']:
                win_counter += 1
        
        team['win_counter'] = win_counter
        team['lose_counter'] = lose_counter
        team['win_percentage'] = int((win_counter/(win_counter+lose_counter))*100)

    return allTeams
    
def win_loss_detail(all_matches,id):
        team = []
        all_matches_home = []
        all_matches_away = []
        win_counter = 0
        lose_counter = 0
        for i in all_matches:
            if i['idTeam1'] == id:
                all_matches_home.append(i)
            elif i['idTeam2'] == id:
                all_matches_away.append(i)

        for z in all_matches_home:
            if z['pointsTeam1'] > z['pointsTeam2']:
                win_counter += 1
            elif z['pointsTeam1'] < z['pointsTeam2']:
                lose_counter += 1

        for y in all_matches_away:
            if y['pointsTeam1'] > y['pointsTeam2']:
                lose_counter += 1
            elif y['pointsTeam1'] < y['pointsTeam2']:
                win_counter += 1
        
        win_percentage = int((win_counter/(win_counter+lose_counter))*100)
        

        return win_counter,lose_counter,win_percentage
    


# Create your views here.

def teams(request):
    allTeams = client.service.GetTeamsByLeagueSaison('bl1', season)
    all_matches = client.service.GetMatchdataByLeagueSaison('bl1', season)

    allTeams = win_loss(allTeams,all_matches)

    return render(request, 'teams/teams.html',{
        'allTeams':allTeams,
    })

def team_detail(request, id):
    team = []
    allID = []
    allTeams = client.service.GetTeamsByLeagueSaison('bl1', season)
    for i in allTeams:
        allID.append(i['teamID'])
    if id in allID:
        all_matches = client.service.GetMatchdataByLeagueSaison('bl1', season)
        for y in allTeams:
            if y['teamID'] == id:
                team.append(y)
        win_counter,lose_counter,win_percentage = win_loss_detail(all_matches,id)
        print(win_counter,lose_counter,win_percentage)

        for y in team:
            y['win_counter'] = win_counter
            y['lose_counter'] = lose_counter
            y['win_percentage'] = win_percentage
        
        next_match = client.service.GetNextMatchByLeagueTeam(4500, id)
        latest_results = []
        for y in all_matches:
            if y['idTeam1'] == id and y['pointsTeam1'] == True  or y['idTeam2'] == id and y['pointsTeam1'] == True:
                latest_results.append(y)

        return render(request, 'teams/team_details.html',{
            'team':team,
            'next_match':next_match,
            'latest_results':reversed(latest_results[-5:]),
        })
    else:
        return HttpResponse('<h1>Team not found</h1>')
