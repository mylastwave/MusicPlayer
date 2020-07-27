from PyQt5.Qt import *
import os


class PlayerBtn(QPushButton):
    """
    播放器控件内所有按钮的父控件
    """
    btn_click = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_paint = True

    def paintEvent(self, evt) -> None:
        super().paintEvent(evt)
        if self.first_paint:
            self.first_paint = False
            # 绘制控件形状
            path = QPainterPath()
            path.addRoundedRect(QRectF(self.rect()), 10, 10)
            polygon = path.toFillPolygon().toPolygon()
            region = QRegion(polygon)
            self.setMask(region)


class PreBtn(PlayerBtn):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(30, 30)
        file_url = os.getcwd() + r'\resource\images\pre_song_30y30.png'
        self.pixmap = QPixmap(file_url)

    def paintEvent(self, evt) -> None:
        super().paintEvent(evt)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawPixmap(self.rect(), self.pixmap)


class NextBtn(PlayerBtn):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(30, 30)
        file_url = os.getcwd() + r'\resource\images\next_song_30y30.png'
        self.pixmap = QPixmap(file_url)

    def paintEvent(self, evt) -> None:
        super().paintEvent(evt)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawPixmap(self.rect(), self.pixmap)


class PlayOrPauseBtn(PlayerBtn):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(40, 40)
        file_url = os.getcwd() + r'\resource\images\pause_play_40y40.png'
        self.pixmap = QPixmap(file_url)
        self.is_pause = True
        # self.clicked.connect(self.clicked_evt)

    def clicked_evt(self):
        if self.is_pause:
            self.is_pause = False
            self.paint_btn(False)
        else:
            self.is_pause = True
            self.paint_btn(True)

    def paint_btn(self, pause):
        if pause:
            # print('暂停')
            self.is_pause = True
            file_url = os.getcwd() + r'\resource\images\pause_play_40y40.png'
            self.pixmap = QPixmap(file_url)
        else:
            # print('播放')
            self.is_pause = False
            file_url = os.getcwd() + r'\resource\images\unpause_play_40y40.png'
            self.pixmap = QPixmap(file_url)
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)
        self.setText('1')  # 设置字符目的是让控件重新绘制一遍，不是真正想显示
        self.setText('')

    def paintEvent(self, evt) -> None:
        super().paintEvent(evt)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawPixmap(self.rect(), self.pixmap)


class VolumeBtn(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(20, 15)
        file_url = os.getcwd() + r'\resource\images\volume3_20y15.png'
        self.pixmap = QPixmap(file_url)
        self.is_mute = False
        self.setStyleSheet('border: 0px solid rgb(0, 0, 0)')

    def paint_btn(self, volume):
        if volume:
            # print('打开')
            file_url = os.getcwd() + r'\resource\images\volume3_20y15.png'
            self.pixmap = QPixmap(file_url)
            self.is_mute = True
        else:
            # print('静音')
            file_url = os.getcwd() + r'\resource\images\mute_20y15.png'
            self.pixmap = QPixmap(file_url)
            self.is_mute = False
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)
        self.setText('1')  # 设置字符目的是让控件重新绘制一遍，不是真正想显示
        self.setText('')

    def paintEvent(self, evt) -> None:
        super().paintEvent(evt)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawPixmap(self.rect(), self.pixmap)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    window = QWidget()
    window.resize(500, 500)
    btn = PlayOrPauseBtn(window)
    btn.move(200, 200)
    window.show()

    sys.exit(app.exec_())
