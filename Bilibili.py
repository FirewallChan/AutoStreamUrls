import requests

class Bilibili:

    Header = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
    }
    cid = ''
    Url ={
        "live_url":"http://api.live.bilibili.com/room/v1/Room/playUrl"
    }
    StreamUrls = []

    def __init__(self,uid:str) -> None:
        self.uid = uid
        self.Url["room_id"] = f"http://api.live.bilibili.com/live_user/v1/Master/info?uid={uid}"
        res = requests.get(self.Url["room_id"],headers=self.Header).json()
        if res['code'] == 1:
            raise Exception("UID Error!")
        self.cid = res['data']['room_id']
        self.Url["live_status"] = f"http://api.live.bilibili.com/room/v1/Room/room_init?id={self.cid}"

    def GetLiveStatus(self) -> bool:
        res = requests.get(self.Url["live_status"],headers=self.Header).json()
        if res['code'] == 0 and res['data']['live_status'] == 1:
            return True
        elif res['data']['live_status'] != 1:
            return False
        else:
            raise Exception("The room doesn't exist!")

    def GetStreamUrls(self) -> str:
        param = {
            'cid':self.cid,
            'platform':'h5',
            'quality':4
        }
        res = requests.get(self.Url["live_url"],params=param,headers=self.Header).json()
        if res['code'] == 19002003:
            raise Exception("The room doesn't exist!")
        elif res['code'] == -400:
            raise Exception("Params are wrong!")
        else:
            self.StreamUrls = res['data']['durl']
            return res['data']['durl']