import json
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel
from ...user.model.user_model import *
from ...user.model.common_model import (
    ProfessionDTO,
    ProfessionVO,
)
from ....config.conf import *
from ....config.constant import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


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
