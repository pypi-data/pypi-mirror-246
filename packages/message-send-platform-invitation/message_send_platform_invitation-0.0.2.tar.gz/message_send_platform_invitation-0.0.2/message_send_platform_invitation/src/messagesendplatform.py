from dotenv import load_dotenv

from circles_local_database_python.connector import Connector
from circles_local_database_python.generic_crud import GenericCRUD
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum

MESSAGE_SEND_PLATFORM_INVITATION_LOCAL_PYTHON_COMPONENT_ID = 243
MESSAGE_SEND_PLATFORM_INVITATION_LOCAL_PYTHON_COMPONENT_COMPONENT_NAME = "message-send-platform-invitation-local-python"
DEVELOPER_EMAIL = 'jenya.b@circ.zone'
object1 = {
    'component_id': MESSAGE_SEND_PLATFORM_INVITATION_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': MESSAGE_SEND_PLATFORM_INVITATION_LOCAL_PYTHON_COMPONENT_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
logger=Logger.create_logger(object=object1)

load_dotenv()

class MessageSendPlatform(GenericCRUD):
    def __init__(self,schema_name, connection: Connector = None,) -> None:
        super().__init__(schema_name, connection)

    def get_potential_person_list_by_campaign_id(self, campaign_id) -> list:
        logger.start(f"get potential person list by campaign id={campaign_id}")
        query = (
            "SELECT person.person_table.person_id "
            "FROM criteria.criteria_table CROSS JOIN ("
            "SELECT person.person_table.person_id FROM person.person_table "
            "WHERE TIMESTAMPDIFF(YEAR, birthday_date, CURDATE()) > 22"
            ") AS person_table JOIN campaign.campaign_table AS campaign_table ON campaign_table.criteria_id = criteria.criteria_table.criteria_id "
            f"WHERE campaign_table.campaign_id = {campaign_id}"
        )
        self.cursor.execute(query)
        potential_person_tpl =  self.cursor.fetchall()
        potential_person_list = [item[0] for item in potential_person_tpl]
        logger.end(f"potential_person = {potential_person_list}")
        return potential_person_list


    def get_number_of_invitations_sent_in_the_last_24_hours(self,message_id) -> int:
        logger.start(f"get number of invitations sent in the last 24_hours for message id={message_id}")
        query = (
            f"SELECT COUNT(*) FROM message_outbox_view WHERE message_id = {message_id} AND return_code=0 AND updated_timestamp - INTERVAL 24 HOUR"
        )
        self.schema_name = "message"
        self.cursor.execute(query)
        number_of_invitations =  self.cursor.fetchall()
        logger.end(f"number_of_invitations={number_of_invitations}")
        return number_of_invitations[0][0]


    def get_number_of_invitations_to_send(self,message_id) -> int:
        logger.start()
        multiplier = 0.1
        invitations_sent_in_the_last_24_hours = self.get_number_of_invitations_sent_in_the_last_24_hours(message_id) * multiplier
        logger.end(f"number_of_invitations_to_send={invitations_sent_in_the_last_24_hours}")
        return invitations_sent_in_the_last_24_hours