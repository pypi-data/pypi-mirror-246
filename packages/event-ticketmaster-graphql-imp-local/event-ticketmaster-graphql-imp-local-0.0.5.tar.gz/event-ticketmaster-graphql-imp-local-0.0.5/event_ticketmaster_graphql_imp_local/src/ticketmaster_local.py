from dotenv import load_dotenv
from .util import TicketmasterUtil
import os
import requests
import geohash2
import sys
import pycountry  # for converting from country name -> country code
from .ticketmaster_event_constants import TicketmasterEventLocalConstants
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))
load_dotenv()
from event_remote.remote_event import EventRemote  # noqa
from logger_local.Logger import Logger  # noqa

logger = Logger.create_logger(
    object=TicketmasterEventLocalConstants.TICKETMASTER_EVENT_LOCAL_CODE_LOGGER_OBJECT)  # noqa

remote_event = EventRemote()


class TicketmasterLocal:
    def __init__(self) -> None:
        self.base_url = TicketmasterEventLocalConstants.TICKETMASTER_BASE_URL
        self.api_key = os.getenv("TICKETMASTER_API_KEY")
        self.discover_events = TicketmasterEventLocalConstants.TICKETMASTER_DISCOVER_EVENTS  # noqa

    def _internal_get_events(self, query_params: dict):
        object_start = {
            'query_params': query_params
        }
        logger.start("start internal get events", object=object_start)
        query_params_string = "&".join(
            [f"{key}={value}" for key, value in query_params.items()])

        url = f"{self.base_url}{self.discover_events}?apikey={
            self.api_key}&{query_params_string}"
        response = requests.get(url, params=None)

        logger.info("ticketmaster events response", object=response.json())

        events_list = TicketmasterUtil.convert_ticketmaster_json_to_external_event_list(response.json())  # noqa
        remote_event.create_external_events(events_list)

        object_end = {
            'events_list': events_list
        }
        logger.end("end internal get events", object=object_end)
        return response.json()

    def get_event_by_keyword(self, keyword: str, num_of_events: int = 1):
        object_start = {
            "keyword": keyword,
            "num_of_events": num_of_events}
        logger.start("start get_event_by_keyword", object=object_start)

        query_params = {
            "keyword": keyword,
            "size": num_of_events}

        response = self._internal_get_events(query_params=query_params)

        object_end = {
            "response": response
        }
        logger.end("end get_event_by_keyword", object=object_end)
        return response

    def get_events_by_radius(self, lat, lng, radius, unit, num_of_events=1):
        object_start = {
            "lat": lat,
            "lng": lng,
            "radius": radius,
            "unit": unit,
            "num_of_events": num_of_events
        }

        logger.start("start get_events_by_radius", object=object_start)
        geopoint = geohash2.encode(lat, lng, precision=9)

        query_params = {
            "geoPoint": geopoint,
            "radius": radius,
            "unit": unit,
            "size": num_of_events}

        response = self._internal_get_events(query_params=query_params)
        object_end = {
            "response": response
        }
        logger.end("end get_events_by_radius", object=object_end)
        return response

    def get_events_by_radius_km(self, lat, lng, radius, num_of_events=1):
        return self.get_events_by_radius(lat, lng, radius, "km", num_of_events)

    def get_events_by_radius_miles(self, lat, lng, radius, num_of_events=1):
        return self.get_events_by_radius(lat, lng, radius, "miles",
                                         num_of_events)

    def get_events_by_country_code(self, country_code: str,
                                   num_of_events: int = 1):
        object_start = {
            "country_code": country_code,
            "num_of_events": num_of_events
        }
        logger.start("start get_events_by_country_code", object=object_start)

        query_params = {
            "countryCode": country_code,
            "size": num_of_events}
        response = self._internal_get_events(query_params=query_params)

        object_end = {
            "response": response
        }
        logger.end("end get_events_by_country_code", object=object_end)
        return response

    def get_events_by_country(self, country: str, num_of_events: int = 1):
        object_start = {
            "country": country,
            "num_of_events": num_of_events
        }
        logger.start("start get_events_by_country", object=object_start)

        country_code = (pycountry.countries.get(name=country)).alpha_2

        response = self.get_events_by_country_code(country_code, num_of_events)
        object_end = {
            "response": response
        }
        logger.end("end get_events_by_country", object_end)
        return response

    def get_events_by_cities(self, cities: list[str], num_of_events: int = 1):
        object_start = {
            "city": cities,
            "num_of_events": num_of_events
        }
        logger.start("start get events by cities", object=object_start)

        query_parameters = {
            "city": cities,
            "size": num_of_events
        }

        response = self._internal_get_events(query_params=query_parameters)
        object_end = {
            "response": response
        }

        logger.end("end get events by cities", object=object_end)
        return response
