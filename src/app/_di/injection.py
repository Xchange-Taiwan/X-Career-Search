from src.infra.resource.manager import (
    aioboto3,
    ResourceManager,
)
from src.infra.resource.handler import *
from src.infra.mq.sqs_mq_adapter import SqsMqAdapter
from src.infra.api.opensearch import OpenSearch
from src.domain.search.service.search_service import SearchService
from src.config.conf import SQS_QUEUE_URL, SQS_DEAD_LETTER_QUEUE_URL

session = aioboto3.Session()
_resource_manager = ResourceManager(
    {
        "user_duplicate_queue_resource": SQSResourceHandler(
            session=session,
            label="subscribe mentor update from user service",
            queue_url=SQS_QUEUE_URL,
        ),
        "user_duplicate_dead_letter_queue_resource": SQSResourceHandler(
            session=session,
            label="subscribe mentor update from DLQ",
            queue_url=SQS_DEAD_LETTER_QUEUE_URL,
        ),
    }
)

queue_rsc: SQSResourceHandler = _resource_manager.get("user_duplicate_queue_resource")
dlq_rsc: SQSResourceHandler = _resource_manager.get("user_duplicate_dead_letter_queue_resource")
_queue_adapter = SqsMqAdapter(sqs_rsc=queue_rsc)
_dlq_adapter = SqsMqAdapter(sqs_rsc=dlq_rsc)

opensearch = OpenSearch()
_search_service = SearchService(opensearch=opensearch)
