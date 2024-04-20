import logging as log
from typing import List, Optional

from pydantic import BaseModel

from .common_model import InterestListVO, ProfessionVO

log.basicConfig(filemode="w", level=log.INFO)


class ProfileDTO(BaseModel):
    name: Optional[str]
    avator: Optional[str]
    timezone: Optional[int]
    industry: Optional[int]
    position: Optional[str]
    company: Optional[str]
    linkedin_profile: Optional[str]
    interested_positions: Optional[List[int]] = []
    skills: Optional[List[int]] = []
    topics: Optional[List[int]] = []


class ProfileVO(BaseModel):
    user_id: int
    name: Optional[str]
    avator: Optional[str]
    timezone: Optional[int]
    industry: Optional[ProfessionVO]
    position: Optional[str]
    company: Optional[str]
    linkedin_profile: Optional[str]
    interested_positions: Optional[List[InterestListVO]] = []
    skills: Optional[List[InterestListVO]] = []
    topics: Optional[List[InterestListVO]] = []
