def get_yt_id(url):
    ytid_length = 11
    if url.startswith("https://www.youtube.com/"):
        ytid = url.split("=")[1][0:ytid_length]
    elif url.startswith("https://youtu.be/"):
        ytid = url.split("/")[3][0:ytid_length]
    return ytid