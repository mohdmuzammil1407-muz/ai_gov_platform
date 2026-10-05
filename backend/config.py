import os
import hashlib
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Load environment files reliably regardless current working directory.
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env")

DEFAULT_SECRET_KEY = "dev-only-ai-gov-platform-secret-key-change-me-before-production-2026"
SECRET_KEY = os.getenv("SECRET_KEY", DEFAULT_SECRET_KEY)
if len(SECRET_KEY) < 32:
    SECRET_KEY = hashlib.sha256(SECRET_KEY.encode("utf-8")).hexdigest()
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
STAFF_ADMIN_TOKEN_HOURS = int(os.getenv("STAFF_ADMIN_TOKEN_HOURS", "6"))
CITIZEN_TOKEN_HOURS = int(os.getenv("CITIZEN_TOKEN_HOURS", "24"))
DEFAULT_JWT_TOKEN_HOURS = int(os.getenv("DEFAULT_JWT_TOKEN_HOURS", "2"))

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RESET_PASSWORD_BASE_URL = os.getenv("RESET_PASSWORD_BASE_URL", "http://localhost:5173/reset-password")

