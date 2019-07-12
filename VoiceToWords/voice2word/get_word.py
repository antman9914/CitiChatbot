# coding=gbk
# ���ߣ����Ρ�ʯ����
from voice2word import Global, format_transfer, delete_voices, download_voice
from aip import AipSpeech


class Converter:
    def __init__(self):
        self._client = AipSpeech(Global.get_app_id(), Global.get_api_key(), Global.get_secret_key())

    # ʶ�𱾵��ļ�
    # file string:�ļ���
    # client client����
    # dev_pid int ����id
    # format string ��Ƶ��ʽ
    def __recognize(self, file, dev_pid, format):
        # ��ȡ�ļ�
        def get_file_content(file_path):
            with open(file_path, 'rb') as fp:
                return fp.read()

        res = self._client.asr(get_file_content(file), format, 16000, {
            'dev_pid': dev_pid,
        })
        # 3301 ���ʹ���
        # 3305 16000�Ĳ�������Ƶʱ������30s
        # 3308 ��Ƶ������������60s
        if res["err_no"] == 0:
            return res["result"]
        elif res["err_no"] == 3301:
            return "error 3301"
        elif res["err_no"] == 3305:
            return "error 3305"
        elif res["err_no"] == 3308:
            return "error 3308"

    def get_words(self, url):
        # �������amr�ļ�
        delete_voices.remove(".amr")

        # �����ļ�
        download_voice.download_by_path(url, "voice.amr")

        # �ļ���ʽת��
        pcm = format_transfer.amr2pcm("voice.amr")

        # ��ý��
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
