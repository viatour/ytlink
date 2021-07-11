import requests
import shutil
from io import BytesIO
import win32clipboard
from PIL import Image
import urllib.request
import json
import urllib
import pprint


filename = "thumbnail.jpg"


def get_video_data(ytid):
    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % ytid}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        #pprint.pprint(data)
    return data


def save_image(imgurl):
    r = requests.get(imgurl, stream=True)

    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()


ytvideo = input("Youtube link?")
youtube_id = ytvideo.split("=")[1]
videodata = get_video_data(youtube_id)

thumbnail = videodata["thumbnail_url"]
title = videodata["title"]

save_image(thumbnail)


linkplustitle = f"{ytvideo}\n\n{title}"

send_to_clipboard(win32clipboard.CF_UNICODETEXT, linkplustitle)
print("Link and title copied to clipboard!")
choice = input("Want image?")
if choice == "y":
    image = Image.open(filename)

    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    send_to_clipboard(win32clipboard.CF_DIB, data)
    print("Image copied to clipboard!")
else:
    input("Press any key..")

