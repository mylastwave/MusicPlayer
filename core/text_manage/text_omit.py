from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics, QFont


# 文本超出宽度的字符显示省略
def text_omit(text: str, width: int) -> str:
    font = QFontMetrics(QFont(text))
    font_size = font.width(text)
    resize_width = width
    if font_size > resize_width:
        text = font.elidedText(text, Qt.ElideRight, width)
    return text
