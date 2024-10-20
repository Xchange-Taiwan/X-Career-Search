from fastapi import (
    APIRouter,
    Request, Depends,
)
from ...domain.search.service.search_service import SearchService
from ...infra.api.opensearch import OpenSearch
from ...domain.user.model.user_model import *
from ..req.search_internal import *
from ..res.response import *
from ...config.conf import *
from ...config.exception import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


router = APIRouter(
    prefix='/internal',
    tags=['Post Mentor to OpenSearch'],
    responses={404: {'description': 'Not found'}},
)
opensearch = OpenSearch()
_search_service = SearchService(
    opensearch=opensearch,
)


@router.post('/mentor', status_code=status.HTTP_201_CREATED,
             responses=post_response('mentor', ProfileVO))
async def post_mentor_to_opensearch(
        body: ProfileDTO = Depends(post_mentor),
):
    res = await _search_service.send_mentor(body=body)
    print(res)
    if res.get("status_code") == 200:
        return res_success(data=json.loads(res.get('body')))
    else:
        raise ClientException(
            msg=f"{res.get('body')}", code=f"{res.get('status_code')}")
