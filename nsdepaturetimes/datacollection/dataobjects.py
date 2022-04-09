from datetime import datetime
import pytz
import math


class Depatures:
    def __init__(self) -> None:
        pass

    def parse_depatures(self, depatures):
        """
        Parse the depatures from the API respones;
        Change the structure to having a dictionary keyed at the trainnumbers, containing the depature time, track and traincategory.
        """
        parsed_depatures = {}
        for depature in depatures["payload"]["departures"]:
            parsed_depatures[depature["product"]["number"]] = {
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
            parsed_depatures[depature["product"]["number"]]["delay"] = math.ceil(
                (
                    parsed_depatures[depature["product"]["number"]]["actualDateTime"]
                    - parsed_depatures[depature["product"]["number"]]["plannedDateTime"]
                ).total_seconds()
                / 60
            )
            parsed_depatures[depature["product"]["number"]][
                "timeBeforeLeave"
            ] = math.floor(
                (
                    parsed_depatures[depature["product"]["number"]]["actualDateTime"]
                    - datetime.now(tz=pytz.timezone("Europe/Amsterdam"))
                ).total_seconds()
                / 60
            )
        self.depatures = parsed_depatures

    def update_depatures(self, updates):
        for trainnumber in self.depatures.keys():
            self.depatures[trainnumber] = {
                **self.depatures[trainnumber],
                **updates[trainnumber],
            }
