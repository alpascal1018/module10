import json
import requests
from flask import Flask

# API endpoint URL
INCIDENTS_URL = "https://jhu-intropython-mod10.replit.app/"

################################################################################

app = Flask(__name__)

# get incidents by machine type (elevators/escalators)
# field is called "unit_type" in WMATA API response
@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type: str):
  # create an empty list called 'incidents'
  incidents = []
  # use 'requests' to do a GET request to the WMATA Incidents API
  station_response = requests.get(INCIDENTS_URL)
  # retrieve the JSON from the response
  station_loads = json.loads(station_response.text)
  # iterate through the JSON response and retrieve all incidents matching 'unit_type'
  match_type = []
  for incident in station_loads["ElevatorIncidents"]:
    if str(incident["UnitType"]).lower() in unit_type:
      match_type.append(incident)
  # for each incident, create a dictionary containing the 4 fields from the Module 7 API definition
  #   -StationCode, StationName, UnitType, UnitName
  for incident in match_type:
    info = {
        "StationCode": "",
        "StationName": "",
        "UnitType": "",
        "UnitName": ""
    }
    info["StationCode"] = incident["StationCode"]
    info["StationName"] = incident["StationName"]
    info["UnitType"] = incident["UnitType"]
    info["UnitName"] = incident["UnitName"]
    # add each incident dictionary object to the 'incidents' list
    incidents.append(info)
  # return the list of incident dictionaries using json.dumps()
  return(json.dumps(incidents))
################################################################################

if __name__ == '__main__':
    app.run(debug=True)