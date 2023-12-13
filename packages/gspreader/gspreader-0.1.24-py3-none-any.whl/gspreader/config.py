import os
from dotenv import load_dotenv

load_dotenv()

GSPREADER_GOOGLE_CREDS = os.environ["GSPREADER_GOOGLE_CREDS"] if "GSPREADER_GOOGLE_CREDS" in os.environ else None
GSPREADER_GOOGLE_CREDS_PATH = os.environ["GSPREADER_GOOGLE_CREDS_PATH"] if "GSPREADER_GOOGLE_CREDS_PATH" in os.environ else None
GSPREADER_GOOGLE_CLIENT_EMAIL = os.environ["GSPREADER_GOOGLE_CLIENT_EMAIL"]
