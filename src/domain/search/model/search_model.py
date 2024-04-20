import logging as log
from typing import List, Optional

from pydantic import BaseModel

from ....config.conf import *
from ....config.constant import *
from ...mentor.model.mentor_model import MentorProfileVO

log.basicConfig(filemode="w", level=log.INFO)


class SearchMentorProfileDTO(BaseModel):
    search_patterns: List[str]
    filter_positions: List[str]
    filter_skills: List[str]
    filter_topics: List[str]
    filter_expertises: List[str]
    filter_industries: List[str]
    sorting_by: SortingBy
    sorting: Sorting
    next_id: int


class SearchMentorProfileVO(MentorProfileVO):
    updated_at: Optional[int]
    views: Optional[int]


class SearchMentorProfileListVO(BaseModel):
    mentors: List[SearchMentorProfileVO]
    next_id: Optional[int]
