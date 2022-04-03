import signal
import functools


helpFile = '''
Usage: python Main.py -c <config_file> -o <output_file>



-c | --config : 设置想要抓取的主播列表的配置文件，如果不设置则默认使用当前目录下的config.json
-o | --outFile: 设置抓取的直播m3u8地址的文件保存位置，默认保存位置在当前目录下的playList.m3u8
'''


#函数装饰器，可以设置函数的执行时间超过是返回TimeOut,可以修改signal.alarm的数字实现设定超时时间 用法：@Set_TimeOut
def Set_TimeOut(func):
    def handle():
        raise RuntimeError
    
    @functools.wraps(func)
    def To_Do(*args,**kwargs):
        try:
            signal.signal(signal.SIGALRM,handle)
            signal.alarm(5)
            res = func(*args,**kwargs)
            signal.alarm(0)
            return res
        except Exception as e:
            return e
    return To_Do




#从字典将信息写入m3u8的播放列表中，字典的格式为{"key":"url"}
def WriteChannel(ChannelUrls:dict,filePath):
    with open(filePath,"w",encoding="utf-8") as file:
        content = ["#EXTM3U\n"]
        for key in ChannelUrls:
            content.append("#EXTINF:-1,"+key+"\n")
            content.append(ChannelUrls[key]+"\n")
        file.writelines(content)