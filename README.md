# nsdepaturetimes
A dash webapp which shows the depature time of trains in the Netherlands

##Configurations
The configuration of the application occurs via some environment settings:
- Ocp-Apim-Subscription-Key: Key of the NS API subscription; you should be subscribed to NS App product on https://apiportal.ns.nl/
- STATION_CODE: the Station Code of the given station (stationsverkorting), e.g. ASD for Amsterdam Centraal
- MINIMUM_DEPARTURE_TIME: a filter to remove all trains that leave within that time
