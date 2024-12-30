import json
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel
from .experience_model import ExperienceVO
from ...user.model.user_model import *
from ...user.model.common_model import (
    ProfessionListVO,
)
from ....config.conf import *
from ....config.constant import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


class MentorProfileDTO(ProfileDTO):
    personal_statement: Optional[str]
    about: Optional[str]
    seniority_level: Optional[SeniorityLevel]
    expertises: Optional[List[str]]

    class Config:
        from_attributes = True  # orm_mode = True


class ProfessionDTO(BaseModel):
    professions_id: int
    category: Optional[str]
    subject: Optional[str] = ''
    profession_metadata: Optional[Dict] = {}


class MentorProfileVO(ProfileVO):
    personal_statement: Optional[str] = ""
    about: Optional[str] = ""
    seniority_level: Optional[SeniorityLevel] = ""
    expertises: Optional[ProfessionListVO] = None
    experiences: Optional[List[ExperienceVO]] = []
