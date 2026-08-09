import os

from dotenv import load_dotenv


load_dotenv()




GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gemini-2.5-flash"
)


# ==========================
# Project Paths
# ==========================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CHROMA_PATH = os.path.join(
    BASE_DIR,
    "chroma_db"
)


UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploaded_docs"
)


DATABASE_PATH = os.path.join(
    BASE_DIR,
    "database",
    "office.db"
)


# ==========================
# Email
# ==========================

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")

EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


# ==========================
# Create Required Folders
# ==========================

os.makedirs(
    CHROMA_PATH,
    exist_ok=True
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    os.path.dirname(DATABASE_PATH),
    exist_ok=True
)