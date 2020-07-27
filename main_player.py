from PyQt5.Qt import *

from MusicPlayer.core.spider.request_song import request_song
from MusicPlayer.core.spider.songlist_spider import SongListSpider
from MusicPlayer.core.text_manage.text_omit import text_omit
from MusicPlayer.resource.ui import main2
from MusicPlayer.resource.widget import all_playlist_widget, app_titleItem_widget
from MusicPlayer.resource.widget.all_playlist_widget import PlayListArea
from MusicPlayer.resource.widget.songlist_widget import SongListWidget, SongFrame
from MusicPlayer.core.player.player import Player
import os


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(1000, 670)
        # 使用designer编写的界面
        self.ui = main2.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setupUi()
        # 给自定义定义信号设置槽函数
        self.signal_bind()

    def setupUi(self):
        # 初始化线程类
        self.thread_songlistui = QThread()  # 显示歌单的线程
        self.thread_player = QThread()  # 播放歌曲的线程
        self.thread_download = QThread()   # 下载歌曲的线程
        # 初始化播放器，先将播放器移入线程，再设置线程启动的信号槽，不能反过来，否则程序还是会假死
        self.player = Player(self.ui.player_frame)
        self.player.moveToThread(self.thread_player)
        self.thread_player.started.connect(self.player.run)
        self.thread_player.start()  # 启动线程
        # 初始化下载类，先移入线程，再设置线程启动的信号槽，不能反过来，否则程序还是会假死
        self.download = DownloadSong()
        self.download.moveToThread(self.thread_download)
        self.thread_download.started.connect(self.download.run)
        # 初始化歌单歌曲爬虫，先放入新创建的线程中，再设置线程启动的信号槽，不能反过来，否则程序还是会假死
        self.spider = SongListSpiderThread()
        self.spider.spider_finished[dict].connect(self.setupSongListUi)
        self.spider.moveToThread(self.thread_songlistui)
        self.thread_songlistui.started.connect(self.spider.run)
        # 作为展示区父控件
        self.mainDisplayWidget = self.ui.mainDisplayWidget
        # 创建垂直布局，存放用于展示某功能的控件
        self.v_layout = QVBoxLayout(self.mainDisplayWidget)
        self.v_layout.setContentsMargins(0, 0, 0, 0)

        # 歌单展示
        self.playlist_widget = all_playlist_widget.MainUi()
        self.playlist_widget.setupUi(self.playlist_widget)

        # 歌单控件构建完成槽函数
        def bindfunc():
            # print('绑定事件')
            lis = self.playlist_widget.findChildren(all_playlist_widget.APlayListFrame)
            # 为所有的显示歌单图片的控件绑定点击事件
            for i in lis:
                i.playlist_clicked[dict].connect(self.runSpiderThread)

        self.playlist_area = self.playlist_widget.findChild(PlayListArea)
        self.playlist_area.setup_finished.connect(bindfunc)
        self.playlist_area.emitSignal()

        self.v_layout.addWidget(self.playlist_widget)

    # 在新线程内运行歌单爬虫
    def runSpiderThread(self, dic):
        self.playlist_widget.hide()
        # 在构建歌单控件的时候需要用到
        self.songlist_dic = dic
        # 将需要爬取的歌单id交给爬虫类
        self.spider.setSongistId(dic['id'])
        # 启动线程
        self.thread_songlistui.start()

    # 得到歌曲信息后更新控件
    def setupSongListUi(self, val):
        # 生成界面
        self.slw = SongListWidget(self.songlist_dic, val)
        # 关闭按钮
        btn = self.slw.findChild(QPushButton, 'close_btn')
        # 为新界面关闭按钮绑定槽函数
        btn.clicked.connect(lambda: [self.slw.hide(), self.playlist_widget.show()])
        # 为歌单中的歌曲被双击行为绑定事件
        songs = self.slw.findChildren(SongFrame)
        for song in songs:
            song.double_clicked_song[dict].connect(self.play_song)
        # 添加进布局进行显示
        self.v_layout.addWidget(self.slw)
        # 终止线程
        self.thread_songlistui.terminate()

    # 双击之后触发的播放歌曲的槽函数
    def play_song(self, data):
        # 检查线程运行状态
        if DownloadSong.is_running:
            return
        # 终止线程再让线程重新启动
        self.thread_download.terminate()
        # 先把歌曲信息交给下载器再启动下载线程
        self.download.setSongData(data)
        self.thread_download.start()

    # 为自定义信号绑定槽函数
    def signal_bind(self):
        # 应用最小化，最大化，关闭
        def app_max_func():
            if self.windowState() == Qt.WindowNoState:
                self.setWindowState(Qt.WindowMaximized)
            elif self.windowState() == Qt.WindowMaximized:
                self.setWindowState(Qt.WindowNoState)

        self.ui.app_min_btn.clicked.connect(lambda: self.setWindowState(Qt.WindowMinimized))
        self.ui.app_max_btn.clicked.connect(app_max_func)
        self.ui.app_close_btn.clicked.connect(lambda: self.close())

        # 窗口挪动
        def window_move(point):
            self.move(self.pos() + point)

        self.ui.titleWidget.window_moved.connect(window_move)

        # 音乐下载成功事件
        def download_finished_evt(song_data):
            self.player.download_song(song_data['id'])
            song_show_frame = self.ui.song_show_frame
            # 共两个标签控件， 第一个显示歌名，第二个显示歌手名
            labels = song_show_frame.findChildren(QLabel)
            # 对字符串进行超出省略处理
            labels[0].setText(text_omit(song_data['name'], song_show_frame.width()))
            labels[1].setText(text_omit(song_data['singer'], song_show_frame.width()))
        self.download.download_finished[dict].connect(download_finished_evt)

        # 音乐下载失败事件
        def download_failed_evt():
            mb = QMessageBox(self)
            mb.setWindowTitle('消息提示')
            mb.setStandardButtons(QMessageBox.Yes)
            mb.button(QMessageBox.Yes).setText('好的')
            mb.setText('<h3>音乐播放失败</h3>')
            mb.setInformativeText('<b>可能是版权问题或者网络问题</b>')
            mb.show()
        self.download.download_failed.connect(download_failed_evt)


class SongListSpiderThread(QObject):
    """要在线程中运行的歌单爬虫"""
    spider_finished = pyqtSignal([dict])

    def __init__(self):
        super().__init__()
        self.spider = SongListSpider()

    def setSongistId(self, songlist_id):
        self.songlist_id = songlist_id

    def run(self) -> None:
        # 得到的是字典数据
        result = self.spider.main(self.songlist_id)
        self.spider_finished[dict].emit(result)


class DownloadSong(QObject):
    """要在线程中运行的下载歌曲类"""
    download_finished = pyqtSignal([dict])
    download_failed = pyqtSignal()
    is_running = False

    def __init__(self):
        super().__init__()
        # 用来标识当前程序是不是在运行中

    def setSongData(self, data):
        self.song_data = data
        self.song_id = data['id']

    def run(self):
        # 确认线程运行状态
        # if DownloadSong.is_running:
        #     return
        # 更改属性
        DownloadSong.is_running = True
        # 得到的结果为Ture，则为歌曲正常获取，得到的为False，则获取失败，可能是版权问题造成
        print('开始下载歌曲：', self.song_data['name'])
        result = request_song(self.song_id)
        if result:  # 返回True发送信号，携带歌曲id
            self.download_finished[dict].emit(self.song_data)
        else:   # 返回False发送下载失败
            self.download_failed.emit()
        DownloadSong.is_running = False


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    MainWindow = MyMainWindow()

    MainWindow.show()

    sys.exit(app.exec_())
