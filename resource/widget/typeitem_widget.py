from PyQt5.Qt import *

"""
展示区域展示类型控件栏
"""


# 展示类型栏控件的类
class TypeItemUi(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedHeight(44)
        self.setupUi()

    def setupUi(self):
        # 创建横向布局
        h_layout = QHBoxLayout()

        type1 = TypeBtn('歌单')
        type1.setChecked(True)
        type2 = TypeBtn('敬请期待')

        # 按钮组
        type_group = QButtonGroup()
        type_group.addButton(type1)
        type_group.addButton(type2)
        type_group.setExclusive(True)

        h_layout.addStretch(1)
        h_layout.addWidget(type1)
        h_layout.addWidget(type2)
        h_layout.addStretch(1)

        h_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(h_layout)

    def paintEvent(self, evt) -> None:
        super().paintEvent(evt)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(225, 225, 226), 4))
        painter.drawLine(0, self.height(), self.width(), self.height())


class TypeBtn(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置字体
        font = QFont()
        font.setFamily('微软雅黑')
        font.setPointSize(12)
        self.setFont(font)
        # 更改鼠标样式
        self.setCursor(Qt.PointingHandCursor)
        # 互斥，能一次保持按下状态
        self.setCheckable(True)
        self.setAutoExclusive(True)
        # 设置按钮样式
        self.setFixedSize(70, 40)
        self.setFlat(True)
        # self.setStyleSheet('background-color: rgb(94, 184, 251)')
        # self.setStyleSheet('border: 1px solid rgb(255, 255, 255)')
        # 绑定槽函数
        self.toggled.connect(self.paint_evt)

    # 控制按钮文字颜色
    def paint_evt(self):
        if self.isChecked():
            self.setStyleSheet('color: rgb(94, 184, 251);')
        else:
            self.setStyleSheet('color: rgb(0, 0, 0)')

    # 重写鼠标进入离开事件
    def enterEvent(self, evt) -> None:
        super().enterEvent(evt)
        self.setStyleSheet('color: rgb(94, 184, 251);')

    def leaveEvent(self, evt) -> None:
        super().leaveEvent(evt)
        if self.isChecked():
            self.setStyleSheet('color: rgb(94, 184, 251);')
        else:
            self.setStyleSheet('color: rgb(0, 0, 0)')
