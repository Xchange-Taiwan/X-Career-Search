import logging as log
from typing import List

from fastapi import APIRouter, Query

from ...config.conf import *
from ...config.constant import *
from ...config.exception import *
from ...domain.search.model import search_model as search
from ..res.response import *

log.basicConfig(filemode="w", level=log.INFO)


router = APIRouter(
    prefix="/search",
    tags=["Search Mentors"],
    responses={404: {"description": "Not found"}},
)


# TODO: read from SEARCH service
@router.get(
    "/mentors",
    responses=idempotent_response(
        "mentor_list", search.SearchMentorProfileListVO
    ),
)
async def mentor_list(
    search_patterns: List[str] = Query(None),
    filter_positions: List[str] = Query(None),
    filter_skills: List[str] = Query(None),
    filter_topics: List[str] = Query(None),
    filter_expertises: List[str] = Query(None),
    filter_industries: List[str] = Query(None),
    sorting_by: SortingBy = Query(SortingBy.UPDATED_TIME),
    sorting: Sorting = Query(Sorting.DESC),
    next_id: int = Query(None),
):
    # TODO: implement
    query = search.SearchMentorProfileDTO(
        search_patterns=search_patterns,
        filter_positions=filter_positions,
        filter_skills=filter_skills,
        filter_topics=filter_topics,
        filter_expertises=filter_expertises,
        filter_industries=filter_industries,
        sorting_by=sorting_by,
        sorting=sorting,
        next_id=next_id,
    )
    return res_success(data=None)
