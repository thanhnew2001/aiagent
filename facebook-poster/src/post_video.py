import requests
import logging
import time
import os
import random
import schedule
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Facebook API URL and Access Token (Replace with your actual values)
PAGE_ID = "605183966002485"
ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")

FB_API_URL = f"https://graph.facebook.com/v18.0/{PAGE_ID}/videos"

CHUNK_SIZE = 4 * 1024 * 1024  # 4MB chunks

def get_random_quote(quotes_file):
    """Get a random quote from the specified file."""
    with open(quotes_file, 'r') as file:
        quotes = file.readlines()
    return random.choice(quotes).strip() if quotes else None

def get_random_video(video_folder):
    """Get a random video from the specified folder."""
    videos = [os.path.join(video_folder, vid) for vid in os.listdir(video_folder) if vid.endswith(("mp4", "mov"))]
    return random.choice(videos) if videos else None

def upload_video_to_facebook(video_path):
    """Uploads a video to Facebook using chunked upload."""

    # Step 1: Start the upload session
    start_params = {
        "access_token": ACCESS_TOKEN,
        "upload_phase": "start",
        "file_size": os.path.getsize(video_path),
    }

    start_response = requests.post(FB_API_URL, data=start_params)
    start_data = start_response.json()

    if "upload_session_id" not in start_data:
        logging.error(f"Failed to start video upload: {start_data}")
        return

    upload_session_id = start_data["upload_session_id"]
    start_offset = int(start_data["start_offset"])  # 🔹 Convert to integer
    logging.info(f"Started upload session: {upload_session_id}")

    # Step 2: Transfer the video file in chunks
    with open(video_path, "rb") as video_file:
        while True:
            video_file.seek(start_offset)  # 🔹 Now it's an integer
            chunk = video_file.read(CHUNK_SIZE)

            if not chunk:
                break  # No more data to upload

            transfer_params = {
                "access_token": ACCESS_TOKEN,
                "upload_phase": "transfer",
                "upload_session_id": upload_session_id,
                "start_offset": start_offset,  # 🔹 Now it's an integer
            }
            files = {"video_file_chunk": chunk}
            transfer_response = requests.post(FB_API_URL, data=transfer_params, files=files)
            transfer_data = transfer_response.json()

            if "start_offset" not in transfer_data:
                logging.error(f"Failed to transfer video: {transfer_data}")
                return

            start_offset = int(transfer_data["start_offset"])  # 🔹 Convert to integer
            logging.info(f"Transferred chunk, new start_offset: {start_offset}")

    # Step 3: Finish and publish the video
    finish_params = {
        "access_token": ACCESS_TOKEN,
        "upload_phase": "finish",
        "upload_session_id": upload_session_id,
        # get current datetime
        "title": f"{time.strftime('%Y-%m-%d %H:%M:%S')}",
        "description": get_random_quote("../quotes/list.txt")
    }

    finish_response = requests.post(FB_API_URL, data=finish_params)
    finish_data = finish_response.json()

    if "id" in finish_data:
        logging.info(f"✅ Video uploaded successfully! Video ID: {finish_data['id']}")
    else:
        logging.error(f"❌ Failed to finish video upload: {finish_data}")


def job():
    """Scheduled job to upload a random video."""
    video_folder = "../videos"  # Replace with the path to your video folder
    video_path = get_random_video(video_folder)

    if video_path:
        logging.info(f"Uploading video: {video_path}")
        upload_video_to_facebook(video_path)
    else:
        logging.error("No video found in the specified folder.")

if __name__ == "__main__":
    schedule.every(4).hours.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

        