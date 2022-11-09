import requests
import json


response = requests.get("http://data.itsfactory.fi/journeys/api/1/stop-monitoring?stops=2519")
received = response.json()
timetable = received['body']

print(timetable['2519'][0]['lineRef']+":", timetable['2519'][0]['call']['aimedArrivalTime'])
print(timetable['2519'][1]['lineRef']+":", timetable['2519'][1]['call']['aimedArrivalTime']) 


