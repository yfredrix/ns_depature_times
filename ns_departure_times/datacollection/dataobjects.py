from datetime import datetime
import pytz
import math


class Departures:
    def __init__(self, station_code: str = "", station_name: str = "") -> None:
        self.stationCode = station_code
        self.stationName = station_name

    def parse_departures(self, departures: dict):
        """
        Parse the departures from the API respones;
        Change the structure to having a dictionary keyed at the trainnumbers, containing the depature time, track and traincategory.
        """
        parsed_departures = {}
        for departure in departures["payload"]["departures"]:
            parsed_departures[departure["product"]["number"]] = {
                "name": departure["name"],
                "actualDateTime": datetime.strptime(
                    departure["actualDateTime"], "%Y-%m-%dT%H:%M:%S%z"
                )
                if "actualDateTime" in departure.keys()
                else None,
                "plannedDateTime": datetime.strptime(
                    departure["plannedDateTime"], "%Y-%m-%dT%H:%M:%S%z"
                ),
                "cancelled": departure["cancelled"],
                "direction": departure["direction"],
                "track": departure["actualTrack"]
                if "actualTrack" in departure.keys()
                else departure["plannedTrack"],
                "trainCategory": departure["trainCategory"],
                "trainNumber": departure["product"]["number"],
                "changedPlatform": False
                if (
                    "actualTrack" in departure.keys()
                    and departure["actualTrack"] == departure["plannedTrack"]
                )
                or ("actualTrack" not in departure.keys())
                else True,
                "via": [
                    departure["routeStations"][i]["mediumName"]
                    for i in range(len(departure["routeStations"]))
                ],
                "messages": [i['message'] for i in departure["messages"]],
            }
            parsed_departures[departure["product"]["number"]]["delay"] = math.ceil(
                (
                    parsed_departures[departure["product"]["number"]]["actualDateTime"]
                    - parsed_departures[departure["product"]["number"]][
                        "plannedDateTime"
                    ]
                ).total_seconds()
                / 60
            )
            parsed_departures[departure["product"]["number"]][
                "timeBeforeLeave"
            ] = math.floor(
                (
                    parsed_departures[departure["product"]["number"]]["actualDateTime"]
                    - datetime.now(tz=pytz.timezone("Europe/Amsterdam"))
                ).total_seconds()
                / 60
            )
        self.departures = parsed_departures

    def update_departures(self, updates: dict):
        for trainnumber in self.departures.keys():
            self.departures[trainnumber] = {
                **self.departures[trainnumber],
                **updates[trainnumber],
            }
