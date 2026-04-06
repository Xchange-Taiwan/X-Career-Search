import logging
from typing import List, Optional

from pydantic import BaseModel, Field

from .common_model import ProfessionVO, InterestListVO
from ....config.conf import DEFAULT_LANGUAGE

log = logging.getLogger(__name__)


class ProfileDTO(BaseModel):
    """與 X-Career-User `ProfileDTO` 欄位一致。"""

    user_id: Optional[int]
    name: Optional[str] = ""
    avatar: Optional[str] = ""
    job_title: Optional[str] = ""
    company: Optional[str] = ""
    years_of_experience: Optional[str] = "0"
    location: Optional[str] = ""
    interested_positions: Optional[List[str]] = Field(default_factory=list)
    skills: Optional[List[str]] = Field(default_factory=list)
    topics: Optional[List[str]] = Field(default_factory=list)
    industry: Optional[str] = ""
    language: Optional[str] = DEFAULT_LANGUAGE
    is_mentor: Optional[bool] = False

    model_config = {
        "from_attributes": True,
    }


class ProfileVO(BaseModel):
    """與 X-Career-User `ProfileVO` 欄位一致（不含 User 專屬 helper）。"""

    user_id: int
    name: Optional[str] = ""
    avatar: Optional[str] = ""
    job_title: Optional[str] = ""
    company: Optional[str] = ""
    years_of_experience: Optional[str] = "0"
    location: Optional[str] = ""
    interested_positions: Optional[InterestListVO] = None
    skills: Optional[InterestListVO] = None
    topics: Optional[InterestListVO] = None
    industry: Optional[ProfessionVO] = None
    onboarding: Optional[bool] = False
    is_mentor: Optional[bool] = False
    language: Optional[str] = DEFAULT_LANGUAGE
