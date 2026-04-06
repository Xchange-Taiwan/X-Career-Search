from typing import Dict

_INTEREST_NESTED_PROPS = {
    "id": {"type": "integer"},
    "subject": {
        "type": "text",
        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
    },
    "subject_group": {"type": "keyword"},
    "category": {"type": "keyword"},
    "language": {"type": "keyword"},
    "desc": {"type": "object", "dynamic": True},
}

PROFILES_INDEX_MAPPING: Dict = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1,
    },
    "mappings": {
        "properties": {
            # ── base profile ────────────────────────────────────────────
            "user_id": {"type": "long"},
            "name": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
            },
            "avatar": {"type": "keyword"},
            "location": {"type": "keyword"},
            "job_title": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
            },
            "company": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
            },
            "years_of_experience": {"type": "keyword"},
            "industry": {"type": "keyword"},
            "language": {"type": "keyword"},
            "is_mentor": {"type": "boolean"},

            # ── mentor-specific ─────────────────────────────────────────
            "personal_statement": {"type": "text"},
            "about": {"type": "text"},
            "seniority_level": {"type": "keyword"},

            # ── timestamps ──────────────────────────────────────────────
            "created_at": {"type": "date"},
            "updated_at": {"type": "date"},

            # ── nested: interests ────────────────────────────────────────
            "interested_positions": {
                "type": "nested",
                "properties": _INTEREST_NESTED_PROPS,
            },
            "skills": {
                "type": "nested",
                "properties": _INTEREST_NESTED_PROPS,
            },
            "topics": {
                "type": "nested",
                "properties": _INTEREST_NESTED_PROPS,
            },

            # ── nested: expertises (professions) ─────────────────────────
            "expertises": {
                "type": "nested",
                "properties": {
                    "id": {"type": "integer"},
                    "subject": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
                    },
                    "subject_group": {"type": "keyword"},
                    "category": {"type": "keyword"},
                    "language": {"type": "keyword"},
                    "profession_metadata": {"type": "object", "dynamic": True},
                },
            },

            # ── nested: mentor_experiences ────────────────────────────────
            # Declared as `nested` (not `object`) so each experience item can be
            # queried independently (e.g. filter by category + metadata together).
            "experiences": {
                "type": "nested",
                "properties": {
                    "id": {"type": "integer"},
                    "category": {"type": "keyword"},  # WORK / EDUCATION / LINK
                    "order": {"type": "integer"},
                    "mentor_experiences_metadata": {"type": "object", "dynamic": True},
                },
            },
        }
    },
}
