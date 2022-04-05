from zeep import Client

client = Client(wsdl='https://www.openligadb.de/Webservices/Sportsdata.asmx?wsdl')


print(client.service.GetLastMatchByLeagueTeam(4500,7))



