import json
import os
from datetime import datetime

ARCHIVE_DIR = "archives"
os.makedirs(ARCHIVE_DIR, exist_ok=True)

def save_translation(filename, original, translated, language):
    file_id = datetime.now().strftime("%Y%m%d%H%M%S")
    data = {
        "filename": filename,
        "language": language,
        "original": original,
        "translated": translated,
        "timestamp": file_id
    }
    with open(f"{ARCHIVE_DIR}/{file_id}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return file_id

def list_archives():
    return [f.replace(".json", "") for f in os.listdir(ARCHIVE_DIR) if f.endswith(".json")]

def load_archive(file_id):
    with open(f"{ARCHIVE_DIR}/{file_id}.json", "r", encoding="utf-8") as f:
        return json.load(f)
