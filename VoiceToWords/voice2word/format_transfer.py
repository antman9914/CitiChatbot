# 作者：邹鑫、石亮禾
import os
from voice2word import Global


def wav2pcm(wav_file):
    # 假设 wav_file = "音频文件.wav"
    # wav_file.split(".") 得到["音频文件","wav"] 拿出第一个结果"音频文件"  与 ".pcm" 拼接 等到结果 "音频文件.pcm"
    pcm_file = "%s.pcm" % (wav_file.split(".wav")[0])
    print(pcm_file)
    # 就是此前我们在cmd窗口中输入命令,这里面就是在让Python帮我们在cmd中执行命令
    os.system("%s/ffmpeg -y  -i %s  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s" % (Global.get_ffmpeg_path(),wav_file, pcm_file))
    return pcm_file


def amr2pcm(amr_file):
    # 假设 wav_file = "音频文件.wav"
    # wav_file.split(".") 得到["音频文件","wav"] 拿出第一个结果"音频文件"  与 ".pcm" 拼接 等到结果 "音频文件.pcm"
    pcm_file = "%s.pcm" % (amr_file.split(".amr")[0])
    print(pcm_file)
    # 就是此前我们在cmd窗口中输入命令,这里面就是在让Python帮我们在cmd中执行命令
    os.system("%s/ffmpeg -y  -i %s  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s" % (Global.get_ffmpeg_path(),amr_file, pcm_file))
    return pcm_file


# def speex2pcm(speex_file): # 待测试
#     # 假设 wav_file = "音频文件.wav"
#     # wav_file.split(".") 得到["音频文件","wav"] 拿出第一个结果"音频文件"  与 ".pcm" 拼接 等到结果 "音频文件.pcm"
#     pcm_file = "%s.pcm" % (speex_file.split(".speex")[0])
#     print(pcm_file)
#     # 就是此前我们在cmd窗口中输入命令,这里面就是在让Python帮我们在cmd中执行命令
#     os.system("%s/ffmpeg -y  -i %s  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s" % (
#     Global.get_ffmpeg_path(), speex_file, pcm_file))
#     return pcm_file

# wav2pcm("../aaa.wav")