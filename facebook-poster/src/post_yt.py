import os
import time
import random
import logging
import schedule
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# YouTube API credentials
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRET_FILE = "client_secrets.json"  # Replace with your JSON file
TOKEN_FILE = "token.pickle"

def authenticate_youtube():
    """Authenticate with YouTube API using OAuth 2.0."""
    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)

def get_random_quote(quotes_file):
    """Get a random quote from a file."""
    with open(quotes_file, "r") as file:
        quotes = file.readlines()
    return random.choice(quotes).strip() if quotes else "Enjoy this video!"

def get_random_video(video_folder):
    """Get a random video file from the specified folder."""
    videos = [os.path.join(video_folder, vid) for vid in os.listdir(video_folder) if vid.endswith(("mp4", "mov"))]
    return random.choice(videos) if videos else None

def upload_video_to_youtube(video_path):
    """Uploads a video to YouTube."""
    youtube = authenticate_youtube()

    title = f"Uploaded on {time.strftime('%Y-%m-%d %H:%M:%S')}"
    description = get_random_quote("../quotes/list.txt")

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": description,
                "description": description,
                "tags": ["fun", "random", "video"],
                "categoryId": "22",  # Category ID for Entertainment
            },
            "status": {
                "privacyStatus": "public",  # Options: "public", "private", "unlisted"
            },
        },
        media_body=MediaFileUpload(video_path, chunksize=-1, resumable=True),
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            logging.info(f"Upload Progress: {int(status.progress() * 100)}%")

    if response:
        logging.info(f"✅ Video uploaded successfully! Video ID: {response['id']}")

def job():
    """Scheduled job to upload a random video to YouTube."""
    video_folder = "../videos"
    video_path = get_random_video(video_folder)

    if video_path:
        logging.info(f"Uploading video: {video_path}")
        upload_video_to_youtube(video_path)
    else:
        logging.error("No video found in the specified folder.")

if __name__ == "__main__":
    schedule.every(1).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
