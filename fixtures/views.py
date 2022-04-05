from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from zeep import Client

client = Client(wsdl='https://www.openligadb.de/Webservices/Sportsdata.asmx?wsdl')

lastmatch = client.service.GetLastMatch('bl1')
season = lastmatch['leagueSaison']

def fixtures(request,matchday):
    matchlist = client.service.GetFusballdaten(matchday,'bl1',season)
    allRounds = client.service.GetAvailGroups('bl1',season)
    if  matchday > 34 or matchday < 1:
        return HttpResponse('<h1>Matchday not available</h1>')
    else:  
        return render(request,"matches/matchlist.html",{
            'matchlist':matchlist,
            'matchday':matchday,
            'allRounds':allRounds,
            })
