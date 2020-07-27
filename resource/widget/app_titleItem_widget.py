from PyQt5.Qt import *


class MyTitleWidget(QWidget):
    """
    标题栏控件
    """
    window_moved = pyqtSignal([QPoint])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # flag 属性的作用，当鼠标在标题控件外按下移入到标题控件时不会触发标题控件的鼠标事件
        # 只有在标题控件按下并且拖动时才能正常触发标题控件自定义的鼠标事件
        self.flag = False
        # self.setStyleSheet('background-color: rgb(94, 184, 251);')

    def mousePressEvent(self, evt) -> None:
        super().mousePressEvent(evt)

        self.flag = True
        self.mouse_g_pos = evt.globalPos()

    def mouseMoveEvent(self, evt) -> None:
        super().mouseMoveEvent(evt)

        # 判断flag属性是否被创建
        res = hasattr(self, 'flag')

        # 当没有事先触发点击事件或者flag为false时，退出函数
        if not res or not self.flag:
            return

        # 发送自定义信号，携带移动的距离
        mouse_moved = evt.globalPos() - self.mouse_g_pos
        self.mouse_g_pos = evt.globalPos()
        self.window_moved[QPoint].emit(mouse_moved)

    def mouseReleaseEvent(self, evt) -> None:
        super().mouseReleaseEvent(evt)

        # 判断flag属性是否被创建
        res = hasattr(self, 'flag')

        # 当没有事先触发点击事件时退出函数
        if not res:
            return

        # 鼠标松开时重置flag值
        self.flag = False

    def paintEvent(self, event):
        # 以下几行代码的功能是避免在多重传值后的功能失效
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)


class MyButton(QPushButton):
    """
    标题栏最大化最小化和关闭的按钮
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setStyleSheet('color: rgb(158, 209, 251);')
        self.setFlat(True)

    def enterEvent(self, evt) -> None:
        super().enterEvent(evt)

        self.setStyleSheet('color: rgb(251, 251, 251);')

    def leaveEvent(self, evt) -> None:
        super().leaveEvent(evt)

        self.setStyleSheet('color: rgb(158, 209, 251);')
