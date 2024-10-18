import os
from dotenv import load_dotenv
load_dotenv()

BATCH = int(os.getenv('BATCH', '10'))
