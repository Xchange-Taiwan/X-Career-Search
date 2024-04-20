import logging as log
from typing import List, Optional

from pydantic import BaseModel

from ....config.conf import *
from ....config.constant import *
from ...user.model.common_model import ProfessionDTO, ProfessionVO
from ...user.model.user_model import *

log.basicConfig(filemode="w", level=log.INFO)


class MentorProfileDTO(BaseModel):
    personal_statement: Optional[str]
    about: Optional[str]
    # TODO: enum
    seniority_level: Optional[str] = []
    expertises: Optional[List[ProfessionDTO]] = []


class MentorProfileVO(ProfileVO):
    personal_statement: Optional[str]
    about: Optional[str]
    # TODO: enum
    seniority_level: Optional[str] = []
    expertises: Optional[List[ProfessionVO]] = []
