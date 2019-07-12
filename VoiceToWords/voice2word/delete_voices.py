# coding=gbk
import os

# 作者：邹鑫、石亮禾
# 删除音源文件里的多余音频文件
def remove(suffix):
    filearray = []
    address=os.getcwd()
    f_list = os.listdir(address)
    for fileNAME in f_list:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(fileNAME)[1] == suffix:
           filearray.append(fileNAME)
    # 以上是从pythonscripts文件夹下读取所有excel表格，并将所有的名字存储到列表filearray
    print("在默认文件夹下有%d个文档" % len(filearray))
    ge = len(filearray)

    for i in range(ge):
        fname = filearray[i]
        os.remove(fname)
    print('remove  successful' )

# remove(".wav")