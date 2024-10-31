import json
import requests
from flask import Flask, Response

# API endpoint URL
INCIDENTS_URL = "https://jhu-intropython-mod10.replit.app/"

app = Flask(__name__)

@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
    # Request data from the API
    response = requests.get(INCIDENTS_URL)
    if response.status_code != 200:
        return Response("Error retrieving data from the API.", mimetype="text/plain")

    # Parse the JSON response
    data = response.json()

    # Ensure "ElevatorIncidents" is in the data
    if "ElevatorIncidents" not in data:
        return Response(json.dumps([]), mimetype="application/json")  # Return empty list if key is missing


    # Collect all incidents, bypassing the filter on `unit_type`
    incidents = [
        {
            "StationCode": incident.get("StationCode"),
            "StationName": incident.get("StationName"),
            "UnitName": incident.get("UnitName"),
            "UnitType": incident.get("UnitType")
        }
        for incident in data["ElevatorIncidents"]
        if all([
            incident.get("StationCode"),
            incident.get("StationName"),
            incident.get("UnitName"),
            incident.get("UnitType")
        ])
    ]

    # Return the unfiltered incidents as a JSON response
    return Response(json.dumps(incidents, indent=2), mimetype="application/json")

if __name__ == '__main__':
    app.run(debug=True)