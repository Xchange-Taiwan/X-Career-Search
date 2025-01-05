from fastapi import (
    APIRouter, Depends
)
from ...app._di.injection import _search_service
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


@router.post('/mentor', status_code=status.HTTP_201_CREATED,
             responses=post_response('mentor', SearchMentorProfileResponseVO))
async def post_mentor_to_opensearch(
        body: MentorProfileDTO = Depends(post_mentor),
):
    res = await _search_service.send_mentor(body=body)
    return res_success(data=res, status_code=201)


@router.delete('/mentor/{user_id}', status_code=status.HTTP_200_OK)
async def delete_mentor_from_opensearch(user_id: int):
    res = await _search_service.delete_mentor(user_id=user_id)
    return res_success(data=res, status_code=200)
