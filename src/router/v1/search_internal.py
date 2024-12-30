from fastapi import (
    APIRouter, Depends
)
from ...domain.search.service.search_service import SearchService
from ...infra.api.opensearch import OpenSearch
from ...domain.search.model.search_model import *
from ...domain.mentor.model.mentor_model import MentorProfileDTO
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
             responses=post_response('mentor', SearchMentorProfileResponseVO))
async def post_mentor_to_opensearch(
        body: MentorProfileDTO = Depends(post_mentor),
):
    res = await _search_service.send_mentor(body=body)
    status_code = res.get('status_code', None)
    if status_code in (201, 200):
        return res_success(data=res.get('body').json(), status_code=201)
    elif status_code is None:
        return res_err_format(data=res, status_code=status_code)
    elif 400 <= status_code < 500 or 500 <= status_code < 600:
        return res_err_format(data=res, status_code=status_code)
    else:
        raise ServerException(
            msg=f"{res.get('body')}", code=f"{res.status_code}")
