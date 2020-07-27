from PyQt5.Qt import *
from MusicPlayer.core.text_manage.text_omit import text_omit
from MusicPlayer.resource.ui import songlist
from MusicPlayer.core.spider.songlist_spider import SongListSpider
from MusicPlayer.core.spider import request_song
import os
import time


class SongListWidget(QFrame):
    completed = pyqtSignal([QFrame])

    def __init__(self, info: dict, songlist_dict: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 歌单信息
        self.info = info
        self.result = songlist_dict
        self.ui = songlist.Ui_Form()
        self.ui.setupUi(self)
        self.setupUi()

    def setupUi(self):
        # 定位到展示歌单图片的控件，设置歌单图片
        self.songlist_pic = self.findChild(QFrame, 'songlist_pic')
        # print(self.songlist_pic)
        img_filename = self.info['img'].split('==/')[1].split('?')[0]
        img_url = os.getcwd() + '\\resource\\images\\playlist_pic\\' + img_filename
        # img_url = os.path.dirname(os.getcwd()) + '\\images\\playlist_pic\\' + img_filename  # 直接运行本文件的路径写法
        self.songlist_pic.setStyleSheet('border-image: url({});'.format(img_url.replace('\\', '/')))  # 这里只能用/，不然显示不出来
        # 定位到展示歌单标题的控件，设置歌单标题
        self.songlist_title = self.findChild(QLabel, 'songlist_title')
        self.songlist_title.setText(self.info['title'])
        # 定位作为到存放歌曲条目的父控件
        self.songlist_qf = self.findChild(QFrame, 'songlist_frame')
        # 创建垂直布局，存放歌曲条目
        v_layout = QVBoxLayout(self.songlist_qf)
        v_layout.setSpacing(0)
        # 创建一个父控件存放歌曲信息的表头
        h_frame = QFrame()
        h_frame.setFixedHeight(25)
        # 创建横向布局，按顺序存放标签，标签内容为歌曲的信息类别
        h_layout = QHBoxLayout(h_frame)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setSpacing(0)
        h_layout.setAlignment(Qt.AlignRight)
        label1 = QLabel('')
        label1.setFixedWidth(50)
        label2 = QLabel('音乐标题')
        label3 = QLabel('歌手')
        label4 = QLabel('时长')
        h_layout.addWidget(label1)
        h_layout.addWidget(label2, 13)
        h_layout.addWidget(label3, 9)
        h_layout.addWidget(label4, 2)
        v_layout.addWidget(h_frame)
        # 遍历歌曲字典，逐个创建布局进行展示
        for index, data in self.result.items():
            # print(index, data)
            # 展示一首歌曲的控件
            frame = SongFrame(index, data)
            v_layout.addWidget(frame)
        # 添加一个空控件保证歌曲铺不满屏幕时样式不会变形
        v_layout.addStretch(1)
        # 设置滚动条
        self.setScrollBar()

        self.completed.emit(self)

    def setScrollBar(self):
        # 滚动条
        self.scrollbar = self.findChild(QScrollBar, 'scrollBar')
        # 滚动区域
        self.area = self.findChild(QScrollArea, 'scrollArea')
        self.scrollbar.setPageStep(self.height())
        # 当滚动区域的滚动条的范围变化时同时更新外部滚动条的范围
        self.area.verticalScrollBar().rangeChanged.connect(lambda val1, val2: self.scrollbar.setRange(val1, val2))
        # 当滚动区域的滚动条的变化时更新外部滚动条的值
        self.area.verticalScrollBar().valueChanged.connect(lambda val: self.scrollbar.setValue(val))
        # 当滚动条的值变化时把值同步到滚动区域的滚动条
        self.scrollbar.valueChanged.connect(lambda val: self.area.verticalScrollBar().setValue(val))


# 创建一首歌曲的控件类
class SongFrame(QFrame, QAbstractButton):
    double_clicked_song = pyqtSignal([dict])

    def __init__(self, index, data):
        super().__init__()
        self.index = index
        self.data = data
        self.setFixedHeight(25)
        self.setMinimumWidth(750)
        self.setStyleSheet('font-size: 12px;')
        self.setProperty('id', data['id'])
        self.setProperty('name', data['name'])
        self.setProperty('singer', data['singer'])
        # self.setFocusPolicy(Qt.ClickFocus)
        self.setupUi()

    def setupUi(self):
        # 创建水平布局，存放歌曲条目的歌曲信息
        h_layout = QHBoxLayout(self)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setSpacing(0)
        # 给自己设置属性，键为id，值为歌曲id号
        self.setProperty('id', self.data['id'])
        if self.index % 2:
            self.setStyleSheet('background-color: rgb(245, 245, 247)')
        else:
            self.setStyleSheet('background-color: rgb(250, 250, 250)')
        no_lb = QLabel(str(self.index + 1))  # 歌曲的编号
        no_lb.setFixedWidth(50)
        no_lb.setAlignment(Qt.AlignCenter)
        self.name_lb = QLabel(self.data['name'])  # 歌曲名称
        self.singer_lb = QLabel(self.data['singer'])  # 演唱者
        self.singer_lb.setStyleSheet('color: rgb(102, 102, 102)')
        len_lb = QLabel(self.data['length'])  # 歌曲时长
        # 将歌曲信息加入横向布局
        h_layout.addWidget(no_lb)
        h_layout.addWidget(self.name_lb, 13)
        h_layout.addWidget(self.singer_lb, 9)
        h_layout.addWidget(len_lb, 2)

    # 重写resize事件
    def resizeEvent(self, evt) -> None:
        super().resizeEvent(evt)
        # 对可能超出控件范围的字符串进行处理
        self.name_lb.setText(text_omit(self.data['name'], int(self.width() / 2 + 50)))
        self.singer_lb.setText(text_omit(self.data['singer'], int(self.width() / 3 + 50)))

    # 重写鼠标事件
    def enterEvent(self, evt) -> None:
        self.setStyleSheet('background-color: rgb(235, 236, 237)')

    def leaveEvent(self, evt) -> None:
        if self.index % 2:
            self.setStyleSheet('background-color: rgb(245, 245, 247)')
        else:
            self.setStyleSheet('background-color: rgb(250, 250, 250)')

    def mouseDoubleClickEvent(self, evt) -> None:
        super().mouseDoubleClickEvent(evt)
        # 整合数据
        data = dict()
        data['id'] = self.property('id')
        data['name'] = self.property('name')
        data['singer'] = self.property('singer')
        # 发送信号
        self.double_clicked_song[dict].emit(data)

    # def focusInEvent(self, evt) -> None:
    #     super().focusInEvent(evt)
    #     self.setStyleSheet('background-color: rgb(277, 227, 229)')


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    dic = {'title': '乐坛“破圈”大佬 | 主副业全能', 'href': 'https://music.163.com/playlist?id=5104104942',
           'img': 'http://p1.music.126.net/wswfwGinA8TZxv97eRgAQw==/109951165125139763.jpg?param=200y200',
           'id': '5104104942'}

    songlist_dict = {
        0:
            {'name': '神奈川空中探訪', 'id': '39745258', 'length': '04:06', 'singer': 'NORIKIYO'},
        1:
            {'name': 'Call\xa0Of\xa0Justice', 'id': '479764117', 'length': '06:26',
             'singer': 'KEN THE 390/DOTAMA/Rude-α/Rei©hi/じょう/Ace/MC☆ニガリ a.k.a 赤い稲妻/Lick-G & KOPERU'},
        2:
            {'name': '超自由', 'id': '1418922380', 'length': '03:02', 'singer': 'あっこゴリラ/大門弥生 (YAYOI DAIMON)'},
        3:
            {'name': 'Gana\xa0Gana\xa0Ganda', 'id': '28465153', 'length': '03:11', 'singer': "THE OTOGIBANASHI'S"},
        4:
            {'name': 'ジャングルクルーズ', 'id': '32619112', 'length': '02:57', 'singer': 'KLOOZ'},
        5:
            {'name': 'No.9', 'id': '41416114', 'length': '03:37', 'singer': '焚巻'},
        6:
            {'name': 'Studiolife', 'id': '28606188', 'length': '04:35', 'singer': 'SALU/GOKU GREEN/T-PABLOW/AKLO'},
        7:
            {'name': '魂の叫び', 'id': '33791663', 'length': '03:59', 'singer': 'Soul Scream'},
        8:
            {'name': 'MAKE\xa0ME\xa0CRAZY', 'id': '451981378', 'length': '03:30', 'singer': '餓鬼レンジャー'},
        9:
            {'name': 'GYAKUSOU', 'id': '1443589405', 'length': '02:04', 'singer': 'kZm'}
    }

    slw = SongListWidget(dic, songlist_dict)
    slw.show()
    sys.exit(app.exec_())
