import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, field_validator
from ...mentor.model.mentor_model import MentorProfileVO
from ....config.conf import *
from ....config.constant import *
from ....config.exception import *
import logging
from dateutil.parser import isoparse

log = logging.getLogger(__name__)


class SearchMentorProfileDTO(BaseModel):
    search_pattern: Optional[str]
    filter_positions: Optional[List[str]]
    filter_skills: Optional[List[str]]
    filter_topics: Optional[List[str]]
    filter_expertises: Optional[List[str]]
    filter_industries: Optional[str]
    limit: int = PAGE_LIMIT
    cursor: Optional[datetime]

    @field_validator("cursor")
    def validate_cursor_format(cls, value: Optional[datetime]):
        if value is None:
            return value
        try:
            value.isoformat()
        except Exception:
            raise ClientException(msg="Cursor must be in ISO 8601 datetime format")

        return value


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
