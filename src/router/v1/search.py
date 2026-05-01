from typing import List
from datetime import datetime
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
import logging

log = logging.getLogger(__name__)


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
    filter_industries: str = Query(None),
    filter_offers: List[str] = Query(None),
    limit: int = Query(PAGE_LIMIT),
    cursor: datetime = Query(None),
):
    search_query_dto = SearchMentorProfileDTO(
        search_pattern=search_pattern,
        filter_positions=filter_positions,
        filter_skills=filter_skills,
        filter_topics=filter_topics,
        filter_expertises=filter_expertises,
        filter_industries=filter_industries,
        filter_offers=filter_offers,
        limit=limit,
        cursor=cursor
    )
    # Per-kind filters live on profiles_v2.user_tags, so any filtered query
    # routes to v2. Unfiltered browse stays on v1 to avoid changing default
    # listing behavior.
    use_v2 = any([
        filter_skills,
        filter_topics,
        filter_positions,
        filter_expertises,
        filter_offers,
    ])
    if use_v2:
        query = format_search_mentors_query_v2(search_query_dto)
        index = "profiles_v2"
    else:
        query = format_search_mentors_query(search_query_dto)
        index = "profiles"
    res = await _search_service.get_mentor_list(query, index=index)
    return res_success(data=res, status_code=200)


@router.get('/{user_id}',
            responses=idempotent_response('get_mentor', search.SearchMentorProfileVO))
async def get_mentor(user_id: int):
    res = await _search_service.get_mentor(user_id)
    return res_success(data=res, status_code=200)
