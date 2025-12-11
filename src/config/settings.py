# settings.py

import os
from dotenv import load_dotenv

load_dotenv()

# Configuration settings
PROJECT_NAME = "ShortListResumes"
VERSION = "1.0.0"

# Environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///default.db")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MAX_RESUMES = int(os.getenv("MAX_RESUMES", 100))