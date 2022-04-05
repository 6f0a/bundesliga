from django.shortcuts import render
from zeep import Client
from datetime import datetime

# Create your views here.
client = Client(wsdl='https://www.openligadb.de/Webservices/Sportsdata.asmx?wsdl')

lastmatch = client.service.GetLastMatch('bl1')
season = lastmatch ['leagueSaison']

now = datetime.now()

def index(request):
    upcoming_matches = []
    matchlist = client.service.GetMatchdataByLeagueSaison('bl1', season)
    for y in matchlist:
        if y['matchDateTime'].date() > now.date():
            upcoming_matches.append(y)

    return render(request,'index/index.html',{
        'next_match': upcoming_matches[0:10],
    })