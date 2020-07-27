from PyQt5.Qt import *
from MusicPlayer.resource.widget.typeitem_widget import TypeItemUi
import csv
import requests
import os
import math
import datetime


class MainUi(QFrame):
    """
    展示所有歌单的控件
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumSize(800, 570)

    def setupUi(self, window):
        # 创建纵向布局
        v_layout = QVBoxLayout()
        v_layout.setContentsMargins(0, 0, 0, 0)
        # self.setLayout(v_layout)

        # 实例化类型栏控件， 放入纵向布局
        type_widget = TypeItemUi()
        v_layout.addWidget(type_widget)

        # 创建横向布局，中间放歌单展示控件，两边放空白控件来应对窗口放大，并加入纵向布局
        h_layout = QHBoxLayout()
        v_layout.addLayout(h_layout)

        # 实例化歌单滚动展示区域控件,放入横向布局，并加入空白占位
        area = PlayListArea()
        area.setMinimumWidth(750)
        h_layout.addStretch(1)
        h_layout.addWidget(area)
        h_layout.addStretch(1)

        # 创建滚动条
        qsb = QScrollBar(Qt.Vertical)
        qsb.setPageStep(window.height())

        # 当滚动区域的滚动条的范围变化时同时更新外部滚动条的范围
        area.verticalScrollBar().rangeChanged.connect(lambda val1, val2: qsb.setRange(val1, val2))
        # 当滚动区域的滚动条的变化时更新外部滚动条的值
        area.verticalScrollBar().valueChanged.connect(lambda val: qsb.setValue(val))
        # 当滚动条的值变化时把值同步到滚动区域的滚动条
        qsb.valueChanged.connect(lambda val: area.verticalScrollBar().setValue(val))

        # 创建一个最外层的横向布局，用来放展示区域和滚动条
        h2_layout = QHBoxLayout()
        h2_layout.setContentsMargins(10, 0, 0, 0)
        h2_layout.addLayout(v_layout)
        h2_layout.addWidget(qsb)

        window.setLayout(h2_layout)

        return window


# 滚动展示所有歌单信息的控件的类
class PlayListArea(QScrollArea):
    # 自定义信号，更新完控件后发出
    setup_finished = pyqtSignal()

    def __init__(self, cols=4, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 一页展示几个歌单
        self.limit = 20
        # 展示列数
        self.cols = cols
        # 当前页数
        self.current_page = 1

        # 以列数和每页歌单个数计算最大页数
        # today = datetime.date.today().strftime("%Y%m%d")  # 获得今天日期的字符串
        # self.path = os.getcwd() + '\\core\\spider_files\\playlist_{}.csv'.format(today)
        self.file_path = os.getcwd() + r'\core\spider\spider_files\playlist_{}.csv'.format('20200714')
        with open(self.file_path, 'r', encoding='utf-8') as f:
        # with open('../../core/spider/spider_files/playlist_20200714.csv', 'r', encoding='utf-8') as f:
            number = len(f.readlines())
            self.max_page = math.ceil(number / self.limit)

        # self.setFixedSize(800, 530)
        self.setWidgetResizable(True)
        # 关闭默认滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)
        self.setupUi()

    def setupUi(self):
        # 实例化歌单展示控件
        qw = self.palyListWidget()
        self.setWidget(qw)
        self.setup_finished.emit()

    # 将当前的歌单放入Widget控件并返回
    def palyListWidget(self) -> QWidget:
        # 创建用来装所有内容的主控件
        qw = QWidget()
        # 创建纵向布局
        v_layout = QVBoxLayout()
        qw.setLayout(v_layout)
        # 创建表格布局，展示歌单图片和标题
        g_layout = QGridLayout()
        g_layout.setVerticalSpacing(0)
        # 把表格布局添加进纵向布局
        v_layout.addLayout(g_layout)

        # 读取爬取的歌单数据
        # today = datetime.date.today().strftime("%Y%m%d")  # 获得今天日期的字符串
        # reader = csv.DictReader(open('../../core/spider_files/playlist_{}.csv'.format(today), 'r', encoding='utf-8'))
        reader = csv.DictReader(open(self.file_path, 'r', encoding='utf-8'))
        # reader = csv.DictReader(open('../../core/spider/spider_files/playlist_20200714.csv', 'r', encoding='utf-8'))
        for i, data in enumerate(reader):
            # 显示选中的页面的限定好的数量的歌单
            if (self.current_page - 1) * self.limit + 1 <= i <= self.limit * self.current_page:
                # 实例化自定义控件
                frame = APlayListFrame(data)

                # no为当前页控件为limit数量控件中的第几个，以0开始，算出所在行和列
                no = i - ((self.current_page - 1) * self.limit + 1)
                row = no // self.cols
                column = no % self.cols

                g_layout.addWidget(frame, row, column)

        # 实例化翻页控件，添加进布局，放在最后一行歌单的下面
        self.page_item = self.pageItem()
        v_layout.addWidget(self.page_item)
        return qw

    # 生成翻页控件
    def pageItem(self) -> QFrame:
        # 根据当前页和最大页数生成页面编号列表
        if self.current_page - 1 >= 5 and self.max_page - self.current_page >= 5:
            self.page_list = list(range(self.current_page - 3, self.current_page + 3 + 1))
            self.page_list.insert(0, '.')
            self.page_list.insert(0, 1)
            self.page_list.append('.')
            self.page_list.append(self.max_page)
        elif self.current_page - 1 <= 4 and self.max_page - self.current_page >= 5:
            self.page_list = list(range(1, self.current_page + 3 + 1))
            self.page_list.append('.')
            self.page_list.append(self.max_page)
        elif self.current_page - 1 >= 5 and self.max_page - self.current_page < 5:
            self.page_list = list(range(self.current_page - 3, self.max_page + 1))
            self.page_list.insert(0, '.')
            self.page_list.insert(0, 1)
        else:
            self.page_list = list(range(1, self.max_page + 1))

        # 创建承载页面按钮的控件
        qf = QFrame()
        # 使用横向布局排列按钮
        h_layout = QHBoxLayout()
        # 横向布局左边的空白区域
        h_layout.addStretch(1)
        qf.setLayout(h_layout)

        # 按照上面生成的页面标号列表顺序创建控件并添加进横向布局
        for i in self.page_list:
            i = str(i)
            # 点代表用省略号折叠过多的页面
            if i == '.':
                wdt = QLabel('…')
            # 当前的页面标号创建成label标签进行展示，和其他页数按钮区分开
            elif int(i) == self.current_page:
                wdt = QLabel(i)
                wdt.setFixedSize(30, 25)
                wdt.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                font = QFont()
                font.setUnderline(True)
                wdt.setFont(font)
                wdt.setStyleSheet('color: rgb(94, 184, 251);')
                # wdt.setStyleSheet('background-color: rgb(94, 184, 251);')
            # 页面按钮
            else:
                wdt = PageButton(i)
                wdt.setFlat(True)
                wdt.setObjectName('page_btn')
                wdt.setProperty('page', i)
                wdt.setFixedHeight(25)

                # 选中页面改变的槽函数
                def page_change(page):
                    self.current_page = page
                    # 重新绘制一遍更新展示内容
                    print('页面切换，开始重新生成控件……')
                    self.setupUi()

                # 此处使用的是自定义信号，用来获取点击按钮上显示的页数
                wdt.page_changed[int].connect(page_change)
            # 将创建的控件添加进横向布局
            h_layout.addWidget(wdt)
        # 创建上一页按钮和下一页按钮
        pre_page = QPushButton('<')
        pre_page.setFixedSize(30, 20)
        pre_page.setCursor(Qt.PointingHandCursor)
        pre_page.setObjectName('pre_page')
        next_page = QPushButton('>')
        next_page.setFixedSize(30, 20)
        next_page.setCursor(Qt.PointingHandCursor)
        next_page.setObjectName('next_page')
        # 插入到布局当中，这里索引是1不是0是因为上面先插入了一个空白区域
        h_layout.insertWidget(1, pre_page)
        h_layout.insertWidget(-1, next_page)
        # 横向布局右边的空白区域
        h_layout.addStretch(1)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setSpacing(0)

        # 点击上一页的槽函数
        def pre_page_change():
            # 当前页数大于1才起作用
            if self.current_page > 1:
                self.current_page -= 1
                print('页面切换，开始重新生成控件……')
                self.setupUi()

        pre_page.clicked.connect(pre_page_change)

        # 点击下一页的槽函数
        def next_page_change():
            # 当前页数小于最大页数才起作用
            if self.current_page < self.max_page:
                self.current_page += 1
                print('页面切换，开始重新生成控件……')
                self.setupUi()

        next_page.clicked.connect(next_page_change)

        return qf

    # 发送自定义信号
    def emitSignal(self):
        self.setup_finished.emit()


# 展示一个歌单的封面和标题的控件
class APlayListFrame(QFrame):
    # 自定义点击信号
    playlist_clicked = pyqtSignal([dict])

    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.info = dict(data)
        # 标记是否点击了图片
        self.flag = False
        self.setupUi()

    def setupUi(self):
        # 歌单的标题
        self.label = QLabel(self.info['title'])
        self.label.setMaximumWidth(140)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignLeft)

        # 显示歌单图片的控件
        self.qf = QFrame()
        # qf.setFrameShape(QFrame.Box)
        self.qf.setCursor(QCursor(Qt.PointingHandCursor))
        self.qf.setFixedSize(140, 140)
        self.qf.setProperty('href', self.info['href'])
        # 提取在href地址的图片id号，用来命名下载的图片，也容易获取设置背景图片的路径
        self.qf.setProperty('img', self.info['img'].split('==/')[1].split('?')[0])
        self.qf.setProperty('id', self.info['id'])

        # 下载歌单封面图片，设置在控件内
        self.download_pic(self.info['img'])
        img_url = os.getcwd().replace('\\', '/') + '/resource/images/playlist_pic/' + self.qf.property(
            'img')  # qss路径比较严格，必须手动将\替换成/
        # img_url = '../images/playlist_pic/' + qf.property('img')
        # print(img_url)
        self.qf.setStyleSheet(f'border-image: url({img_url});')

        self.setFixedSize(160, 200)
        self.setContentsMargins(1, 1, 1, 1)
        # 创建纵向布局，是歌单标题展示在歌单图片下方
        v_layout2 = QVBoxLayout()
        v_layout2.setSpacing(15)
        v_layout2.addWidget(self.qf)
        v_layout2.addWidget(self.label)
        self.setLayout(v_layout2)

    # 下载歌单封面图片
    def download_pic(self, href) -> None:
        # 从href地址提取图片名称
        file_name = href.split('==/')[1].split('?')[0]
        file_url = os.getcwd() + '/resource/images/playlist_pic/' + file_name
        # file_url = '../images/playlist_pic/' + file_name
        # 判断本地是否已经下载该图片
        if os.path.isfile(file_url):
            # print('不用下')
            return
        img = requests.get(href).content
        with open(file_url, 'wb') as f:
            f.write(img)

    # 重写鼠标事件，用户点击歌单图片并且松开时鼠标还在图片之上，才能正常触发事件
    def mousePressEvent(self, evt) -> None:
        super().mouseMoveEvent(evt)

        mouse_x = evt.x()
        mouse_y = evt.y()
        pic_h = self.qf.height()
        pic_w = self.qf.width()
        if 0 < mouse_x < pic_w and 0 < mouse_y < pic_h:
            self.flag = True

    def mouseReleaseEvent(self, evt) -> None:
        super().mouseReleaseEvent(evt)

        if not self.flag:
            return

        self.flag = False  # 必须对flag重新赋值，以免在重新点击触发鼠标事件时的判断造成影响
        mouse_x = evt.x()
        mouse_y = evt.y()
        pic_h = self.qf.height()
        pic_w = self.qf.width()

        if 0 < mouse_x < pic_w and 0 < mouse_y < pic_h:
            try:
                self.playlist_clicked[dict].emit(self.info)
            except Exception as e:
                print(e)


# 换页按钮的类
class PageButton(QPushButton):
    # 自定义信号
    page_changed = pyqtSignal([int])

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        # self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFixedSize(30, 20)
        self.font = QFont()
        self.font.setPointSize(8)
        self.setFont(self.font)
        self.setCursor(Qt.PointingHandCursor)
        self.clicked.connect(self.clicked_evt)

    def clicked_evt(self):
        # 上一页、下一页按钮事件不在这里处理
        if self.text() == '>' or self.text() == '<':
            return
        self.page_changed[int].emit(int(self.text()))


class CreatePlayListFrame(QObject):
    finished = pyqtSignal([object])

    def __init__(self):
        super().__init__()

    def set_data(self, data):
        self.data = data

    def run(self):
        print(1)
        self.frame = APlayListFrame(self.data)
        self.finished[object].emit(self.frame)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    ui = MainUi()
    ui.setupUi(ui)

    ui.show()

    sys.exit(app.exec_())
