import youtube_dl
import requests


async def audio(url):
    ydl = youtube_dl.YoutubeDL({"outtmpl": "%(id)s.%(ext)s"})

    with ydl:
        result = ydl.extract_info(
            f"{url}",
            download=False,  # We just want to extract the info
        )

    if "entries" in result:
        # Can be a playlist or a list of videos
        video = result["entries"][0]
    else:
        # Just a video
        video = result

    audio = video["formats"][2]["url"]

    # video = video["formats"][-2]["url"]
    response = requests.get(audio, allow_redirects=True)

    open("audio/audio.mp3", "wb").write(response.content)

    return True


async def video(url):
    ydl = youtube_dl.YoutubeDL({"outtmpl": "%(id)s.%(ext)s"})

    with ydl:
        result = ydl.extract_info(
            f"{url}",
            download=False,  # We just want to extract the info
        )

    if "entries" in result:
        # Can be a playlist or a list of videos
        video = result["entries"][0]
    else:
        # Just a video
        video = result

    # audio = video["formats"][2]["url"]

    video = video["formats"][-1]["url"]
    response = requests.get(video, allow_redirects=True)

    # f = open("video/video.mp4", "wb").write(response.content)
    with open("video/video.mp4", "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

    return True


# mp4("https://youtu.be/QkPxefOSRic")
# print("done")
