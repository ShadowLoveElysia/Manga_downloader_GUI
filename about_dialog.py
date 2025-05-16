from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QTextBrowser
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

class AboutDialog(QDialog):
    def __init__(self, parent=None, lang=None):
        super().__init__(parent)
        self.lang = lang  # 当前语言对象
        self.setWindowTitle(self.tr("about_title"))
        self.setMinimumSize(450, 300)
        
        # 创建主布局
        layout = QVBoxLayout(self)
        
        # 应用名称（大字体）
        app_name = QLabel(self.tr("app_title"))
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        app_name.setFont(font)
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(app_name)
        
        # 版本信息
        version_label = QLabel(self.tr("version"))
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
        
        # 描述文本
        description = QTextBrowser()
        description.setOpenExternalLinks(True)
        description.setReadOnly(True)
        
        about_text = self.tr("about_description")
        
        description.setHtml(about_text)
        layout.addWidget(description)
        
        # 关闭按钮
        close_button = QPushButton(self.tr("close_button"))
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
    
    def tr(self, key):
        """翻译函数，从当前语言对象获取翻译"""
        if self.lang:
            return self.lang.get(key)
        return key 