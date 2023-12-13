from .ticketmaster_event_constants import TicketmasterEventLocalConstants
from dotenv import load_dotenv
import os
load_dotenv()
from logger_local.Logger import Logger  # noqa


class TicketmasterResponseException(Exception):
    pass


logger = Logger.create_logger(object=TicketmasterEventLocalConstants.TICKETMASTER_EVENT_LOCAL_CODE_LOGGER_OBJECT) # noqa


class TicketmasterUtil:

    def convert_ticketmaster_json_to_external_event_list(ticketmaster_json: dict): # noqa
        logger.start("start convert ticketmaster JSON to external events list",
                     object=ticketmaster_json)
        try:

            if 'errors' in ticketmaster_json:
                error_details = ticketmaster_json.get('errors')
                raise TicketmasterResponseException(error_details[0]['detail'])

            events_data = ticketmaster_json['_embedded']['events']
            external_events = []

            # Iterate through each event
            for event in events_data:
                url = event['url']
                # subsystem_id = 1  # temp
                system_id = TicketmasterEventLocalConstants.TICKETMASTER_SYSTEM_ID  # noqa
                external_event_identifier = event['id']
                environment_id = os.getenv("ENVIRONMENT_ID")

                external_events.append({'url': url,
                                        'system_id': system_id,
                                        # 'subsystem_id': subsystem_id,
                                        'external_event_identifier': external_event_identifier,  # noqa
                                        'environment_id': environment_id})

            object_end = {
                'external_events': external_events
            }
            logger.end("end convert ticketmaster JSON to external events list",
                       object=object_end)
            return external_events

        except TicketmasterResponseException as e:
            logger.exception(f"Ticketmaster response exception: {str(e)}",
                             object=e)
            raise

        except Exception as e:
            logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
