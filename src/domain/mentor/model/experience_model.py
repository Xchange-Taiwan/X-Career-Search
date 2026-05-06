import json
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel
from ....config.constant import *
import logging

log = logging.getLogger(__name__)


class ExperienceDTO(BaseModel):
    category: ExperienceCategory = None
    mentor_experiences_metadata: Dict = {}
    order: int = 0


class ExperienceVO(BaseModel):
    category: ExperienceCategory = None
    mentor_experiences_metadata: Dict = {}
    order: int = 0


class ExperienceListVO(BaseModel):
    experiences: List[ExperienceVO] = []
