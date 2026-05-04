import logging
from typing import Optional

from pydantic import BaseModel

from .common_model import ProfessionVO
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
    industry: Optional[ProfessionVO] = None
    onboarding: Optional[bool] = False
    is_mentor: Optional[bool] = False
    language: Optional[str] = DEFAULT_LANGUAGE
