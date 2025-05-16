import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFileDialog, QDialogButtonBox, QTabWidget,
    QWidget, QGroupBox, QComboBox
)
from PyQt6.QtCore import Qt, QDir
from config import config
from languages import available_languages

class SettingsDialog(QDialog):
    def __init__(self, parent=None, current_project_root="", lang=None):
        super().__init__(parent)
        self.lang = lang  # 当前语言对象
        
        self.setWindowTitle(self.tr("settings_title"))
        self.setMinimumWidth(550)
        self.setMinimumHeight(400)
        
        # 保存初始项目根目录和浏览器设置
        self.current_project_root = current_project_root
        self.current_chrome_path = config.get("chrome_path", "")
        self.current_chromedriver_path = config.get("chromedriver_path", "")
        self.current_language = config.get("language", "zh_CN")
        
        # 创建主布局
        layout = QVBoxLayout(self)
        
        # 创建选项卡小部件
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # 创建"常规"选项卡
        self.general_tab = QWidget()
        self.general_layout = QVBoxLayout(self.general_tab)
        self.tab_widget.addTab(self.general_tab, self.tr("General"))
        
        # 语言设置组
        language_group = QGroupBox(self.tr("Language"))
        language_layout = QHBoxLayout()
        language_label = QLabel(self.tr("Select language:"))
        self.language_combo = QComboBox()
        
        # 添加可用语言
        for lang_code, lang_info in available_languages.items():
            self.language_combo.addItem(lang_info["name"], lang_code)
            # 设置当前选中的语言
            if lang_code == self.current_language:
                self.language_combo.setCurrentText(lang_info["name"])
        
        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_combo)
        language_group.setLayout(language_layout)
        self.general_layout.addWidget(language_group)
        
        # 项目根目录设置组
        project_root_group = QGroupBox(self.tr("Project Path"))
        project_root_layout = QVBoxLayout()
        
        # 项目根目录行
        project_root_row = QHBoxLayout()
        project_root_label = QLabel(self.tr("project_root"))
        self.project_root_edit = QLineEdit(self.current_project_root)
        self.project_root_button = QPushButton(self.tr("browse_button"))
        self.project_root_button.clicked.connect(self._browse_project_root)
        
        project_root_row.addWidget(project_root_label)
        project_root_row.addWidget(self.project_root_edit)
        project_root_row.addWidget(self.project_root_button)
        project_root_layout.addLayout(project_root_row)
        
        # 项目根目录说明
        help_text = self.tr("project_root_help")
        help_label = QLabel(help_text)
        help_label.setWordWrap(True)
        project_root_layout.addWidget(help_label)
        
        project_root_group.setLayout(project_root_layout)
        self.general_layout.addWidget(project_root_group)
        
        # 添加伸缩空间
        self.general_layout.addStretch()
        
        # 创建"浏览器"选项卡
        self.browser_tab = QWidget()
        self.browser_layout = QVBoxLayout(self.browser_tab)
        self.tab_widget.addTab(self.browser_tab, self.tr("Browser"))
        
        # Chrome 浏览器路径设置
        chrome_group = QGroupBox(self.tr("Chrome Settings"))
        chrome_layout = QVBoxLayout()
        
        # Chrome 路径行
        chrome_path_row = QHBoxLayout()
        chrome_path_label = QLabel(self.tr("chrome_path"))
        self.chrome_path_edit = QLineEdit(self.current_chrome_path)
        self.chrome_path_button = QPushButton(self.tr("browse_button"))
        self.chrome_path_button.clicked.connect(self._browse_chrome_path)
        
        chrome_path_row.addWidget(chrome_path_label)
        chrome_path_row.addWidget(self.chrome_path_edit)
        chrome_path_row.addWidget(self.chrome_path_button)
        chrome_layout.addLayout(chrome_path_row)
        
        # ChromeDriver 路径行
        chromedriver_path_row = QHBoxLayout()
        chromedriver_path_label = QLabel(self.tr("chromedriver_path"))
        self.chromedriver_path_edit = QLineEdit(self.current_chromedriver_path)
        self.chromedriver_path_button = QPushButton(self.tr("browse_button"))
        self.chromedriver_path_button.clicked.connect(self._browse_chromedriver_path)
        
        chromedriver_path_row.addWidget(chromedriver_path_label)
        chromedriver_path_row.addWidget(self.chromedriver_path_edit)
        chromedriver_path_row.addWidget(self.chromedriver_path_button)
        chrome_layout.addLayout(chromedriver_path_row)
        
        # Chrome 版本说明
        chrome_help_text = self.tr("chrome_version_help")
        chrome_help_label = QLabel(chrome_help_text)
        chrome_help_label.setWordWrap(True)
        chrome_layout.addWidget(chrome_help_label)
        
        chrome_group.setLayout(chrome_layout)
        self.browser_layout.addWidget(chrome_group)
        
        # 添加伸缩空间
        self.browser_layout.addStretch()
        
        # 按钮区域
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def tr(self, key):
        """翻译函数，从当前语言对象获取翻译"""
        if self.lang:
            return self.lang.get(key)
        return key
    
    def _browse_project_root(self):
        """打开文件夹选择对话框以设置项目根目录"""
        directory = QFileDialog.getExistingDirectory(
            self,
            self.tr("Select Project Root"),
            self.project_root_edit.text() or QDir.homePath()
        )
        if directory:
            self.project_root_edit.setText(directory)
    
    def _browse_chrome_path(self):
        """打开文件选择对话框以设置Chrome浏览器路径"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("Select Chrome Executable"),
            self.chrome_path_edit.text() or QDir.homePath(),
            self.tr("Executable (*.exe);;All files (*)")
        )
        if file_path:
            self.chrome_path_edit.setText(file_path)
    
    def _browse_chromedriver_path(self):
        """打开文件选择对话框以设置ChromeDriver路径"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("Select ChromeDriver Executable"),
            self.chromedriver_path_edit.text() or QDir.homePath(),
            self.tr("Executable (*.exe);;All files (*)")
        )
        if file_path:
            self.chromedriver_path_edit.setText(file_path)
    
    def get_settings(self):
        """返回用户设置"""
        return {
            "project_root": self.project_root_edit.text().strip(),
            "chrome_path": self.chrome_path_edit.text().strip(),
            "chromedriver_path": self.chromedriver_path_edit.text().strip(),
            "language": self.language_combo.currentData()
        } 