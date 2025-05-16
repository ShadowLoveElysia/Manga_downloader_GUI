from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QGroupBox, QSpinBox, QTextEdit, QComboBox, QCheckBox, QFileDialog,
    QSizePolicy, QMessageBox
)
from PyQt6.QtCore import Qt
import os

class SettingsPanel(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("下载设置")
        self.parent_window = parent # Keep a reference to parent if needed later
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- 添加各个设置项对应的输入控件 ---

        # manga_url (可以简化为只处理一个URL或用TextEdit一行一个)
        self.url_label = QLabel("漫画 URL (每行一个):")
        self.url_edit = QTextEdit() # Using QTextEdit for multiline input
        self.url_edit.setPlaceholderText("在此粘贴漫画网址，每行一个...")
        self.layout().addWidget(self.url_label)
        self.layout().addWidget(self.url_edit)

        # cookies
        self.cookies_label = QLabel("Cookies:")
        self.cookies_edit = QTextEdit() # Using QTextEdit for potentially long cookies
        self.cookies_edit.setPlaceholderText("在此粘贴你的 Cookies 字符串...")
        self.cookies_edit.setFixedHeight(80) # Give some height
        self.layout().addWidget(self.cookies_label)
        self.layout().addWidget(self.cookies_edit)

        # imgdir (可以简化为只指定一个输出目录，或者与URL对应)
        # 考虑到main.py接收列表且与URL对应，简化为指定一个基础输出目录，
        # 或者让用户为每个URL指定目录（更复杂）。先简化为指定一个根目录，或与URL列表框结合。
        # 这里先实现一个简单的：指定一个根目录
        self.imgdir_label = QLabel("图片保存根目录:")
        self.imgdir_layout = QHBoxLayout()
        self.imgdir_edit = QLineEdit()
        self.imgdir_browse_button = QPushButton("浏览...")
        self.imgdir_browse_button.clicked.connect(self._browse_imgdir)
        self.imgdir_layout.addWidget(self.imgdir_edit)
        self.imgdir_layout.addWidget(self.imgdir_browse_button)
        self.layout().addWidget(self.imgdir_label)
        self.layout().addLayout(self.imgdir_layout)


        # res (Width, Height) - 可以用两个SpinBox
        # self.res_label = QLabel("分辨率 (宽, 高):")
        # res_layout = QHBoxLayout()
        # self.res_width_spinbox = QSpinBox()
        # self.res_width_spinbox.setRange(1, 4000)
        # self.res_height_spinbox = QSpinBox()
        # self.res_height_spinbox.setRange(1, 4000)
        # res_layout.addWidget(self.res_width_spinbox)
        # res_layout.addWidget(QLabel("x"))
        # res_layout.addWidget(self.res_height_spinbox)
        # res_layout.addStretch() # Push widgets to the left
        # self.layout().addWidget(self.res_label)
        # self.layout().addLayout(res_layout)
        # # 设置默认值 (假设main.py中的默认值是784, 1200)
        # self.res_width_spinbox.setValue(784)
        # self.res_height_spinbox.setValue(1200)


        # sleep_time (float) - SpinBox 或 LineEdit
        self.sleep_time_label = QLabel("每页下载间隔 (秒):")
        self.sleep_time_spinbox = QSpinBox()
        self.sleep_time_spinbox.setRange(0, 60) # 0 to 60 seconds
        self.sleep_time_spinbox.setValue(1)
        self.layout().addWidget(self.sleep_time_label)
        self.layout().addWidget(self.sleep_time_spinbox)


        # loading_wait_time (int) - SpinBox
        self.loading_wait_time_label = QLabel("页面加载等待时间 (秒):")
        self.loading_wait_time_spinbox = QSpinBox()
        self.loading_wait_time_spinbox.setRange(1, 120) # 1 to 120 seconds
        self.loading_wait_time_spinbox.setValue(20)
        self.layout().addWidget(self.loading_wait_time_label)
        self.layout().addWidget(self.loading_wait_time_spinbox)


        # cut_image (None, 'dynamic', or tuple) - 使用 ComboBox 或 CheckBox+QLineEdit
        # 可以简化： None, dynamic, 或者固定裁剪值 (左上右下)
        self.cut_image_label = QLabel("图片裁剪:")
        self.cut_image_combo = QComboBox()
        self.cut_image_combo.addItem("不裁剪", None) # Data is None
        self.cut_image_combo.addItem("动态裁剪 (移除空白)", "dynamic") # Data is 'dynamic'
        # Add option for fixed cropping - more complex input needed
        # self.cut_image_combo.addItem("固定裁剪 (左,上,右,下)", "fixed") # Data is 'fixed' or something to indicate this mode
        self.layout().addWidget(self.cut_image_label)
        self.layout().addWidget(self.cut_image_combo)

        # # 如果实现固定裁剪，需要额外的输入框，并根据 ComboBox 隐藏/显示
        # self.fixed_cut_layout = QHBoxLayout()
        # # Labels and SpinBoxes for left, upper, right, lower
        # # self.fixed_cut_layout.addWidget(...) 
        # # self.layout().addLayout(self.fixed_cut_layout)
        # # self.fixed_cut_layout.setVisible(False) # Initially hidden
        # # Connect cut_image_combo's currentIndexChanged to update visibility

        # file_name_prefix (string) - LineEdit
        self.prefix_label = QLabel("文件名前缀:")
        self.prefix_edit = QLineEdit()
        self.layout().addWidget(self.prefix_label)
        self.layout().addWidget(self.prefix_edit)

        # number_of_digits (int) - SpinBox
        self.digits_label = QLabel("文件名数字位数:")
        self.digits_spinbox = QSpinBox()
        self.digits_spinbox.setRange(1, 10)
        self.digits_spinbox.setValue(3)
        self.layout().addWidget(self.digits_label)
        self.layout().addWidget(self.digits_spinbox)

        # start_page (int or None) - SpinBox + CheckBox
        self.start_page_label = QLabel("开始页码 (1-indexed):")
        self.start_page_spinbox = QSpinBox()
        self.start_page_spinbox.setRange(1, 99999) # Example range
        self.start_page_spinbox.setEnabled(False) # Disabled by default
        self.start_page_checkbox = QCheckBox("指定开始页")
        self.start_page_checkbox.stateChanged.connect(self.start_page_spinbox.setEnabled)
        start_page_layout = QHBoxLayout()
        start_page_layout.addWidget(self.start_page_checkbox)
        start_page_layout.addWidget(self.start_page_spinbox)
        start_page_layout.addStretch()
        self.layout().addWidget(self.start_page_label)
        self.layout().addLayout(start_page_layout)

        # end_page (int or None) - SpinBox + CheckBox
        self.end_page_label = QLabel("结束页码 (1-indexed):")
        self.end_page_spinbox = QSpinBox()
        self.end_page_spinbox.setRange(1, 99999) # Example range
        self.end_page_spinbox.setEnabled(False) # Disabled by default
        self.end_page_checkbox = QCheckBox("指定结束页")
        self.end_page_checkbox.stateChanged.connect(self.end_page_spinbox.setEnabled)
        end_page_layout = QHBoxLayout()
        end_page_layout.addWidget(self.end_page_checkbox)
        end_page_layout.addWidget(self.end_page_spinbox)
        end_page_layout.addStretch()
        self.layout().addWidget(self.end_page_label)
        self.layout().addLayout(end_page_layout)

        # 添加一个伸缩器把所有控件顶到顶部
        self.layout().addStretch()

    def _browse_imgdir(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "选择图片保存目录",
            self.imgdir_edit.text() or os.path.expanduser("~") # Start from current or home
        )
        if directory:
            self.imgdir_edit.setText(os.path.normpath(directory))

    def get_settings(self):
        """Collects current settings from the UI elements."""
        settings = {
            'manga_url': [url.strip() for url in self.url_edit.toPlainText().split('\n') if url.strip()],
            'cookies': self.cookies_edit.toPlainText().strip(),
            'imgdir': [self.imgdir_edit.text().strip()] * len([url.strip() for url in self.url_edit.toPlainText().split('\n') if url.strip()]), # Currently assigns the same dir to all URLs
            # 'res': (self.res_width_spinbox.value(), self.res_height_spinbox.value()), # If res is implemented
            'sleep_time': self.sleep_time_spinbox.value(), # Note: main.py expects float, SpinBox gives int. May need conversion or float SpinBox.
            'loading_wait_time': self.loading_wait_time_spinbox.value(),
            'cut_image': self.cut_image_combo.currentData(), # Gets the data (None or 'dynamic')
            'file_name_prefix': self.prefix_edit.text().strip(),
            'number_of_digits': self.digits_spinbox.value(),
            'start_page': self.start_page_spinbox.value() if self.start_page_checkbox.isChecked() else None,
            'end_page': self.end_page_spinbox.value() if self.end_page_checkbox.isChecked() else None,
        }

        # Handle float for sleep_time if necessary, or update main.py to accept int
        # For now, main.py's Downloader expects int for sleep_time=2, so SpinBox int is fine.

        # Validation (basic)
        if not settings['manga_url']:
             QMessageBox.warning(self, "输入错误", "请至少提供一个漫画 URL。")
             return None
        if not settings['cookies']:
             QMessageBox.warning(self, "输入错误", "请提供 Cookies。")
             return None
        if not settings['imgdir'][0]: # Check the first (and only) imgdir if using simplified
             QMessageBox.warning(self, "输入错误", "请指定图片保存目录。")
             return None
        # Add more validation as needed

        return settings
