import json
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel
from ...mentor.model.mentor_model import MentorProfileVO
from ....config.conf import *
from ....config.constant import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


class SearchMentorProfileDTO(BaseModel):
    search_pattern: Optional[str]
    filter_positions: Optional[List[str]]
    filter_skills: Optional[List[str]]
    filter_topics: Optional[List[str]]
    filter_expertises: Optional[List[str]]
    filter_industries: Optional[List[str]]
    # sorting_by: SortingBy
    # sorting: Sorting
    # next_id: int


class SearchMentorProfileVO(MentorProfileVO):
    updated_at: Optional[int]
    views: Optional[int]


class SearchMentorProfileListVO(BaseModel):
    mentors: List[SearchMentorProfileVO]
    next_id: Optional[int]


class ShardInfo(BaseModel):
    total: int
    successful: int
    failed: int


class SearchMentorProfileResponseVO(BaseModel):
    _index: str
    _id: str
    _version: int
    result: str
    _shards: ShardInfo
    _seq_no: int
    _primary_term: int
