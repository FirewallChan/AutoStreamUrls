import youtube_dl
import Utils

class Youtube:
    channelName = ""
    ydl_opts = {
        "format":"best"
    }

    def __init__(self,channelID:str,proxyUrl:str = "127.0.0.1:10808") -> None:
        self.ydl_opts["proxy"] = proxyUrl
        self.channelID = channelID
        self.url = f"https://www.youtube.com/channel/{channelID}/live"

    @Utils.Set_TimeOut
    def getInfo(self) -> list:
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(self.url,download=False)
            streamUrl = info["url"]
            Title = info["title"]
            Channel_Name = info ["uploader"]
        return [Channel_Name,Title,streamUrl]