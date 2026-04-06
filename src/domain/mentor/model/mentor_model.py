import json
import logging
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field

from .experience_model import ExperienceVO
from ...user.model.common_model import ProfessionListVO
from ...user.model.user_model import ProfileDTO, ProfileVO
from ....config.constant import SeniorityLevel

log = logging.getLogger(__name__)


class MentorProfileDTO(ProfileDTO):
    """與 X-Career-User `MentorProfileDTO` 相同欄位；下列為寫入索引額外欄位。"""

    personal_statement: Optional[str] = None
    about: Optional[str] = None
    seniority_level: Optional[SeniorityLevel] = None
    expertises: Optional[List[str]] = None
    personal_links: Optional[Dict] = None
    education: Optional[Dict] = None
    work_experience: Optional[Dict] = None
    experiences: Optional[List[Dict]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True

    def to_json(self) -> Dict:
        dao_dict = {}
        for key in self.model_fields.keys():
            value = getattr(self, key)
            if value is None:
                continue
            elif (
                isinstance(value, str)
                or isinstance(value, list)
                or isinstance(value, dict)
            ):
                if len(value) == 0:
                    continue
            elif isinstance(value, Enum):
                dao_dict[key] = value.value
                continue
            dao_dict[key] = value

        dao_dict = jsonable_encoder(dao_dict)
        return dao_dict


class ProfessionDTO(BaseModel):
    professions_id: int
    category: Optional[str]
    subject: Optional[str] = ""
    profession_metadata: Optional[Dict] = {}


class MentorProfileVO(ProfileVO):
    personal_statement: Optional[str] = ""
    about: Optional[str] = ""
    seniority_level: Optional[SeniorityLevel] = SeniorityLevel.NO_REVEAL
    expertises: Optional[ProfessionListVO] = None
    personal_links: Optional[Dict] = None
    education: Optional[Dict] = None
    work_experience: Optional[Dict] = None
    experiences: Optional[List[ExperienceVO]] = Field(default_factory=list)
