# coding=gbk
import os

# ���ߣ����Ρ�ʯ����
# ɾ����Դ�ļ���Ķ�����Ƶ�ļ�
def remove(suffix):
    filearray = []
    address=os.getcwd()
    f_list = os.listdir(address)
    for fileNAME in f_list:
        # os.path.splitext():�����ļ�������չ��
        if os.path.splitext(fileNAME)[1] == suffix:
           filearray.append(fileNAME)
    # �����Ǵ�pythonscripts�ļ����¶�ȡ����excel��񣬲������е����ִ洢���б�filearray
    print("��Ĭ���ļ�������%d���ĵ�" % len(filearray))
    ge = len(filearray)

    for i in range(ge):
        fname = filearray[i]
        os.remove(fname)
    print('remove  successful' )

# remove(".wav")