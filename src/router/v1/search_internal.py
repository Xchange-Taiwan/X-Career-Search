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
    return res_success(data=res, status_code=201)
