import os
import requests

# --- YouTube API ---
YOUTUBE_API_KEY = os.environ["YOUTUBE_API_KEY"]
VIDEO_ID = os.environ["YOUTUBE_VIDEO_ID"]

yt_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={VIDEO_ID}&key={YOUTUBE_API_KEY}"
yt_resp = requests.get(yt_url).json()
view_count = yt_resp["items"][0]["statistics"]["viewCount"]

# --- Reddit Auth ---
auth = requests.auth.HTTPBasicAuth(
    os.environ["REDDIT_CLIENT_ID"],
    os.environ["REDDIT_CLIENT_SECRET"]
)

data = {
    "grant_type": "password",
    "username": os.environ["REDDIT_USERNAME"],
    "password": os.environ["REDDIT_PASSWORD"]
}

headers = {"User-Agent": "YouTubeViewBot/0.1"}
token_resp = requests.post("https://www.reddit.com/api/v1/access_token",
                           auth=auth, data=data, headers=headers).json()

token = token_resp["access_token"]
headers["Authorization"] = f"bearer {token}"

# --- Update Comment ---
comment_id = os.environ["REDDIT_COMMENT_ID"]  # e.g. t1_xyz123
new_text = f"This YouTube video has {view_count} views right now!"

edit_url = "https://oauth.reddit.com/api/editusertext"
payload = {
    "thing_id": comment_id,
    "text": new_text
}

edit_resp = requests.post(edit_url, headers=headers, data=payload)
print("Reddit response:", edit_resp.json())
