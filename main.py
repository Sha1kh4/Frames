from twikit import Client
from PIL import Image 
import schedule
import time
import requests
import os

# Initialize the Twikit client and load cookies
client = Client('en-US')
client.load_cookies('Monkeyman.json')

# Global variable to keep track of frame number
current_frame = 1

def print_link_by_line_no(filename, line_no):
  """
  Prints the link at the specified line number in the file.
  """
  try:
    with open(filename, 'r') as file:
      lines = file.readlines()
      if 0 <= line_no - 1 < len(lines):
        line = lines[line_no - 1].strip()
        if line and line.startswith('http'):
          print(line)
          return load_image_from_url(line, f"image_{line_no}.jpg")
        else:
          print(f"Line {line_no} does not contain a link.")

      else:
        print(f"Line number {line_no} is out of range.")
  except FileNotFoundError:
    print(f"File {filename} not found.")

def load_image_from_url(url, filename):
  """
  Downloads the image from the URL and saves it as a JPEG file.
  """
  try:
    response = requests.get(url, stream=True)
    if response.status_code == 200:
      with open(filename, 'wb') as file:
        for chunk in response.iter_content(1024):
          file.write(chunk)
      print(f"Image saved to {filename}")
      return filename
    else:
      print(f"Failed to download image. Status code: {response.status_code}")
  except requests.exceptions.RequestException as e:
    print(f"Error downloading image: {e}")
    return None

def tweet():
    global current_frame
    link = print_link_by_line_no('links.txt', current_frame)
    
    # Construct tweet text and media upload
    TWEET_TEXT = f'Frame {current_frame}'
    MEDIA_IDS = [
        client.upload_media(link),
    ]
    
    # Create the tweet
    client.create_tweet(TWEET_TEXT, media_ids=MEDIA_IDS)
    print(f"Tweeted with frame {current_frame}")
    # Delete the image file after tweeting
    if link:
        os.remove(link)
        print(f"Deleted image file {link}")
    
    # Increment frame number for the next tweet
    current_frame += 1

# Schedule tweet to run every 10 minutes
schedule.every(10).minutes.do(tweet)

# Main loop to keep the script running and schedule active
if __name__ == '__main__':
#   tweet()
    while True:
        schedule.run_pending()
        time.sleep(1)
