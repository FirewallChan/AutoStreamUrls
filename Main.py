import json
import Utils
import sys
import getopt
import schedule
from Bilibili import Bilibili
from Youtube import Youtube

filePath = "./config.json"
ResPath = "./playList.m3u8"

def GrabBiliUrl(dict:dict):
    res = {}
    for item in dict:
        try:
            liver = Bilibili(dict[item])
            if liver.GetLiveStatus():
                res[item] = liver.GetStreamUrls()
            else:
                item += "(Not Streaming)"
                res[item] = "Blank"
        except Exception as e:
            return e
    return res

def GrabYoutubeUrl(dict:dict,Proxy:str = "127.0.0.1:10808"):
    res = {}
    for item in dict:
        try:
            liver = Youtube(dict[item],Proxy)
            r = liver.getInfo()
            res[r[1]] = r[2]
        except Exception as e:
            item += "(Not Streaming)"
            res[item] = "Blank"
    return res

def Job(filePath,ResPath):
    with open(filePath,"r") as file:
        config = json.load(file)
    bilibili = config["Bilibili"]
    youtube = config["Youtube"]
    bilibiliUrls = GrabBiliUrl(bilibili)
    youtubeUrls = GrabYoutubeUrl(youtube)
    res = {**bilibiliUrls,**youtubeUrls}
    Utils.WriteChannel(res,ResPath)

if __name__ == "__main__":
    try:
        opts,args = getopt.getopt(sys.argv,"hc:o:",["help","config=","outFile="])
    except getopt.GetoptError as e :
        print(e)
        sys.exit()
    if len(opts):
        print(Utils.helpFile)
        sys.exit
    for opt,args in opts:
        if opt == "-h":
            print(Utils.helpFile)
            sys.exit()
        elif opt in ("-c","--config"):
            filePath = args
        elif opt in ("-o","--outFile"):
            ResPath = args
    
    schedule.every(15).minutes.do(Job(filePath,ResPath))