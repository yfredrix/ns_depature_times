from typing import List
from urllib3 import PoolManager
import os
import json


class ApiConnections:
    prefix_url = "https://gateway.apiportal.ns.nl/"

    def __init__(self) -> None:
        self.httpPool = PoolManager(
            headers={"Ocp-Apim-Subscription-Key": os.getenv("SUBSCRIPTION_KEY")}
        )

    def get_departures(self, station_code: str) -> dict:
        req = self.httpPool.request(
            "GET",
            f"{self.prefix_url}reisinformatie-api/api/v2/departures?station={station_code}",
        )
        departures = json.loads(req.data.decode("utf-8"))
        self.station_code = station_code
        return departures

    def get_crowdedness(self, trainnumbers: List[str]) -> dict:
        crowdedness = {}
        for trainnumber in trainnumbers:
            crowdedness[trainnumber] = {}
            req = self.httpPool.request(
                "GET",
                f"{self.prefix_url}virtual-train-api/api/v1/prognose/{trainnumber}",
            )
            prognose = json.loads(req.data.decode("utf-8"))
            if isinstance(prognose["prognoses"], list):
                for stationprog in prognose["prognoses"]:
                    if stationprog["stationUic"] == self.stationUICode:
                        crowdedness[trainnumber]["classification"] = stationprog[
                            "classification"
                        ]
            if "classification" not in crowdedness[trainnumber].keys():
                crowdedness[trainnumber]["classification"] = "UNKNOWN"
        return crowdedness

    def get_trains(self, trainnumbers: List[str]) -> dict:
        trains = {}
        for trainnumber in trainnumbers:
            invalid_material = False
            trains[trainnumber] = {}
            req = self.httpPool.request(
                "GET",
                f"{self.prefix_url}virtual-train-api/api/v1/trein?ids={trainnumber}&stations={self.station_code}&features=drukte,druktev2",
            )
            payloads = json.loads(req.data.decode("utf-8"))
            if isinstance(payloads, list):
                for payload in payloads:
                    for part in payload["materieeldelen"]:
                        if part["type"] != "":
                            continue
                        else:
                            invalid_material = True
                            break
                    if not invalid_material:
                        trains[trainnumber] = {
                            "materieel": payload["materieeldelen"],
                            "ingekort": payload["ingekort"],
                        }
                    else:
                        trains[trainnumber] = {
                            "materieel": [],
                            "ingekort": "UNKNOWN",
                        }
            if "materieel" not in trains[trainnumber].keys():
                trains[trainnumber]["materieel"] = []
                trains[trainnumber]["ingekort"] = "UNKNOWN"
        return trains

    def get_station(self, station_code: str) -> dict:
        req = self.httpPool.request(
            "GET",
            f"{self.prefix_url}reisinformatie-api/api/v2/stations",
        )
        payload = json.loads(req.data.decode("utf-8"))["payload"]
        for station_dict in payload:
            if station_dict["code"].upper() == station_code.upper():
                self.stationUICode = station_dict["UICCode"]
                return station_dict
        return {"code": station_code, "namen": {"middel": "station not found"}}
