from typing import Dict


_USER_TAG_NESTED_PROPS = {
    "tag_id": {"type": "long"},
    "kind": {"type": "keyword"},
    "intent": {"type": "keyword"},
    "subject_group": {"type": "keyword"},
    "subject": {
        "type": "text",
        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
    },
    "language": {"type": "keyword"},
    "desc": {"type": "object", "dynamic": True},
    # NULL on top-level group rows, non-NULL on leaves. Keyword so filters
    # can target group-level buckets.
    "parent_subject_group": {"type": "keyword"},
}


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

            "user_tags": {
                "type": "nested",
                "properties": _USER_TAG_NESTED_PROPS,
            },

            "experiences": {
                "type": "nested",
                "properties": {
                    "id": {"type": "integer"},
                    "category": {"type": "keyword"},
                    "order": {"type": "integer"},
                    "mentor_experiences_metadata": {"type": "object", "dynamic": True},
                },
            },
        }
    },
}
