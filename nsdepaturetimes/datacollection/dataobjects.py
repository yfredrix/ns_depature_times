from datetime import datetime
import pytz
import math


class Departures:
    def __init__(self) -> None:
        pass

    def parse_departures(self, departures):
        """
        Parse the departures from the API respones;
        Change the structure to having a dictionary keyed at the trainnumbers, containing the depature time, track and traincategory.
        """
        parsed_departures = {}
        for depature in departures["payload"]["departures"]:
            parsed_departures[depature["product"]["number"]] = {
                "name": depature["name"],
                "actualDateTime": datetime.strptime(
                    depature["actualDateTime"], "%Y-%m-%dT%H:%M:%S%z"
                )
                if "actualDateTime" in depature.keys()
                else None,
                "plannedDateTime": datetime.strptime(
                    depature["plannedDateTime"], "%Y-%m-%dT%H:%M:%S%z"
                ),
                "cancelled": depature["cancelled"],
                "direction": depature["direction"],
                "track": depature["actualTrack"]
                if "actualTrack" in depature.keys()
                else depature["plannedTrack"],
                "trainCategory": depature["trainCategory"],
                "trainNumber": depature["product"]["number"],
            }
            parsed_departures[depature["product"]["number"]]["delay"] = math.ceil(
                (
                    parsed_departures[depature["product"]["number"]]["actualDateTime"]
                    - parsed_departures[depature["product"]["number"]]["plannedDateTime"]
                ).total_seconds()
                / 60
            )
            parsed_departures[depature["product"]["number"]][
                "timeBeforeLeave"
            ] = math.floor(
                (
                    parsed_departures[depature["product"]["number"]]["actualDateTime"]
                    - datetime.now(tz=pytz.timezone("Europe/Amsterdam"))
                ).total_seconds()
                / 60
            )
        self.departures = parsed_departures

    def update_departures(self, updates):
        for trainnumber in self.departures.keys():
            self.departures[trainnumber] = {
                **self.departures[trainnumber],
                **updates[trainnumber],
            }
