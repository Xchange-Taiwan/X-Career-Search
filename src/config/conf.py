import os
from dotenv import load_dotenv
load_dotenv()

OPENSERACH_DOMAIN_ENDPOINT = os.getenv('OPENSERACH_DOMAIN_ENDPOINT', 'https://search-xchange-search-local-sfx3k5iwd3r4m2cn7evqtlxdwm.us-east-1.es.amazonaws.com')
OPENSERACH_USERNAME = os.getenv('OPENSERACH_USERNAME', 'queekao')
OPENSERACH_PASSWORD = os.getenv('OPENSERACH_PASSWORD', '9bfLbF9-4#bU@7P')

# resource probe cycle secs
PROBE_CYCLE_SECS = int(os.getenv("PROBE_CYCLE_SECS", 3))

# sqs/event bus conf
MQ_CONNECT_TIMEOUT = int(os.getenv("MQ_CONNECT_TIMEOUT", 10))
MQ_READ_TIMEOUT = int(os.getenv("MQ_READ_TIMEOUT", 10))
MQ_MAX_ATTEMPTS = int(os.getenv("MQ_MAX_ATTEMPTS", 3))

# sqs
# for retry failed pub events
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL', 'https://sqs.ap-northeast-1.amazonaws.com/991681440467/USER_DUPLICATE_QUEUE')
SQS_MAX_MESSAGES = int(os.getenv('SQS_MAX_MESSAGES', 10))
SQS_WAIT_SECS = int(os.getenv('SQS_WAIT_SECS', 20))
