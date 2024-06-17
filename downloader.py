import requests
from bs4 import BeautifulSoup
import re
import sys

def get_loom_video_url(share_url):
    response = requests.get(share_url)
    if response.status_code != 200:
        print(f"Failed to retrieve page: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    script_tags = soup.find_all('script')
    video_url = None

    for script in script_tags:
        if script.string and 'window.__LoomShare__' in script.string:
            match = re.search(r'"cdnUrl":"(https:[^"]+)"', script.string)
            if match:
                video_url = match.group(1).replace('\\u002F', '/')
                break

    if not video_url:
        print("Could not find video URL in the page scripts. Checking meta tags.")
        meta_tag = soup.find('meta', property="og:video")
        if meta_tag:
            video_url = meta_tag["content"]
    
    return video_url

def download_video(video_url, output_filename):
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        with open(output_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Video downloaded successfully as {output_filename}")
    else:
        print(f"Failed to download video: {response.status_code}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 downloader.py <loom_share_url>")
        sys.exit(1)

    share_url = sys.argv[1]
    output_filename = "loom_video.mp4"

    video_url = get_loom_video_url(share_url)
    if video_url:
        print(f"Direct video URL: {video_url}")
        download_video(video_url, output_filename)
    else:
        print("Failed to retrieve the video URL.")
