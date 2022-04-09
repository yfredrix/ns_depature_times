from typing import List
from urllib3 import PoolManager
import os
import json


class ApiConnections:
    prefix_url = "https://gateway.apiportal.ns.nl/"

    def __init__(self) -> None:
        self.httpPool = PoolManager(
            headers={
                "Ocp-Apim-Subscription-Key": os.environ.get("Ocp-Apim-Subscription-Key")
            }
        )

    def get_depatures(self, station_code: str) -> dict:
        req = self.httpPool.request(
            "GET",
            f"{self.prefix_url}reisinformatie-api/api/v2/departures?station={station_code}",
        )
        depatures = json.loads(req.data.decode("utf-8"))
        self.station_code = station_code
        return depatures

    def get_crowdedness(self, trainnumbers: List[str]) -> dict:
        crowdedness = {}
        for trainnumber in trainnumbers:
            crowdedness[trainnumber] = {}
            req = self.httpPool.request(
                "GET",
                f"{self.prefix_url}virtual-train-api/api/v1/prognose/{trainnumber}",
            )
            prognose = json.loads(req.data.decode("utf-8"))
            if isinstance(prognose, list):
                for stationprog in prognose:
                    if stationprog["station"] == self.station_code:
                        crowdedness[trainnumber]["classifiction"] = stationprog[
                            "classifiction"
                        ]
            if "classifiction" not in crowdedness[trainnumber].keys():
                crowdedness[trainnumber]["classifiction"] = "UNKNOWN"
        return crowdedness

    def get_trains(self, trainnumbers: List[str]) -> dict:
        trains = {}
        for trainnumber in trainnumbers:
            trains[trainnumber] = {}
            req = self.httpPool.request(
                "GET",
                f"{self.prefix_url}virtual-train-api/api/v1/trein?ids={trainnumber}&stations={self.station_code}&features=drukte,druktev2",
            )
            payloads = json.loads(req.data.decode("utf-8"))
            if isinstance(payloads, list):
                for payload in payloads:
                    trains[trainnumber] = {
                        "materieel": payload["materieeldelen"],
                        "ingekort": payload['ingekort'],
                    }
            if "materieel" not in trains[trainnumber].keys():
                trains[trainnumber]["materieel"] = "UNKNOWN"
                trains[trainnumber]["ingekort"] = "UNKNOWN"
        return trains
