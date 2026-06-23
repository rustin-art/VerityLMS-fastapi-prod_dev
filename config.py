import os
from dotenv import load_dotenv
from pathlib import Path

print("!<----Connecting with Hugging Face---->!")

load_dotenv()
####3rd Alternative Using Manual Headers & constructing payload

API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('HUGGINGFACEHUB_API_TOKEN')}",
    "Content-Type": "application/json"
}

print("!<----Connection with Hugging Face Router Successful---->!")

print("!<----Configuring File uploading modules ---->!")

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

print("!<----File uploading modules configuration Successful---->!")
