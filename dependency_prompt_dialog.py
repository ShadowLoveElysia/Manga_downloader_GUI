from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QDialogButtonBox, QSizePolicy
from PyQt6.QtCore import Qt

class DependencyPromptDialog(QDialog):
    INSTALL_ALL = 1
    REPAIR_MISSING = 2
    # Add other result codes if needed

    def __init__(self, dependency_status, parent=None):
        super().__init__(parent)
        self.setWindowTitle("依赖项检查结果")
        self.setMinimumWidth(500)

        self.result_code = None # To store what action the user chose

        main_layout = QVBoxLayout(self)

        self.status_label = QLabel() # e.g., "所有依赖项均已安装且版本正确。"
        main_layout.addWidget(self.status_label)

        self.details_text_edit = QTextEdit()
        self.details_text_edit.setReadOnly(True)
        self.details_text_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        main_layout.addWidget(self.details_text_edit)

        self.button_box = QDialogButtonBox()
        main_layout.addWidget(self.button_box)

        self._populate_dialog(dependency_status)

    def _populate_dialog(self, dependency_status):
        """
        Populates the dialog based on the results from DependencyManager.
        """
        details_str = "详细信息:\n"
        if not dependency_status or not dependency_status.get('details'):
            self.status_label.setText("无法获取依赖状态。")
            self.status_label.setStyleSheet("color: gray;")
            self.details_text_edit.setText("未能加载依赖详情。")
            self.button_box.addButton("确定", QDialogButtonBox.ButtonRole.AcceptRole).clicked.connect(self.accept)
            return

        # Display details in a readable format
        details_str += "包名称                 要求版本         已安装版本       状态\n"
        details_str += "---------------------------------------------------------------------\n"
        for pkg, info in dependency_status['details'].items():
             # Use consistent spacing
            installed_display = info.get('installed', 'N/A')
            if installed_display == 'Not Found': installed_display = '未找到'
            
            status_display = info.get('status', '未知')
            if status_display == 'OK': status_display = '正常'
            elif status_display == 'Missing': status_display = '缺失'
            elif status_display == 'Mismatch': status_display = '版本不符'
            elif status_display == 'Parse Error': status_display = '解析错误'
            elif status_display == 'Check Error': status_display = '检查错误'

            details_str += f"{pkg:<20} {info.get('required', '任意'):<15} {installed_display:<15} {status_display}\n"

        self.details_text_edit.setText(details_str)

        if dependency_status.get('all_ok'):
            self.status_label.setText("所有核心依赖项均已正确安装！")
            self.status_label.setStyleSheet("color: green;")
            ok_button = self.button_box.addButton("太棒了！", QDialogButtonBox.ButtonRole.AcceptRole)
            ok_button.clicked.connect(self.accept)
        elif dependency_status.get('error'):
             self.status_label.setText("错误: 依赖检查失败！")
             self.status_label.setStyleSheet("color: red;")
             self.details_text_edit.setText(f"依赖检查过程中发生错误:\n{dependency_status['error']}\n\n请手动检查并修复问题。")
             ok_button = self.button_box.addButton("确定", QDialogButtonBox.ButtonRole.AcceptRole)
             ok_button.clicked.connect(self.accept)
        elif dependency_status.get('all_missing'):
            self.status_label.setText("警告: 项目核心依赖项均未安装。")
            self.status_label.setStyleSheet("color: red;")
            install_all_button = self.button_box.addButton("一键安装所有依赖", QDialogButtonBox.ButtonRole.ActionRole)
            install_all_button.clicked.connect(self._on_install_all)
            self.details_text_edit.append("\n建议：点击下方按钮尝试自动安装所有必需的依赖项。")
        elif dependency_status.get('some_missing') or dependency_status.get('version_mismatch'): # Combined condition
            self.status_label.setText("警告: 部分项目核心依赖项缺失或版本不正确。")
            self.status_label.setStyleSheet("color: orange;")
            repair_button = self.button_box.addButton("尝试修复/安装/更新依赖", QDialogButtonBox.ButtonRole.ActionRole)
            repair_button.clicked.connect(self._on_repair_missing)
            self.details_text_edit.append("\n建议：点击下方按钮尝试自动安装或更新不匹配的依赖项。")
        else: # Should ideally not happen if status flags are set correctly
            self.status_label.setText("依赖状态未知或部分不满足。")
            self.status_label.setStyleSheet("color: orange;")


        cancel_button = self.button_box.addButton("稍后处理", QDialogButtonBox.ButtonRole.RejectRole)
        cancel_button.clicked.connect(self.reject)

        # Adjust text edit height based on content (simple fixed height)
        self.details_text_edit.setFixedHeight(150) # Give it a reasonable default height


    def _on_install_all(self):
        self.result_code = self.INSTALL_ALL
        self.accept()

    def _on_repair_missing(self):
        self.result_code = self.REPAIR_MISSING
        self.accept()

    def get_result_code(self):
        return self.result_code

