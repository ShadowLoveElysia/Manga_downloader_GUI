from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import Qt

class ConsoleWidget(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setPlaceholderText("控制台输出将显示在此处...")
        # 可以添加一些样式
        # self.setStyleSheet("background-color: #212121; color: #dcdcdc; font-family: Consolas;")

    def append_output(self, text):
        """Appends text to the console."""
        self.append(text)
        # 自动滚动到底部
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
