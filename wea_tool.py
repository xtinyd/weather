import sys, time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPixmap, QColor, QPalette
from PyQt5.QtCore import Qt, QThread
from bs4 import BeautifulSoup
from urllib import request
from images import *

class WeatherThread(QThread):
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

    def mousePressEvent(self, event):
        """ 父类方法重写，用于实现窗口随鼠标拖动 """
        self.__x_offset = event.globalX() - self.pos().x()
        self.__y_offset = event.globalY() - self.pos().y()

    def mouseMoveEvent(self, event):
        """ 父类方法重写，用于实现窗口随鼠标拖动 """
        self.move(event.globalX() - self.__x_offset, event.globalY() - self.__y_offset)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    wea_thread = WeatherThread(win)
    wea_thread.start()
    sys.exit(app.exec())
