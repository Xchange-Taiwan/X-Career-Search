import json
from enum import Enum
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

    def to_json(self) -> Dict:
        dao_dict = {}
        for field, value in self.__dict__.items():
            if value is None:
                continue
            if isinstance(value, str) and value == '':
                continue
            if isinstance(value, Enum):
                dao_dict[field] = value.value
                continue
            dao_dict[field] = value
        
        return json.dumps(dao_dict)

    def remove_empty_strings(self):
        for field, value in self.__dict__.items():
            if isinstance(value, str) and value == '':
                setattr(self, field, None)


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
