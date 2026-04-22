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
from ....config.constant import (
    InterestCategory,
    ProfessionCategory,
    SeniorityLevel,
    MentorAction,
)

log = logging.getLogger(__name__)


def _expand_interest_strings(
    items: List[Any], category: InterestCategory, language: Optional[str]
) -> List[Dict[str, Any]]:
    """Map ProfileDTO `List[str]` (subject_group codes) to OpenSearch nested interest docs."""
    lang = language or ""
    out: List[Dict[str, Any]] = []
    for i, raw in enumerate(items):
        if isinstance(raw, dict):
            out.append(raw)
            continue
        if not isinstance(raw, str):
            continue
        out.append(
            {
                "id": i + 1,
                "subject": raw,
                "subject_group": raw,
                "category": category.value,
                "language": lang,
                "desc": {},
            }
        )
    return out


def _expand_expertise_strings(
    items: List[Any], language: Optional[str]
) -> List[Dict[str, Any]]:
    """Map `List[str]` subject_groups to OpenSearch nested `expertises` docs."""
    lang = language or ""
    out: List[Dict[str, Any]] = []
    for i, raw in enumerate(items):
        if isinstance(raw, dict):
            out.append(raw)
            continue
        if not isinstance(raw, str):
            continue
        out.append(
            {
                "id": i + 1,
                "subject": raw,
                "subject_group": raw,
                "category": ProfessionCategory.EXPERTISE.value,
                "language": lang,
                "profession_metadata": {},
            }
        )
    return out


def _profile_doc_for_opensearch(doc: Dict[str, Any], language: Optional[str]) -> Dict[str, Any]:
    """Align HTTP/SQS payload (string lists) with `PROFILES_INDEX_MAPPING` nested fields."""
    if doc.get("interested_positions"):
        doc["interested_positions"] = _expand_interest_strings(
            doc["interested_positions"], InterestCategory.INTERESTED_POSITION, language
        )
    if doc.get("skills"):
        doc["skills"] = _expand_interest_strings(
            doc["skills"], InterestCategory.SKILL, language
        )
    if doc.get("topics"):
        doc["topics"] = _expand_interest_strings(
            doc["topics"], InterestCategory.TOPIC, language
        )
    if doc.get("expertises"):
        doc["expertises"] = _expand_expertise_strings(doc["expertises"], language)
    return doc


class MentorProfileDTO(ProfileDTO):
    """與 X-Career-User `MentorProfileDTO` 相同欄位；下列為寫入索引額外欄位。"""

    personal_statement: Optional[str] = None
    about: Optional[str] = None
    seniority_level: Optional[SeniorityLevel] = None
    expertises: Optional[List[str]] = None
    experiences: Optional[List[Dict]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # SQS routing field – consumed by the Search service command registry;
    # excluded from the OpenSearch document via to_json().
    action: Optional[MentorAction] = None

    class Config:
        from_attributes = True

    # Fields that exist only for SQS routing and must never be persisted to OpenSearch.
    _EXCLUDE_FROM_DOC = {"action"}

    def to_json(self) -> Dict:
        dao_dict = {}
        for key in self.model_fields.keys():
            if key in self._EXCLUDE_FROM_DOC:
                continue
            value = getattr(self, key)
            if value is None:
                continue
            elif isinstance(value, (list, dict)):
                if len(value) == 0:
                    continue
            elif isinstance(value, Enum):
                dao_dict[key] = value.value
                continue
            dao_dict[key] = value

        dao_dict = jsonable_encoder(dao_dict)
        return _profile_doc_for_opensearch(dao_dict, self.language)


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
    experiences: Optional[List[ExperienceVO]] = Field(default_factory=list)
