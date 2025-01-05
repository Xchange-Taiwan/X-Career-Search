from src.infra.resource.manager import (
    aioboto3,
    ResourceManager,
)
from src.infra.resource.handler import *
from src.infra.mq.sqs_mq_adapter import SqsMqAdapter
from src.infra.api.opensearch import OpenSearch
from src.domain.search.service.search_service import SearchService
from src.config.conf import SQS_QUEUE_URL

session = aioboto3.Session()
_resource_manager = ResourceManager(
    {
        "sqs_rsc": SQSResourceHandler(
            session=session,
            label="subscribe mentor update from user service",
            queue_url=SQS_QUEUE_URL,
        ),
    }
)

sqs_rsc: SQSResourceHandler = _resource_manager.get("sqs_rsc")
mq_adapter = SqsMqAdapter(sqs_rsc=sqs_rsc)

opensearch = OpenSearch()
_search_service = SearchService(opensearch=opensearch)
