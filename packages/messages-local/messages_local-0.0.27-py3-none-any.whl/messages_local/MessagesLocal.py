from datetime import datetime
from typing import List, Union

from dotenv import load_dotenv
from label_message_local.LabelConstants import LabelsLocalConstants
from label_message_local.LabelMessage import LabelsMessageLocal
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from message_local.MessageImportance import MessageImportance
from message_local.MessageLocal import MessageLocal
from message_local.Recipient import Recipient
from message_local.MessageConstants import AWS_SMS_MESSAGE_PROVIDER_ID, SMS_MESSAGE_CHANNEL_ID
from queue_worker_local.queue_worker import QueueWorker
from sms_message_aws_sns_local.sms_message_aws_sns import SmsMessageAwsSns

load_dotenv()

# TODO Please make sure it defined only onetime in the repo i.e. MessagesLocalConstants
MESSAGE_ACTION_ID = 15
MESSAGE_LOCAL_PYTHON_COMPONENT_ID = ""
MESSAGE_LOCAL_PYTHON_COMPONENT_COMPONENT_NAME = ""
DEVELOPER_EMAIL = 'jenya.b@circ.zone'

object_message = {
    'component_id': MESSAGE_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': MESSAGE_LOCAL_PYTHON_COMPONENT_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}

logger = Logger.create_logger(object=object_message)


class MessagesLocal:
    # no classes type, so the worker can init it with json.
    def __init__(self, default_original_body: str = None, default_subject: str = None,
                 default_importance: int = MessageImportance.MEDIUM.value) -> None:
        self.default_original_body = default_original_body
        self.default_subject = default_subject
        self.default_importance = default_importance

    # This method should be used by Queue Worker
    def send_sync(self, to_recipients: List[dict], cc_recipients: List[dict] = None, bcc_recipients: List[dict] = None,
                  original_body: str = None, importance: int = None,
                  sender_profile_id: int = None, original_subject: str = None,
                  template_id: int = None, user_external_id: int = None, campaign_id: int = None) -> None:
        """send method"""
        original_body = original_body or self.default_original_body
        original_subject = original_subject or self.default_subject
        importance = importance or self.default_importance

        details = {
            "original_body": original_body,
            "to_recipients": to_recipients,
            "cc_recipients": cc_recipients,
            "bcc_recipients": bcc_recipients,
            "sender_profile_id": sender_profile_id,
            "original_subject": original_subject,
            "template_id": template_id,
            "user_external_id": user_external_id,
            "importance": importance,
            "campaign_id": campaign_id
        }
        logger.start("MessagesLocal send_sync()", object=details)
        to_recipients = self._get_recipients(to_recipients)
        cc_recipients = self._get_recipients(cc_recipients)
        bcc_recipients = self._get_recipients(bcc_recipients)

        for recipient in to_recipients:
            # the __class__ can be set only once, but for different recipients we might want different classes
            message_local = MessageLocal(original_body=original_body, original_subject=original_subject,
                                         to_recipients=to_recipients)
            message_recipient_channel_id = message_local.get_message_channel_id(recipient)
            message_recipient_provider_id = message_local.get_message_provider_id(
                message_recipient_channel_id, recipient)
            if message_recipient_channel_id == SMS_MESSAGE_CHANNEL_ID \
                    and message_recipient_provider_id == AWS_SMS_MESSAGE_PROVIDER_ID:
                body = message_local.get_body_after_text_template()[recipient.get_profile_id()]
                message_local.__class__ = SmsMessageAwsSns
                message_local.send(body, [recipient])

        logger.end()

    def send_scheduled(self, to_recipients: List[Recipient], cc_recipients: List[Recipient] = None,
                       bcc_recipients: List[Recipient] = None,
                       start_timestamp: Union[str, datetime] = None, end_timestamp: Union[str, datetime] = None,
                       importance: MessageImportance = None,
                       sender_profile_id: int = None, original_subject: str = None, original_body: str = None,
                       template_id: int = None, user_external_id: int = None, campaign_id: int = None) -> int:
        """The message will be sent any time between start_timestamp and end_timestamp"""
        queue = QueueWorker(schema_name="message", table_name="message_table",
                            view_name="message_outbox_view", id_column_name="message_id")
        if not start_timestamp:
            start_timestamp = datetime.now()
        message_json = {
            "to_recipients": self._recipients_to_json(to_recipients),
            "cc_recipients": self._recipients_to_json(cc_recipients),
            "bcc_recipients": self._recipients_to_json(bcc_recipients),
            "sender_profile_id": sender_profile_id,
            "original_subject": original_subject,
            "original_body": original_body,
            "template_id": template_id,
            "user_external_id": user_external_id,
            "importance": importance.value,
            "campaign_id": campaign_id

        }
        class_json = {"default_original_body": self.default_original_body,
                      "default_subject": self.default_subject,
                      "default_importance": self.default_importance
                      }
        # TODO: we should update the label_id to outbox
        queue_id = queue.push({"function_parameters_json": message_json,
                               "class_parameters_json": class_json,
                               "action_id": MESSAGE_ACTION_ID,
                               "start_timestamp": start_timestamp,
                               "end_timestamp": end_timestamp})
        # TODO: add try catch and ignore duplicates
        LabelsMessageLocal.add_label(LabelsMessageLocal(),
                                     label_id=LabelsLocalConstants.MESSAGE_OUTBOX_LABEL_ID, message_id=queue_id)
        logger.info("Message pushed to the queue successfully", object={"queue_id": queue_id})
        return queue_id

    @staticmethod
    def _get_recipients(recipients: List[dict]) -> List[Recipient]:
        """get recipients"""
        if not recipients:
            return []
        return [Recipient(**recipient) for recipient in recipients]

    @staticmethod
    def _recipients_to_json(recipients: List[Recipient]) -> List[dict]:
        """recipients to json"""
        if not recipients:
            return []
        return [recipient.to_json() for recipient in recipients]
