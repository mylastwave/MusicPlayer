from PyQt5.Qt import *
from MusicPlayer.core.spider.request_song import request_song
import pygame
import os
from mutagen.mp3 import MP3


class Player(QObject):
    """播放歌曲的类"""
    def __init__(self, frame):
        super().__init__()
        # 初始化pygame音乐播放器模块
        pygame.mixer.init()
        # 播放器是否有第一次播放
        self.first_played = False
        # 歌曲是否在播放
        self.is_playing = False
        # 歌曲进度，歌曲长度
        self.song_pos = 0
        self.song_length = 0
        # 定时器
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timer_evt)
        self.timer.start()
        # 接收播放器控件
        self.frame = frame
        # 播放器子控件
        # 播放按钮
        self.play_btn = self.frame.findChild(QPushButton, 'play_song_btn')
        self.play_btn.clicked.connect(self.play_btn_evt)
        # 上一曲按钮
        self.pre_btn = self.frame.findChild(QPushButton, 'pre_song_btn')
        # self.pre_btn.clicked.connect(lambda: print('上一曲'))
        # 播放进度条
        self.play_progressbar_slider = self.frame.findChild(QSlider, 'play_progressbar_slider')
        self.play_progressbar_slider.sliderPressed.connect(self.play_slider_pressed_evt)
        self.play_progressbar_slider.sliderReleased.connect(self.play_slider_released_evt)
        # 静音按钮
        self.mute_btn = self.frame.findChild(QPushButton, 'mute_btn')
        self.mute_btn.clicked.connect(self.mute_btn_evt)
        # 设置音量
        self.volume = 100
        self.is_mute = False
        self.set_volume(self.volume)
        # 音量条
        self.play_volume_slider = self.frame.findChild(QSlider, 'play_volume_slider')
        self.play_volume_slider.setRange(0, 100)
        self.play_volume_slider.setValue(self.volume)
        self.play_volume_slider.valueChanged.connect(self.volume_bar_value_changed_evt)
        # 设置一次歌曲id
        self.song_id = None
        # self.setSongId()
        print('播放器模块加载成功')

    # 音量条数值变化事件
    def volume_bar_value_changed_evt(self, val):
        self.set_volume(val)

    # 静音按钮点击事件
    def mute_btn_evt(self):
        if self.is_mute:
            self.is_mute = False
            self.set_volume(self.volume)
            self.play_volume_slider.setValue(self.volume)
        else:
            self.is_mute = True
            self.set_volume(self.volume)
            self.play_volume_slider.setValue(0)

    # 播放进度条按钮按下事件
    def play_slider_pressed_evt(self):
        # 歌曲id不为空 继续执行
        if self.song_id:
            self.pause()

    # 播放进度条按钮松开事件
    def play_slider_released_evt(self):
        # 歌曲id不为空 继续执行
        if not self.song_id:
            return
        self.song_pos = self.play_progressbar_slider.value()
        # 进度更新后马上更新一次时间
        self.update_song_pos()
        self.play(start=self.song_pos)
        self.play_btn.paint_btn(pause=False)

    # 播放/暂停按钮事件
    def play_btn_evt(self):
        # 当前进度为0则播放歌曲，不是0就执行暂停或者继续播放操作
        if self.song_pos == 0:
            # 歌曲id不为空 继续执行
            if self.song_id:
                # print('从头播放')
                self.load_song()
                self.play()
                self.play_btn.paint_btn(pause=False)
        else:
            if self.is_playing:
                self.pause()
            else:
                self.unpause()

    # 将事件转换成00:00的钟表格式
    @staticmethod
    def tf_song_tmp(val) -> str:
        val = int(val)
        m, s = divmod(val, 60)
        minute = ('{}' if m > 9 else '0{}').format(m)
        second = ('{}' if s > 9 else '0{}').format(s)
        result = '{}:{}'.format(minute, second)
        return result

    # 将转化成分秒的时间更新到label标签中显示进度
    def update_song_pos(self):
        result = Player.tf_song_tmp(self.song_pos)
        self.frame.findChild(QLabel, 'song_pos_label').setText(result)
        self.play_progressbar_slider.setValue(self.song_pos)

    # 计时器事件
    def timer_evt(self):
        if self.is_playing:
            # 当播放进度到达歌曲长度后将进度重置为0，没到达就将进度加1
            if self.song_pos >= self.song_length - 1:  # 减1是为了不让进度不会超过长度一秒
                self.song_pos = 0
                self.is_playing = False
                self.play_btn.paint_btn(pause=True)
            else:
                self.song_pos += 1
            self.update_song_pos()

    # 设置歌曲id
    def setSongId(self, song_id):
        self.song_id = song_id

    # 线程开启时执行的函数
    def run(self):
        self.load_song()  # 这里加载一次目的在变更播放进度条

    # 加载歌曲
    def load_song(self):
        if not self.song_id:
            return
        self.file_url = os.getcwd() + r'\core\spider\spider_files\music\{}.mp3'.format(self.song_id)
        music = MP3(self.file_url)
        pygame.mixer.music.load(self.file_url)
        self.song_length = music.info.length
        result = Player.tf_song_tmp(music.info.length)
        # 将歌曲时长显示在label标签
        self.frame.findChild(QLabel, 'song_length_label').setText(result)
        # 更新播放进度条控件的范围
        self.play_progressbar_slider.setRange(0, self.song_length)

    # 播放
    def play(self, loops=0, start=0):
        if not self.song_id:
            return
        self.load_song()  # 这里必须重新加载一次，不加载的话从第二次拖动进度条开始就不放歌了
        pygame.mixer.music.play(loops=loops, start=start)
        # 设置进度条位置
        self.play_progressbar_slider.setValue(start)
        # 更新歌曲当前pos值
        self.song_pos = start
        self.first_played = True
        self.is_playing = True
        # 更改播放/暂停按钮图标
        self.play_btn.paint_btn(pause=False)

    # 暂停播放
    def pause(self):
        pygame.mixer.music.pause()
        self.is_playing = False
        # 更改播放/暂停按钮图标
        self.play_btn.paint_btn(pause=True)

    # 继续播放
    def unpause(self):
        pygame.mixer.music.unpause()
        self.is_playing = True
        # 更改播放/暂停按钮图标
        self.play_btn.paint_btn(pause=False)

    # 设置音量
    def set_volume(self, value):
        if self.is_mute:
            pygame.mixer.music.set_volume(0)
            self.mute_btn.paint_btn(0)
            return
        self.volume = value
        pygame.mixer.music.set_volume(self.volume / 100)
        self.mute_btn.paint_btn(self.volume)

    # 下载歌曲
    def download_song(self, song_id):
        # 设置当前播放歌曲的id
        self.setSongId(song_id)
        # 开始播放
        self.play()

    # 判断是否在播放音乐,返回1为正在播放
    def get_is_playing(self):
        # result = pygame.mixer.music.get_busy()
        return self.is_playing

    # 在音乐播放完成时，用事件的方式通知用户程序
    # def set_endevent(self):
    #     def test():
    #         print('end')
    #
    #     pygame.mixer.music.set_endevent(1)

    # 使用指定下一个要播放的音乐文件，当前的音乐播放完成后自动开始播放指定的下一个
    def queque(self):
        # pygame.mixer.music.queue(file)
        pass