# Example Usage (for testing)
if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    # Example dummy dependency status dictionaries
    dummy_status_all_ok = {
        'all_ok': True, 'all_missing': False, 'some_missing': False, 'version_mismatch': False,
        'details': {'PyQt6': {'installed': '6.5.0', 'required': '==6.5.0', 'status': 'OK'},
                    'selenium': {'installed': '4.8.2', 'required': 'any', 'status': 'OK'}},
        'missing_packages_info': [], 'mismatch_packages_info': []
    }
    dummy_status_all_missing = {
        'all_ok': False, 'all_missing': True, 'some_missing': False, 'version_mismatch': False,
        'details': {
            'PyQt6': {'installed': 'Not Found', 'required': '==6.5.0', 'status': 'Missing'},
            'selenium': {'installed': 'Not Found', 'required': 'any', 'status': 'Missing'}
        },
        'missing_packages_info': [{'name': 'PyQt6', 'original_line': 'PyQt6==6.5.0'}, {'name': 'selenium', 'original_line': 'selenium'}],
        'mismatch_packages_info': []
    }
    dummy_status_some_missing_mismatch = {
        'all_ok': False, 'all_missing': False, 'some_missing': True, 'version_mismatch': True,
        'details': {
            'PyQt6': {'installed': '6.4.0', 'required': '==6.5.0', 'status': 'Mismatch'},
            'numpy': {'installed': 'Not Found', 'required': '>=1.20', 'status': 'Missing'},
            'Pillow': {'installed': '10.0.0', 'required': '>=9.0.0', 'status': 'OK'}
        },
        'missing_packages_info': [{'name': 'numpy', 'original_line': 'numpy>=1.20'}],
        'mismatch_packages_info': [{'name': 'PyQt6', 'installed': '6.4.0', 'required': '==6.5.0', 'original_line': 'PyQt6==6.5.0'}]
    }
    dummy_status_error = {
        'all_ok': False, 'all_missing': False, 'some_missing': False, 'version_mismatch': False,
        'error': '无法读取 requirements.txt 文件。', "details": {},
        "missing_packages_info": [], "mismatch_packages_info": []
    }


    app = QApplication(sys.argv)

    print("Testing with: All OK")
    dialog_ok = DependencyPromptDialog(dummy_status_all_ok)
    dialog_ok.exec()
    print(f"Result: {dialog_ok.get_result_code()}")

    print("\nTesting with: All Missing")
    dialog_all_missing = DependencyPromptDialog(dummy_status_all_missing)
    dialog_all_missing.exec()
    print(f"Result: {dialog_all_missing.get_result_code()}")

    print("\nTesting with: Some Missing / Mismatch")
    dialog_some_missing = DependencyPromptDialog(dummy_status_some_missing_mismatch)
    dialog_some_missing.exec()
    print(f"Result: {dialog_some_missing.get_result_code()}")

    print("\nTesting with: Error State")
    dialog_error = DependencyPromptDialog(dummy_status_error)
    dialog_error.exec()
    print(f"Result: {dialog_error.get_result_code()}")


    sys.exit()
