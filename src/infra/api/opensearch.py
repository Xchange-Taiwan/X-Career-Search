# import awswrangler as wr
import httpx
from ...config.exception import *
from ...config.conf import *
from ...router.res.response import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


class OpenSearch:
    def __init__(self):
        # Init opensearch connection
        # self.connection = None
        # self.http_client = None
        # try:
        # self.connection = wr.opensearch.connect(host=OPENSERACH_DOMAIN_ENDPOINT, port=443,
        #                                         username=OPENSERACH_USERNAME, password=OPENSERACH_PASSWORD)
        self.http_client = httpx.Client(
            base_url=OPENSERACH_DOMAIN_ENDPOINT,
            headers={
                "Content-Type": "application/json"
            },
            auth=(OPENSERACH_USERNAME, OPENSERACH_PASSWORD)
        )
        # except Exception as e:
        #     log.error(
        #         f'Error connection with openseach or httpx client problems: {e}')
