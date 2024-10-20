import os
from dotenv import load_dotenv
load_dotenv()

OPENSERACH_DOMAIN_ENDPOINT = os.getenv('OPENSERACH_DOMAIN_ENDPOINT', '')
OPENSERACH_USERNAME = os.getenv('OPENSERACH_USERNAME', '')
OPENSERACH_PASSWORD = os.getenv('OPENSERACH_PASSWORD', '')
