import urllib.request

# 作者：邹鑫
# 作用：从一个url下载音频文件
def download_by_path(from_url,to_path):
    conn = urllib.request.urlopen(from_url)
    f = open(to_path, 'wb')
    f.write(conn.read())
    f.close()
    return 0

# download_by_path("http://m7.music.126.net/20190630085922/2fc73d5779f8d85d1ea423d3c2c006c2/ymusic/07fa/a2a1/35ea/732937117d6d0a8c13a81bb40184662e.mp3","voice.mp3")
# download_by_path("aa","voice.amr")