import httpx
from ...config.exception import *
from ...config.conf import *
from ...router.res.response import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


class OpenSearch:
    def __init__(self):
        # Init opensearch connection
        # sync
        self.http_client = httpx.Client(
            base_url=OPENSERACH_DOMAIN_ENDPOINT,
            headers={
                "Content-Type": "application/json"
            },
            auth=(OPENSERACH_USERNAME, OPENSERACH_PASSWORD)
        )
        # async
        # async with httpx.AsyncClient(
        #     base_url=OPENSERACH_DOMAIN_ENDPOINT,
        #     headers={
        #         "Content-Type": "application/json"
        #     },
        #     auth=(OPENSERACH_USERNAME, OPENSERACH_PASSWORD)
        # ) as client:
        #     self.http_client = client
