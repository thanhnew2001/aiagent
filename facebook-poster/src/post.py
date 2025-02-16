import requests
import logging
import time
import os
import random
import schedule

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Facebook API endpoint and access token
FB_API_URL = "https://graph.facebook.com/v18.0/me/photos"
ACCESS_TOKEN = "xxx"  # Replace with your valid access token

def get_random_image(img_folder):
    """Get a random image from the specified folder."""
    images = [os.path.join(img_folder, img) for img in os.listdir(img_folder) if img.endswith(('png', 'jpg', 'jpeg', 'gif'))]
    return random.choice(images) if images else None

def get_random_quote(quotes_file):
    """Get a random quote from the specified file."""
    with open(quotes_file, 'r') as file:
        quotes = file.readlines()
    return random.choice(quotes).strip() if quotes else None

def post_to_facebook(message, image_path):
    """Send a post with a message and photo to Facebook and handle potential errors."""
    payload = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }
    files = {
        "source": open(image_path, "rb")
    }

    try:
        response = requests.post(FB_API_URL, data=payload, files=files)
        response_data = response.json()

        if response.status_code == 200:
            logging.info(f"Successfully posted to Facebook: {response_data}")
            return response_data
        else:
            logging.error(f"Failed to post to Facebook: {response_data}")
            return response_data
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None

def job():
    img_folder = "../img"  # Replace with the path to your img folder
    quotes_file = "../quotes/list.txt"  # Replace with the path to your quotes file

    image_path = get_random_image(img_folder)
    message = get_random_quote(quotes_file)
    
    if image_path and message:
        post_to_facebook(message, image_path)
    else:
        if not image_path:
            logging.error("No images found in the specified folder.")
        if not message:
            logging.error("No quotes found in the specified file.")

if __name__ == "__main__":
    schedule.every(12).hours.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)