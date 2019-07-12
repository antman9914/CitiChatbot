# coding=gbk
# 作者：邹鑫、石亮禾
from voice2word import Global, format_transfer, delete_voices, download_voice
from aip import AipSpeech


class Converter:
    def __init__(self):
        self._client = AipSpeech(Global.get_app_id(), Global.get_api_key(), Global.get_secret_key())

    # 识别本地文件
    # file string:文件名
    # client client对象
    # dev_pid int 语言id
    # format string 音频格式
    def __recognize(self, file, dev_pid, format):
        # 读取文件
        def get_file_content(file_path):
            with open(file_path, 'rb') as fp:
                return fp.read()

        res = self._client.asr(get_file_content(file), format, 16000, {
            'dev_pid': dev_pid,
        })
        # 3301 音质过差
        # 3305 16000的采样率音频时长高于30s
        # 3308 音频过长，高于了60s
        if res["err_no"] == 0:
            return res["result"]
        elif res["err_no"] == 3301:
            return "error 3301"
        elif res["err_no"] == 3305:
            return "error 3305"
        elif res["err_no"] == 3308:
            return "error 3308"

    def get_words(self, url):
        # 清除所有amr文件
        delete_voices.remove(".amr")

        # 下载文件
        download_voice.download_by_path(url, "voice.amr")

        # 文件格式转换
        pcm = format_transfer.amr2pcm("voice.amr")

        # 获得结果
        res = self.__recognize(pcm, 1536, "pcm")

        return res


# delete_voices.remove()
# converter = Converter()
# pcm = format_transfer.wav2pcm("v3.wav")
# # pcm = format_transfer.wav2pcm("voice.amr")
# res = converter.recognize(pcm, 1536, "pcm")
# # res = converter.recognize("v2.pcm", 1536, "pcm")
# print(res)
# c = Converter()
# res = c.recognize("voice.pcm",)
# res = c.get_words("https://api.weixin.qq.com/cgi-bin/media/get?access_token=23_r71wkIzje7RNunfdC_3UVpWkGzk4Ak68a0wAD4bYFkqhwephJMlMj2kkLStTpVu7-Zi42z6kh0T2eAtYI48t_wjSjOO8MM0deAHQxmEd2M5Csfze2PDBXJ-x2qALFIcAHAGAD&media_id=dABM-WBO-UJTrrg20-d4UF3HBuazXzP0Tvm3ZFHdYs4b9vzwIj21klAoGCUCFhbi")
# print(res)
