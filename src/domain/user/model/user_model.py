import json
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel
from .common_model import ProfessionVO, InterestListVO
from ....config.constant import *
import logging as log

log.basicConfig(filemode="w", level=log.INFO)


class ProfileDTO(BaseModel):
    user_id: Optional[int]
    name: Optional[str] = ""
    avatar: Optional[str] = ""
    job_title: Optional[str] = ""
    company: Optional[str] = ""
    years_of_experience: Optional[str] = "0"
    location: Optional[str] = ""
    linkedin_profile: Optional[str] = ""
    interested_positions: Optional[List[Union[str]]] = []
    skills: Optional[List[Union[str]]] = []
    topics: Optional[List[Union[str]]] = []
    industry: Optional[str] = ""
    language: Optional[str] = ""


class ProfileVO(BaseModel):
    user_id: int
    name: Optional[str] = ""
    avatar: Optional[str] = ""
    job_title: Optional[str] = ""
    company: Optional[str] = ""
    years_of_experience: Optional[str] = "0"
    location: Optional[str] = ""
    linkedin_profile: Optional[str] = ""
    interested_positions: Optional[InterestListVO] = None
    skills: Optional[InterestListVO] = None
    topics: Optional[InterestListVO] = None
    industry: Optional[ProfessionVO] = None
    onboarding: Optional[bool] = False
    language: Optional[str]
