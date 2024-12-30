import json
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel
from .common_model import ProfessionVO, InterestListVO
from ....config.constant import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


class ProfileDTO(BaseModel):
    user_id: Optional[int]
    name: Optional[str]
    avatar: Optional[str]
    job_title: Optional[str]
    company: Optional[str]
    years_of_experience: Optional[int] = 0
    region: Optional[str]
    linkedin_profile: Optional[str]
    interested_positions: Optional[List[Union[str]]] = []
    skills: Optional[List[Union[str]]] = []
    topics: Optional[List[Union[str]]] = []
    industries: Optional[List[Union[str]]] = []
    language: Optional[str]


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
