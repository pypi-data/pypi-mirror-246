from typing import List
from message_local.MessageLocal import MessageLocal
from message_local.MessageImportance import MessageImportance
from message_local.Recipient import Recipient
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.Logger import Logger
# from api_management_local.api_call import APICallsLocal
# from api_management_local.api_limit import APILimitsLocal


WHATSAPP_MESSAGE_VONAGE_LOCAL_PYTHON_COMPONENT_ID = 173
WHATSAPP_MESSAGE_VONAGE_LOCAL_PYTHON_COMPONENT_NAME = 'send whatsapp-message-local-python-package'

whatsapp_message_local_python_unit_tests_logger_object = {
    'component_id': WHATSAPP_MESSAGE_VONAGE_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': WHATSAPP_MESSAGE_VONAGE_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    "developer_email": "jenya.b@circ.zone"
}
logger = Logger.create_logger(
    object=whatsapp_message_local_python_unit_tests_logger_object)


class WhatsAppMessage(MessageLocal):
    """Whatsapp message"""
    # don't rename the parameters, unless you do that in MessagesLocal.send_sync.message_local.__init__ as well
    def __init__(self, original_body: str, to_recipients: List[Recipient],
                 importance: MessageImportance) -> None:
        super().__init__(original_body=original_body, importance=importance, to_recipients=to_recipients)

    def send(self, recipient: Recipient):
        logger.start()
        data = {
            "to": recipient,
            "message_type": "text",
            "text": self.get_body_after_text_template(recipient),
            "channel": "whatsapp"
        }
        print("whatsapp message sent to recipient: " + str(recipient))
        logger.end()

    def was_read(self) -> bool:
        pass

    def display(self):
        """display message"""
        logger.start()
        logger.info(self.get_body_after_text_template())
        logger.end()

    def _can_send(self) -> bool:
        logger.start()
       # APICallsLocal()._insert_api_call_dict
        logger.end()

    def _after_send_attempt(self) -> None:
        logger.start()
       # APILimitsLocal().get_api_limit_by_api_type_id_external_user_id
        logger.end()
