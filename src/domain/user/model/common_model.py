import json
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel
from ....config.constant import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


class InterestVO(BaseModel):
    id: int
    category: InterestCategory = None
    language: Optional[str] = None
    subject_group: str = 'unknown'
    subject: Optional[str] = ''
    desc: Optional[Dict] = {}


class InterestListVO(BaseModel):
    interests: List[InterestVO] = []
    language: Optional[str] = None



class ProfessionDTO(BaseModel):
    id: int
    category: ProfessionCategory = None
    language: Optional[str] = ''


class ProfessionVO(ProfessionDTO):
    subject_group: str = 'unknown'
    subject: str = ''
    profession_metadata: Dict = {}
    language: Optional[str] = ''

    class Config:
        from_attributes = True # orm_mode = True


class ProfessionListVO(BaseModel):
    professions: List[ProfessionVO] = []

