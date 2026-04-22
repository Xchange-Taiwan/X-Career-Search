import os
from dotenv import load_dotenv
load_dotenv()

# 與 X-Career-User 預設一致（語系 / ProfileDTO.language）
DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'zh_TW')

OPENSERACH_DOMAIN_ENDPOINT = os.getenv('OPENSERACH_DOMAIN_ENDPOINT', '')
OPENSERACH_USERNAME = os.getenv('OPENSERACH_USERNAME', '')
OPENSERACH_PASSWORD = os.getenv('OPENSERACH_PASSWORD', '')

PAGE_LIMIT = int(os.getenv("PAGE_LIMIT", 9))

# Profile string fields that default to "" and may be absent in legacy OpenSearch documents
PROFILE_STR_DEFAULT_FIELDS = os.getenv('PROFILE_STR_DEFAULT_FIELDS', 'job_title;company')
PROFILE_STR_DEFAULT_FIELDS = PROFILE_STR_DEFAULT_FIELDS.strip().split(';')
