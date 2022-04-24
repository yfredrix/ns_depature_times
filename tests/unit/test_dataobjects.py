from nsdeparturetimes.datacollection import Departures
from datetime import datetime, timezone, timedelta


def test_parse_depatures():
    departure = Departures()
    departure.parse_departures(
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
                        "routeStations": [{"mediumName": "Rotterdam Centraal"}],
                        "messages": [{"message": ""}],
                    }
                ]
            }
        }
    )
    assert len(departure.departures) == 1
    assert departure.departures[1234]["name"] == "Amsterdam Centraal"
    assert departure.departures[1234]["actualDateTime"] == datetime(
        2019, 12, 4, 12, 0, 0, tzinfo=timezone(timedelta(hours=1))
    )
    assert departure.departures[1234]["plannedDateTime"] == datetime(
        2019, 12, 4, 12, 0, 0, tzinfo=timezone(timedelta(hours=1))
    )
    assert departure.departures[1234]["cancelled"] == False
    assert departure.departures[1234]["direction"] == "Oost"
    assert departure.departures[1234]["track"] == "1"
    assert departure.departures[1234]["trainCategory"] == "Intercity"
    assert departure.departures[1234]["trainNumber"] == 1234
    assert departure.departures[1234]["via"] == ["Rotterdam Centraal"]
