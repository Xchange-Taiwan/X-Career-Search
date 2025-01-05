import json
import asyncio
import aioboto3
from botocore.exceptions import ClientError
from typing import Callable, Dict
from src.infra.resource.handler import SQSResourceHandler
from src.config.conf import (
    SQS_MAX_MESSAGES,
    SQS_WAIT_SECS,
)
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class SqsMqAdapter:
    def __init__(self, sqs_rsc: SQSResourceHandler):
        self.sqs_rsc = sqs_rsc
        self.sqs_label = self.sqs_rsc.label
        self.ratio = 0.2
        self.delay = float(SQS_WAIT_SECS * self.ratio)

    async def publish_message(self, event: Dict):
        pass

    async def subscribe_messages(self, callee: Callable, **kwargs):
        while True:
            try:
                sqs_rsc = await self.sqs_rsc.access()
                async with sqs_rsc as sqs_client:
                    await self.__receive_batch_messages(sqs_client, callee, **kwargs)
                    await asyncio.sleep(1)
                    log.info(
                        f"SQS[{self.sqs_label}]: listening loop is running"
                    )
            except Exception as e:
                log.error(f"SQS[{self.sqs_label}]: Error in listening loop: {str(e)}")
                await asyncio.sleep(self.delay)


    async def __receive_batch_messages(
        self, sqs_client: aioboto3.Session.client, callee: Callable, **kwargs
    ):
        try:
            response = await sqs_client.receive_message(
                QueueUrl=self.sqs_rsc.queue_url,
                MaxNumberOfMessages=SQS_MAX_MESSAGES,
                WaitTimeSeconds=SQS_WAIT_SECS,
            )

            messages = response.get("Messages", [])
            for message in messages:
                try:
                    log.info(
                        "SQS[%s]: Message received: %s", self.sqs_label, message["Body"]
                    )
                    request_body = json.loads(message["Body"])

                    async def ack():
                        await sqs_client.delete_message(
                            QueueUrl=self.sqs_rsc.queue_url,
                            ReceiptHandle=message["ReceiptHandle"],
                        )

                    # ack: handled by callee
                    request_body.update({"ack": ack})

                    # main process
                    await callee(request_body, **kwargs)
                    # await ack() >> ack: handled by callee
                except Exception as e:
                    log.error(
                        f"SQS[{self.sqs_label}]: Error processing message: {str(e)}"
                    )

            # sleep 1 secs if there's no msgs
            if not messages:
                await asyncio.sleep(1)

        except ClientError as e:
            log.error(
                "SQS[%s]: Error receiving messages: %s", self.sqs_label, e.__str__()
            )
            log.info("SQS[%s]: break loop due to ClientError ...", self.sqs_label)

        except Exception as e:
            log.error("SQS[%s]: Unexpected error: %s", self.sqs_label, e.__str__())
            log.info("SQS[%s]: break loop due to Exception ...", self.sqs_label)
