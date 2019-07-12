此包的主要功能是：

​		根据微信提供的.amr音频文件下载地址，将其下载、解析，并获得语音中的文字输出.



使用步骤:

​		1. 此包实现了.amr文件转化为百度语音识别API所推荐的语音格式，需要下载ffmpeg(压缩包已经放在与此readme.md文件同级的文件夹中)，然后，根据教程对其进行安装，教程链接如下：

​		https://blog.csdn.net/a18852867035/article/details/82053611

​		2. ffmpeg安装完成之后，需要对源代码中的voice2word包下的Global模块中的get_ffmpeg_path()函数进行修改，将返回值改为ffmpeg的bin目录的绝对路径，如，本文的路径为D:/ffmpeg/bin。

​		3. 需要导入百度SDK的包:baidu-aip

​		4. 导入此包后，创建一个Converter对象，并调用其get_word()函数，只需要传入一个参数(self不需要传递)：要下载的.amr文件的url(字符串形式)。返回值即为解析后的文字(字符串形式)。