from logger_local.LoggerComponentEnum import LoggerComponentEnum


class TicketmasterEventLocalConstants:

    DEVELOPER_EMAIL = 'gil.a@circ.zone'
    TICKETMASTER_EVENT_LOCAL_COMPONENT_ID = 246
    # TODO Please write your own COMPONENT_NAME
    TICKETMASTER_EVENT_LOCAL_PYHTON_COMPONENT_NAME = "event-ticketmaster-graphql-imp-local"  # noqa
    TICKETMASTER_EVENT_LOCAL_CODE_LOGGER_OBJECT = {
        'component_id': TICKETMASTER_EVENT_LOCAL_COMPONENT_ID,
        'component_name': TICKETMASTER_EVENT_LOCAL_PYHTON_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'developer_email': DEVELOPER_EMAIL
    }
    TICKETMASTER_EVENT_LOCAL_TEST_LOGGER_OBJECT = {
        'component_id': TICKETMASTER_EVENT_LOCAL_COMPONENT_ID,
        'component_name': TICKETMASTER_EVENT_LOCAL_PYHTON_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value, # noqa
        # TODO Please add the framework you use
        'developer_email': DEVELOPER_EMAIL
    }

    TICKETMASTER_BASE_URL = "https://app.ticketmaster.com"

    TICKETMASTER_DISCOVER_EVENTS = "/discovery/v2/events.json"

    TICKETMASTER_SYSTEM_ID = 10
