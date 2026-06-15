from typing import Dict


# Five flat keyword[] arrays mirror the buckets exposed on
# MentorProfileVO/DTO at the User service. Filters are simple `terms`
# matches on the canonical subject_group key — no nesting needed.
_BUCKET_FIELDS = (
    "want_position",
    "want_skill",
    "want_topic",
    "have_skill",
    "have_topic",
)


PROFILES_INDEX_MAPPING: Dict = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1,
    },
    "mappings": {
        "properties": {
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

            "personal_statement": {"type": "text"},
            "about": {"type": "text"},
            "seniority_level": {"type": "keyword"},

            "created_at": {"type": "date"},
            "updated_at": {"type": "date"},

            **{field: {"type": "keyword"} for field in _BUCKET_FIELDS},

            "experiences": {
                "type": "nested",
                "properties": {
                    "category": {"type": "keyword"},
                    "order": {"type": "integer"},
                    "mentor_experiences_metadata": {"type": "object", "dynamic": True},
                },
            },
        }
    },
}
