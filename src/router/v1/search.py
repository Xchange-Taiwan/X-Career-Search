from typing import List
from fastapi import (
    APIRouter,
    Request, Depends,
    Header, Path, Query, Body, Form
)
from ...domain.search.model import (
    search_model as search,
)
from ...app._di.injection import _search_service
from ..req.search import *
from ..res.response import *
from ...config.conf import *
from ...config.constant import *
from ...config.exception import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


router = APIRouter(
    prefix='/search/mentors',
    tags=['Search Mentors'],
    responses={404: {'description': 'Not found'}},
)


@router.get('',
            responses=idempotent_response('mentor_list', search.SearchMentorProfileListVO))
async def mentor_list(
    search_pattern: str = Query(None),
    filter_positions: List[str] = Query(None),
    filter_skills: List[str] = Query(None),
    filter_topics: List[str] = Query(None),
    filter_expertises: List[str] = Query(None),
    filter_industries: List[str] = Query(None),
    # sorting_by: SortingBy = Query(SortingBy.UPDATED_TIME),
    # sorting: Sorting = Query(Sorting.DESC),
):
    search_query_dto = SearchMentorProfileDTO(
        search_pattern=search_pattern,
        filter_positions=filter_positions,
        filter_skills=filter_skills,
        filter_topics=filter_topics,
        filter_expertises=filter_expertises,
        filter_industries=filter_industries,
        # sorting_by=sorting_by,
        # sorting=sorting
    )
    query = format_search_mentors_query(search_query_dto)
    res = await _search_service.get_mentor_list(query)
    return res_success(data=res, status_code=200)


@router.get('/{user_id}',
            responses=idempotent_response('get_mentor', search.SearchMentorProfileVO))
async def get_mentor(user_id: int):
    res = await _search_service.get_mentor(user_id)
    return res_success(data=res, status_code=200)
