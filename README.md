今天我们做一个基于Python3 + PyQt5的一个天气预报，先来看一下效果图：

![](http://upload-images.jianshu.io/upload_images/4667452-1075b698d883af32.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
整体界面比较简陋，但是这里我们主要把功能实现就行了。
## 工具准备：
- Python3.x
运行本例代码还需要装几个Python3的模块:
```bash
$ pip install pyqt5
$ pip install bs4
$ pip install lxml 
```
- 开发环境呢，我这里用的VSCode，补一张效果图（如果感兴趣的话可以参看[我的Python3开发环境配置]）：
![](http://upload-images.jianshu.io/upload_images/4667452-cedcf02de1b8fe79.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
## 正文开始
### 1.天气信息爬取
在制作天气预报信息显示时，我们首先需要获取预报信息，这里我们准备从[中国天气网](http://www.weather.com.cn)爬取我们所需要的天气信息。具体思路是：
> 1. 获取所在城市码，构造爬取链接
> 2. 使用urllib获取网站html源码
> 3. 分析html源码，获取我们所需的天气信息

大概就上面三条，分析html源码我们使用bs4包所提供的BeautifulSoup进行，关于BeautifulSoup的使用参见[[脚本之家——Python中使用Beautiful Soup库的超详细教程](http://www.jb51.net/article/65287.htm)]。
1. 获取城市码
打开中国天气网，输入你所在的城市名，打开后点击**今天**，注意浏览器上的链接地址。我输入的城市是**西安**，所以地址是：<br>***http://www.weather.com.cn/weather1d/101110101.shtml***<br>其中**101110101**就是西安的城市码，其他城市以此类推。
2. 使用urllib获取网站html源码
```python
from urllib import request

city_code = "101110101"
req = request("http://www.weather.com.cn/weather1d/" + city_code + ".shtml")
# 将网页数据解码为utf-8字符集
html = req.read().decode('utf-8')
# 为了节省调试时间，我们这里直接将网页源码保存至本地文件tmp.html中
f = open("tmp.html", "w", encoding="utf-8")
f.write(html)
f.close()
```
3. 分析html源码，获取我们所需的天气信息
```python
from bs4 import BeautifulSoup
# 我们使用lxml解析器
soup = BeautifulSoup(open("tmp.html", "r", encoding="utf-8"), "lxml")
# 使用字典保存我们所获取的两组数据
weather = {}
weather['day_wea'] = soup.select('div.t > ul.clearfix > li > p.wea')[0].text
weather['night_wea'] = soup.select('div.t > ul.clearfix > li > p.wea')[1].text
weather['day_tem'] = soup.select('div.t > ul.clearfix > li > p.tem > span')[0].text
weather['night_tem'] = soup.select('div.t > ul.clearfix > li > p.tem > span')[1].text
print(weather)

>>> {'day_wea': '阵雨', 'night_wea': '阵雨', 'day_tem': '30', 'night_tem': '22'}
```
我们所需要的天气信息和温度信息已经获取到了，原始资料准备妥当，开始构建我们的图形显示界面
### 2. 构造图形界面
我们获取的天气信息有两组，分别是当日白天天气信息、当日夜间天气信息，我们准备用3个QHBoxLayout、1个QVBoxLayout、6个QLabel控件完成信息的显示。
布局如下：

|白天|夜间|
|--|--|
|天气图标|天气图标|
|预报+温度|预报+温度|

窗口实现代码如下：
```python
class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.img_label = QLabel()
        self.wea_label = QLabel()

        pal = QPalette()
        pal.setColor(QPalette.WindowText, Qt.white)
        font = QFont("微软雅黑", 10)
        
        # 标题Layout
        title_layout = QHBoxLayout()
        self.day_title = QLabel('白天')
        self.night_title = QLabel('夜间')
        title_layout.addWidget(self.day_title)
        title_layout.addWidget(self.night_title)
         # 设置字体颜色为白色
        self.day_title.setPalette(pal)
        self.night_title.setPalette(pal)
        # 设置对齐方式为居中对齐
        self.day_title.setAlignment(Qt.AlignHCenter)
        self.night_title.setAlignment(Qt.AlignHCenter) 
        # 设置显示字体
        self.day_title.setFont(font)
        self.night_title.setFont(font)
       

        # 天气图标Layout
        img_layout = QHBoxLayout()
        self.day_img_label = QLabel()
        self.night_img_label = QLabel()
        img_layout.addWidget(self.day_img_label)
        img_layout.addWidget(self.night_img_label)

        # 天气信息Layout
        wea_layout = QHBoxLayout()
        self.day_wea_label = QLabel()
        self.night_wea_label = QLabel()
        wea_layout.addWidget(self.day_wea_label)
        wea_layout.addWidget(self.night_wea_label)
        self.day_wea_label.setPalette(pal)
        self.night_wea_label.setPalette(pal)
        # 文本居中对齐
        self.day_wea_label.setAlignment(Qt.AlignHCenter)
        self.night_wea_label.setAlignment(Qt.AlignHCenter)
        self.day_wea_label.setFont(font)
        self.night_wea_label.setFont(font)
       
        layout = QVBoxLayout(self)
        layout.addLayout(title_layout)
        layout.addLayout(img_layout)
        layout.addLayout(wea_layout)

        self.setLayout(layout)
        # 设置窗口属性，去除系统标题栏、隐藏状态栏、置顶显示
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        # 设置窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)
        # 重新调整窗口大小
        self.resize(300, 200)

        # 用于移动窗口
        self.__x_offset = 0
        self.__y_offset = 0

    def mousePressEvent(self, event):
        """ 父类方法重写，用于实现窗口随鼠标拖动 """
        self.__x_offset = event.globalX() - self.pos().x()
        self.__y_offset = event.globalY() - self.pos().y()

    def mouseMoveEvent(self, event):
        """ 父类方法重写，用于实现窗口随鼠标拖动 """
        self.move(event.globalX() - self.__x_offset, event.globalY() - self.__y_offset)

    def update_weather(self, wea):
        """ 更新天气显示 """
        pixmap = QPixmap(self.__get_images__('day_' + wea['day_wea']))
        self.day_img_label.setPixmap(pixmap)
        self.day_wea_label.setText('%s %s℃' % (wea['day_wea'], wea['day_tem']))

        pixmap = QPixmap(self.__get_images__('night_' + wea['night_wea']))
        self.night_img_label.setPixmap(pixmap)
        self.night_img_label.resize(pixmap.size())
        self.night_wea_label.setText('%s %s℃' % (wea['night_wea'], wea['night_tem']))

    def __get_images__(self, wea_str):
        imags = {"day_阵雨":':/images/day_shower.png', "night_阵雨":":/images/night_shower.png",
            "day_多云":':/images/day_cloudy.png', "night_多云":":/images/night_cloudy.png",
            "day_晴":':/images/day_sunny.png', "night_晴":":/images/night_sunny.png",
            }
        return imags[wea_str]
```
> 我们在上面添加了两个新的方法**update_weather(wea)**，我们第一步爬取到的天气信息输入给这个方法，即可对界面显示元素进行更新。还有一个是**__get_images__(wea_str)**，当获取到具体的当日天气后传参给这个函数将返回当前天气信息的图标名称。***PS:我太懒了，所以我只做了阵雨、多云、晴三种天气信息，剩下的按照需求自己完成就行。***

- 为了使我们的天气信息能够自动更新，我们将每隔1小时对中国天气网进行一次天气信息解析，为此我们写了个线程用于完成这个功能。
```python

    # 城市码
    city_codes = {'西安':'101110101'}

    def __init__(self, win):
        super(WeatherThread, self).__init__()
        self.__win = win

    def run(self):
        while True:
            url = self.get_url('西安')
            html = self.get_html(url)
            wea = self.get_data(html)
            self.__win.update_weather(wea)
            print(wea)
            # 等待1小时
            time.sleep(3600)

    def get_url(self, city):
        url = 'http://www.weather.com.cn/weather1d/' + self.city_codes[city] + '.shtml'
        return url

    def get_html(self, url):
        req = request.urlopen(url)
        html = req.read().decode('utf-8')
        return html

    def get_data(self, html):
        weather = {}
        soup = BeautifulSoup(html, 'lxml')
        weather['day_wea'] = soup.select('div.t > ul.clearfix > li > p.wea')[0].text
        weather['night_wea'] = soup.select('div.t > ul.clearfix > li > p.wea')[1].text
        weather['day_tem'] = soup.select('div.t > ul.clearfix > li > p.tem > span')[0].text
        weather['night_tem'] = soup.select('div.t > ul.clearfix > li > p.tem > span')[1].text
        return weather
```
> 城市码我只弄了一种就是西安的，剩下的自己按照我之前介绍的方法获取就行了。
- 图片我是在[懒人图库](http://www.lanrentuku.com/png/1522.html)上找的，图片我使用Qt资源进行存储，贴上qrc代码：
```xml
<RCC version="1.0">
    <qresource prefix="images">
        <file alias="day_shower.png">./images/shower2.png</file>
        <file alias="night_shower.png">./images/shower2_night.png</file>
        <file alias="day_cloudy.png">./images/cloudy3.png</file>
        <file alias="night_cloudy.png">./images/cloudy3_night.png</file>
        <file alias="night_sunny.png">./images/sunny_night.png</file>
        <file alias="day_sunny.png">./images/sunny.png</file>
    </qresource>
</RCC>
```
使用pyrcc5进行资源的处理：
```bash
$ pyrcc5 images.qrc -o images.py
```

最后添上我们的程序入口：
```python
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    wea_thread = WeatherThread(win)
    wea_thread.start()
    sys.exit(app.exec())
```
哦对了，我列一下这个程序所用到的模块：
```python
import sys, time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPixmap, QColor, QPalette
from PyQt5.QtCore import Qt, QThread
from bs4 import BeautifulSoup
from urllib import request
from images import *
```
本例所有代码已上传至github，有兴趣的朋友可以pull下来。<br>https://github.com/xtinyd/weather.git
******

## 结束语
在PyQt5上我也只是个菜鸟，出这个系列教程的目的呢，还是想让自己学到的东西能够用上，不至于学起来那么盲目，另外也希望可以帮助想学习PyQt5的你。附上我的座右铭：

***没有什么是学习学不来的。<br>——skyloveraining***


