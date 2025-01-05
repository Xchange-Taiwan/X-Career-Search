import os
from dotenv import load_dotenv
load_dotenv()

OPENSERACH_DOMAIN_ENDPOINT = os.getenv('OPENSERACH_DOMAIN_ENDPOINT', '')
OPENSERACH_USERNAME = os.getenv('OPENSERACH_USERNAME', '')
OPENSERACH_PASSWORD = os.getenv('OPENSERACH_PASSWORD', '')

# resource probe cycle secs
PROBE_CYCLE_SECS = int(os.getenv("PROBE_CYCLE_SECS", 3))

# sqs/event bus conf
MQ_CONNECT_TIMEOUT = int(os.getenv("MQ_CONNECT_TIMEOUT", 10))
MQ_READ_TIMEOUT = int(os.getenv("MQ_READ_TIMEOUT", 10))
MQ_MAX_ATTEMPTS = int(os.getenv("MQ_MAX_ATTEMPTS", 3))

# sqs
# for retry failed pub events
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL', 'https://sqs.{REGION}.amazonaws.com/{ACCOUNT_ID}/{QUEUE_NAME}')
SQS_DEAD_LETTER_QUEUE_URL = os.getenv('SQS_DEAD_LETTER_QUEUE_URL', 'https://sqs.{REGION}.amazonaws.com/{ACCOUNT_ID}/{DEAD_LETTER_QUEUE_NAME}')
SQS_MAX_MESSAGES = int(os.getenv('SQS_MAX_MESSAGES', 10))
SQS_WAIT_SECS = int(os.getenv('SQS_WAIT_SECS', 20))
