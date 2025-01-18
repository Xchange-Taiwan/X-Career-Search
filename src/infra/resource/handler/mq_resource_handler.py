import aioboto3
from botocore.config import Config
from src.config.conf import (
    MQ_CONNECT_TIMEOUT,
    MQ_READ_TIMEOUT,
    MQ_MAX_ATTEMPTS,
)
from ._resource_handler import ResourceHandler
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


mq_config = Config(
    connect_timeout=MQ_CONNECT_TIMEOUT,
    read_timeout=MQ_READ_TIMEOUT,
    retries={"max_attempts": MQ_MAX_ATTEMPTS},
)


class SQSResourceHandler(ResourceHandler):

    def __init__(self, session: aioboto3.Session, label: str, queue_url: str):
        super().__init__()
        self.max_timeout = MQ_CONNECT_TIMEOUT

        self.session = session
        self.label = label
        self.queue_url = queue_url

    async def initial(self):
        pass

    async def accessing(self, **kwargs):
        return self.session.client("sqs", config=mq_config)

    # Regular activation to maintain connections and connection pools
    async def probe(self):
        # try:
        #     async with self.session.client("sqs", config=mq_config) as sqs_client:
        #         response = await sqs_client.get_queue_attributes(
        #             QueueUrl=self.queue_url,
        #             AttributeNames=["QueueArn"],
        #         )
        #         log.info(
        #             "Message Queue[SQS] Connection HTTPStatusCode: %s",
        #             response["ResponseMetadata"]["HTTPStatusCode"],
        #         )
        # except Exception as e:
        #     log.error(f"Message Queue[SQS] Connection Error: %s", e.__str__())
        #     await self.initial()
        pass

    async def close(self):
        # log.info("Message Queue[SQS] client is closed")
        pass
