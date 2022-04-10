from nsdepaturetimes.datacollection import Depatures
from datetime import datetime, timezone, timedelta


def test_parse_depatures():
    depature = Depatures()
    depature.parse_depatures(
        {
            "payload": {
                "departures": [
                    {
                        "name": "Amsterdam Centraal",
                        "actualDateTime": "2019-12-04T12:00:00+0100",
                        "plannedDateTime": "2019-12-04T12:00:00+0100",
                        "cancelled": False,
                        "direction": "Oost",
                        "plannedTrack": "1",
                        "trainCategory": "Intercity",
                        "product": {"number": 1234},
                    }
                ]
            }
        }
    )
    assert len(depature.depatures) == 1
    assert depature.depatures[1234]["name"] == "Amsterdam Centraal"
    assert depature.depatures[1234]["actualDateTime"] == datetime(2019,12,4,12,0,0,tzinfo=timezone(timedelta(hours=1)))
    assert depature.depatures[1234]["plannedDateTime"] == datetime(2019,12,4,12,0,0,tzinfo=timezone(timedelta(hours=1)))
    assert depature.depatures[1234]["cancelled"] == False
    assert depature.depatures[1234]["direction"] == "Oost"
    assert depature.depatures[1234]["track"] == "1"
    assert depature.depatures[1234]["trainCategory"] == "Intercity"
    assert depature.depatures[1234]["trainNumber"] == 1234