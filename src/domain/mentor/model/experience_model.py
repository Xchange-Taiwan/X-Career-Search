import json
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel
from ....config.constant import *
import logging as log

log.basicConfig(filemode="w", level=log.INFO)


class ExperienceDTO(BaseModel):
    id: Optional[int] = None
    category: ExperienceCategory = None
    mentor_experiences_metadata: Dict = {}
    order: int = 0


class ExperienceVO(BaseModel):
    id: int
    category: ExperienceCategory = None
    mentor_experiences_metadata: Dict = {}
    order: int = 0


class ExperienceListVO(BaseModel):
    experiences: List[ExperienceVO] = []
