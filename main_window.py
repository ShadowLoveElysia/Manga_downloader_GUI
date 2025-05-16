import sys
import os
import json # Needed for passing settings as JSON string
import subprocess # Needed to run pip command

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTabWidget, 
    QMessageBox, QMenuBar, QFileDialog, QLabel, QLineEdit, QMenu
)
from PyQt6.QtGui import QAction, QActionGroup
from PyQt6.QtCore import QProcess, QStandardPaths, Qt, QDir # Added QDir

# Import settings panel and console widget
from settings_panel import SettingsPanel
from console_widget import ConsoleWidget

# Import dialogs (will be dynamically imported when needed)
# from settings_dialog import SettingsDialog
# from about_dialog import AboutDialog

from dependency_manager import DependencyManager
from dependency_prompt_dialog import DependencyPromptDialog

# Import your new Image to PDF widget
# from img_to_pdf_widget import ImgToPdfWidget

# Import configuration and languages
from config import config
from languages import available_languages

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Load language settings
        self.current_language = config.get("language", "zh_CN")
        self.lang = available_languages[self.current_language]["data"]
        
        self.setWindowTitle(self.tr("app_title"))
        self.setGeometry(100, 100, 800, 600) # Adjust window size

        # Dependency Manager instance
        self.dependency_manager = DependencyManager()

        # Determine the path to the original Manga_downloader-master project
        # Assumes the GUI folder is a sibling of the original project folder
        gui_dir = os.path.dirname(os.path.abspath(__file__))
        # Initial guess for project root (current directory)
        self._project_root_dir = config.get("project_root", gui_dir)
        self.project_root_valid = os.path.isdir(self._project_root_dir)

        self._validate_project_root()

        # Create central widget and main layout FIRST
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self._create_menus() # Create menu bar

        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)

        # --- Settings Tab ---
        self.settings_tab = QWidget()
        self.settings_tab_layout = QVBoxLayout(self.settings_tab)
        self.settings_panel = SettingsPanel() # Create instance of settings panel
        self.settings_tab_layout.addWidget(self.settings_panel)
        self.settings_tab_layout.addStretch() # Push panel to top
        self.tab_widget.addTab(self.settings_tab, self.tr("settings_tab"))

        # --- Console Tab ---
        self.console_tab = QWidget()
        self.console_tab_layout = QVBoxLayout(self.console_tab)
        self.console_widget = ConsoleWidget() # Create instance of console widget
        self.console_tab_layout.addWidget(self.console_widget)
        self.tab_widget.addTab(self.console_tab, self.tr("console_tab"))

        # --- Image to PDF Tab ---
        self.img_to_pdf_tab = QWidget()
        self.img_to_pdf_tab_layout = QVBoxLayout(self.img_to_pdf_tab)
        
        # Create widgets for input directory selection
        input_layout = QHBoxLayout()
        self.input_dir_label = QLabel(self.tr("input_dir"))
        self.input_dir_edit = QLineEdit()
        self.input_dir_button = QPushButton(self.tr("browse_button"))
        self.input_dir_button.clicked.connect(self._browse_input_dir)
        input_layout.addWidget(self.input_dir_label)
        input_layout.addWidget(self.input_dir_edit)
        input_layout.addWidget(self.input_dir_button)
        self.img_to_pdf_tab_layout.addLayout(input_layout)
        
        # Create widgets for output PDF file selection
        output_layout = QHBoxLayout()
        self.output_pdf_label = QLabel(self.tr("output_pdf"))
        self.output_pdf_edit = QLineEdit()
        self.output_pdf_button = QPushButton(self.tr("browse_button"))
        self.output_pdf_button.clicked.connect(self._browse_output_pdf)
        output_layout.addWidget(self.output_pdf_label)
        output_layout.addWidget(self.output_pdf_edit)
        output_layout.addWidget(self.output_pdf_button)
        self.img_to_pdf_tab_layout.addLayout(output_layout)
        
        # Create convert button
        self.convert_button = QPushButton(self.tr("convert_button"))
        self.convert_button.clicked.connect(self._convert_to_pdf)
        self.img_to_pdf_tab_layout.addWidget(self.convert_button)
        
        self.img_to_pdf_tab_layout.addStretch() # Push widgets to top
        self.tab_widget.addTab(self.img_to_pdf_tab, self.tr("img_to_pdf_tab"))

        # --- Buttons ---
        self.button_layout = QHBoxLayout()
        self.start_button = QPushButton(self.tr("start_button"))
        self.stop_button = QPushButton(self.tr("stop_button"))
        self.stop_button.setEnabled(False) # Stop button initially disabled

        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)
        self.main_layout.addLayout(self.button_layout)

        # Connect signals for download buttons
        self.start_button.clicked.connect(self.start_download)
        self.stop_button.clicked.connect(self.stop_download)

        # QProcess for running external scripts (download, pip install)
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.handle_process_finished)
        self.process.errorOccurred.connect(self.handle_process_error)

        # **Connect the signal from ImgToPdfWidget to run commands**
        # self.img_to_pdf_widget.runCommandRequested.connect(self.run_command_in_process)

        # Disable start button if project path is invalid initially
        if not self.project_root_valid:
            self.start_button.setEnabled(False) # Disable download button
            # console_widget is now guaranteed to exist here
            self.console_widget.append_output("ERROR: 原始项目路径无效，部分功能可能受限。请检查文件夹结构或在设置中配置正确路径。")
            # Also potentially disable the convert button in img_to_pdf_widget if it relies on project files
            # For img_to_pdf, only the script location matters relative to project root
            # If the script '文件合并2PDF.py' is expected IN the project root, then validity matters.
            # Let's assume it is expected in the project root.
            # self.img_to_pdf_widget.convert_button.setEnabled(False) # This button is now directly in MainWindow
            self.convert_button.setEnabled(False)

        # --- Call initial dependency check here, at the very end of __init__ ---
        # This is done after all GUI components, including console_widget, are initialized.
        if self.project_root_valid:
             self._check_and_prompt_dependencies(initial_check=True)

    # Property to get the current project root directory
    @property
    def project_root_dir(self):
        return self._project_root_dir

    # Property to set the project root directory and re-validate
    @project_root_dir.setter
    def project_root_dir(self, path):
        self._project_root_dir = os.path.normpath(path)
        self._validate_project_root()
        if self.project_root_valid:
             self.console_widget.append_output(f"INFO: 项目根目录已更新为: {self.project_root_dir}")
             self.start_button.setEnabled(True) # Re-enable if valid
        else:
             self.console_widget.append_output(f"ERROR: 无效的项目根目录: {self.project_root_dir}. 功能已禁用。")
             self.start_button.setEnabled(False) # Keep disabled if invalid

    def _validate_project_root(self):
         # Check if the set project_root_dir is a valid directory
         self.project_root_valid = os.path.isdir(self._project_root_dir)
         # Optional: Also check for existence of key files like main.py
         # if self.project_root_valid:
         #      main_py_path = os.path.join(self._project_root_dir, "main.py")
         #      self.project_root_valid = os.path.isfile(main_py_path)
         #      if not self.project_root_valid:
         #           print(f"WARNING: Project root '{self._project_root_dir}' exists, but main.py not found.", file=sys.stderr)


    def _create_menus(self):
        menu_bar = self.menuBar()

        # 文件菜单
        file_menu = menu_bar.addMenu(self.tr("menu_file"))

        settings_action = QAction(self.tr("menu_settings"), self)
        settings_action.setStatusTip(self.tr("menu_settings"))
        settings_action.triggered.connect(self.open_settings_dialog)
        file_menu.addAction(settings_action)

        check_deps_action = QAction(self.tr("menu_check_deps"), self)
        check_deps_action.setStatusTip(self.tr("menu_check_deps"))
        check_deps_action.triggered.connect(self.check_dependencies)
        file_menu.addAction(check_deps_action)

        file_menu.addSeparator()

        exit_action = QAction(self.tr("menu_exit"), self)
        exit_action.setStatusTip(self.tr("menu_exit"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 语言菜单
        language_menu = menu_bar.addMenu(self.tr("menu_language"))
        language_action_group = QActionGroup(self)
        
        # Add language options
        for lang_code, lang_info in available_languages.items():
            action = QAction(lang_info["name"], self, checkable=True)
            action.setData(lang_code)
            action.setChecked(lang_code == self.current_language)
            action.triggered.connect(self.change_language)
            language_action_group.addAction(action)
            language_menu.addAction(action)

        # 帮助菜单
        help_menu = menu_bar.addMenu(self.tr("menu_help"))
        about_action = QAction(self.tr("menu_about"), self)
        about_action.setStatusTip(self.tr("menu_about"))
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)


    def open_settings_dialog(self):
        """打开设置对话框配置项目根目录和Chrome设置"""
        from settings_dialog import SettingsDialog
        dialog = SettingsDialog(self, current_project_root=self.project_root_dir, lang=self.lang)
        if dialog.exec():
            settings = dialog.get_settings()
            
            # Check and update project root directory
            new_root = settings["project_root"]
            if new_root and os.path.isdir(new_root) and new_root != self.project_root_dir:
                self._project_root_dir = new_root
                self.project_root_valid = True
                config.set("project_root", new_root)
                QMessageBox.information(self, self.tr("Path Updated"), f"{self.tr('path_updated')}:\n{self.project_root_dir}")
            elif new_root and not os.path.isdir(new_root):
                QMessageBox.warning(self, self.tr("Invalid Path"), self.tr("invalid_path"))
            
            # Update Chrome and ChromeDriver paths
            config.set("chrome_path", settings["chrome_path"])
            config.set("chromedriver_path", settings["chromedriver_path"])
            
            # Update language settings (if changed)
            if settings["language"] != self.current_language:
                self.current_language = settings["language"]
                config.set("language", settings["language"])
                self.lang = available_languages[settings["language"]]["data"]
                
                # Prompt user to restart application to apply new language
                QMessageBox.information(
                    self, 
                    "Language Changed / 语言已更改 / 言語が変更されました", 
                    "Please restart the application to apply the new language.\n"
                    "请重新启动应用程序以应用新语言。\n"
                    "新しい言語を適用するにはアプリケーションを再起動してください。"
                )

    def show_about_dialog(self):
        """显示关于对话框"""
        from about_dialog import AboutDialog
        dialog = AboutDialog(self, lang=self.lang)
        dialog.exec()

    def _check_and_prompt_dependencies(self, initial_check=False):
        """Checks dependencies and prompts user if needed."""
        if not self.project_root_valid:
             if not initial_check: # Avoid double-prompt on startup if root is already invalid
                 QMessageBox.warning(self, "无法检查依赖", "项目根目录无效，无法检查依赖项。请先在设置中配置正确的项目根目录。")
             self.console_widget.append_output("ERROR: 项目根目录无效，跳过依赖检查。")
             self.statusBar().showMessage("依赖检查失败 (项目路径无效)", 5000)
             return False

        self.console_widget.append_output("INFO: 开始检查项目依赖项...")
        self.statusBar().showMessage("正在检查依赖项...", 0) # Stay until status changes

        req_file_path = self.dependency_manager.get_requirements_path(self.project_root_dir)
        if not req_file_path or not os.path.exists(req_file_path):
            msg = f"警告: requirements.txt 文件在 '{req_file_path}' 未找到。" if req_file_path else "警告: 无法确定 requirements.txt 的路径。"
            self.console_widget.append_output(msg)
            self.statusBar().showMessage("requirements.txt 未找到", 5000)
            if not initial_check: # Only show prominent message if user manually triggered check
                 QMessageBox.information(self, "依赖信息", msg + "\n\n依赖管理功能（如自动安装）将不可用，除非此文件存在。")
            return False

        status = self.dependency_manager.check_dependencies(req_file_path)

        if status.get("error"):
            self.console_widget.append_output(f"ERROR: 检查依赖时发生错误: {status['error']}")
            self.statusBar().showMessage("依赖检查出错", 5000)
            QMessageBox.critical(self, "依赖检查失败", f"检查依赖项时发生错误:\n{status['error']}")
            return False

        # self.console_widget.append_output("INFO: 依赖项检查完成。") # Will be in dialog details
        self.statusBar().showMessage("依赖项检查完成。", 3000) # Temporary, dialog will appear

        if status.get("all_ok"):
            self.console_widget.append_output("INFO: 所有核心依赖项均满足要求。")
            if not initial_check: # Avoid showing this on every startup if OK
                QMessageBox.information(self, "依赖项状态", "所有核心依赖项均已正确安装！")
            return True

        # If not all OK, show the prompt dialog
        prompt_dialog = DependencyPromptDialog(status, self)
        if prompt_dialog.exec(): # Show dialog modally
            result_code = prompt_dialog.get_result_code()
            if result_code in [DependencyPromptDialog.INSTALL_ALL, DependencyPromptDialog.REPAIR_MISSING]:
                 # Collect packages to install based on dialog result
                 packages_to_install = []
                 if result_code == DependencyPromptDialog.INSTALL_ALL:
                      # For INSTALL_ALL, we just pass the requirements file path to pip
                      packages_to_install = ['-r', req_file_path] # Pip expects -r followed by path
                      action_name = "安装所有依赖项"
                 else: # REPAIR_MISSING
                     # Collect specific packages from status details
                     # Use original_line to get version specifiers like package==version or package>=version
                     if status.get("missing_packages_info"):
                         for pkg_info in status["missing_packages_info"]:
                             packages_to_install.append(pkg_info["original_line"])

                     if status.get("mismatch_packages_info"):
                          for pkg_info in status["mismatch_packages_info"]:
                             packages_to_install.append(pkg_info["original_line"])
                     action_name = "修复/安装特定依赖项"


                 if packages_to_install:
                    # Remove duplicates if any, although original_line should be unique
                    # packages_to_install = list(set(packages_to_install)) # Set might mess up -r order if included
                    
                    self._run_pip_command(['install'] + packages_to_install, action_name)
                 else:
                     self.console_widget.append_output("INFO: 未找到需要安装或更新的包。")
                     self.statusBar().showMessage("无依赖需要修复。", 3000)

            else: # User clicked "稍后处理" or closed dialog
                 self.console_widget.append_output("INFO: 用户选择稍后处理依赖项问题或取消。")
                 self.statusBar().showMessage("依赖项操作已取消。", 3000)

        else: # Dialog was rejected (e.g. closed without selecting an action button)
            self.console_widget.append_output("INFO: 用户已取消依赖项提示。")
            self.statusBar().showMessage("依赖项操作已取消。", 3000)

        # Return False because not all dependencies were OK
        return False

    def _run_pip_command(self, command_args, operation_description="pip 操作"):
        """
        Runs a pip command using the main QProcess.
        command_args: A list of arguments for pip (e.g., ['install', 'requests']).
        """
        if not self.project_root_valid:
             self.console_widget.append_output("ERROR: 项目根目录无效，无法运行 pip 命令。")
             self.statusBar().showMessage("pip 失败 (项目路径无效)", 5000)
             return

        # Assuming python is in PATH or sys.executable is correct
        python_exe = sys.executable if sys.executable else "python"

        # Pip install command list
        full_command = [python_exe, "-m", "pip"] + command_args

        # Use the general method to run the command
        # Pip should run with the original project directory as working directory
        self.run_command_in_process(full_command, operation_description, self.project_root_dir)

    def run_command_in_process(self, command, operation_description, working_directory):
        """
        Runs a command list using the main QProcess, setting the working directory.
        Ensures only one foreground process runs at a time.
        """
        # Check if a process is already running (including pip install if it uses self.process)
        if self.process and self.process.state() != QProcess.ProcessState.NotRunning:
            # Check if it's the download process we can stop
            # Check if it's a different type of process (like pip or pdf conversion)
            # For simplicity, prevent starting *any* new foreground process if one exists.
            self.console_widget.append_output(f"警告: 另一个操作正在进行中。请等待其完成后再试。")
            self.statusBar().showMessage("有操作正在进行中...", 3000)
            return

        if not working_directory or not os.path.isdir(working_directory):
             self.console_widget.append_output(f"ERROR: 无效的工作目录: {working_directory}. 无法执行命令。")
             self.statusBar().showMessage("命令启动失败 (无效目录)", 5000)
             return

        self.console_widget.clear() # Clear console for new run
        self.console_widget.append_output(f"INFO: 即将执行操作 - {operation_description}")
        self.console_widget.append_output(f"CMD: {' '.join(command)}")
        self.console_widget.append_output(f"Working Dir: {working_directory}")
        self.statusBar().showMessage(f"正在准备执行: {operation_description}...", 3000)

        # Disable relevant buttons - generalize this
        # For now, manually disable start/stop buttons for any foreground task initiated this way
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True) # Allow stopping whatever runs in the main process
        self.convert_button.setEnabled(False) # Disable convert button

        self.tab_widget.setCurrentWidget(self.console_tab) # Switch to console tab


        try:
            self.process.setWorkingDirectory(working_directory)
            self.process.start(command[0], command[1:])
            self.statusBar().showMessage(f"正在执行: {operation_description}...", 0)
        except Exception as e:
            self.console_widget.append_output(f"ERROR: 启动 QProcess 失败: {e}")
            self.handle_process_finished(-1, QProcess.ExitStatus.NormalExit) # Simulate finish with error
            self.statusBar().showMessage("命令启动失败!", 5000)

    def tr(self, key):
        """翻译函数，从当前语言对象获取翻译"""
        return self.lang.get(key)

    def start_download(self):
        settings = self.settings_panel.get_settings()  # 从面板获取设置
        if settings is None:  # 在settings_panel中验证失败（由于QMessageBox）
            return

        # 添加Chrome和ChromeDriver路径到设置中，如果已在配置中设置
        chrome_path = config.get("chrome_path", "")
        chromedriver_path = config.get("chromedriver_path", "")
        
        if chrome_path:
            settings["chrome_binary"] = chrome_path
        if chromedriver_path:
            settings["chromedriver_path"] = chromedriver_path

        self.console_widget.clear()  # 清空控制台以便新的运行
        self.console_widget.append_output(f"INFO: {self.tr('info_start_download')}")

        # 运行临时脚本
        temp_runner_script_name = "temp_gui_runner.py"
        temp_runner_script_path = os.path.join(self.project_root_dir, temp_runner_script_name)

        # 生成设置字典的可靠Python字面量格式
        settings_repr = repr(settings)

        runner_script_content = f"""
# This is a temporary script generated by the GUI
# It sets the settings dictionary and then runs the main downloader logic

import sys
import os
import traceback # Import traceback

# Ensure the original project directory is in sys.path to import Downloader
original_project_dir = r'{self.project_root_dir}'
if original_project_dir not in sys.path:
    sys.path.insert(0, original_project_dir)

try:
    # Import the Downloader class from the original project
    from downloader import Downloader

    # Define settings dictionary based on GUI input using the repr string
    settings = {settings_repr}

    print("INFO: GUI传入的设置:")
    # Safely print settings to console, handle potential large values like cookies
    for k, v in settings.items():
        print(f"  {{k}}: {{repr(v)[:150]}}...") # Print truncated repr for large values
    print("-" * 20)

    # Instantiate and run the downloader using the GUI settings
    downloader = Downloader(**settings)
    downloader.download()

except ImportError as e:
    print(f"ERROR: 无法导入 Downloader 类。请确保原始项目文件 ('downloader.py') 存在于 '{original_project_dir}' 目录下。", file=sys.stderr)
    print(f"ImportError: {{e}}", file=sys.stderr)
    sys.exit(1) # Indicate failure
except Exception as e:
    print(f"ERROR: 下载过程中发生错误: {{e}}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr) # Print full traceback to stderr
    sys.exit(1) # Indicate failure
"""
        try:
            with open(temp_runner_script_path, "w", encoding="utf-8") as f:
                f.write(runner_script_content)
            self.console_widget.append_output(f"INFO: 生成临时运行脚本: {temp_runner_script_path}")
        except IOError as e:
            self.console_widget.append_output(f"ERROR: 无法写入临时运行脚本: {e}")
            return

        # 运行临时脚本
        command = [sys.executable, temp_runner_script_name]
        
        # 禁用/启用按钮
        self.start_button.setEnabled(False)
        self.convert_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        # 设置工作目录并启动进程
        try:
            self.process.setWorkingDirectory(self.project_root_dir)
            self.process.start(command[0], command[1:])
        except Exception as e:
            self.console_widget.append_output(f"ERROR: 启动下载进程失败: {e}")
            self.start_button.setEnabled(True)
            self.convert_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def stop_download(self):
        if self.process and self.process.state() != QProcess.ProcessState.NotRunning:
            self.console_widget.append_output("INFO: 正在尝试停止下载...")
            # Terminate is more graceful, kill is forceful
            self.process.terminate() # Or process.kill()
            self.statusBar().showMessage("发送停止信号...", 3000)
            # The handle_process_finished will be called after terminate/kill


    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        try:
            # Decode assuming UTF-8, ignore errors
            text = str(data, encoding='utf-8', errors='ignore').strip()
            if text:
                # Append line by line or as a block
                self.console_widget.append_output(text)
        except Exception as e:
             self.console_widget.append_output(f"[GUI Error decoding stdout: {e}]")


    def handle_stderr(self):
        data = self.process.readAllStandardError()
        try:
            # Decode assuming UTF-8, ignore errors
            text = str(data, encoding='utf-8', errors='ignore').strip()
            if text:
                 # Prepend "STDERR: " or highlight
                 self.console_widget.append_output(f"STDERR: {text}")
        except Exception as e:
             self.console_widget.append_output(f"[GUI Error decoding stderr: {e}]")


    def handle_process_finished(self, exit_code, exit_status):
        self.start_button.setEnabled(self.project_root_valid) # Only enable if project root is valid
        self.stop_button.setEnabled(False)
        self.convert_button.setEnabled(self.project_root_valid) # Enable convert button if valid

        # Clean up temporary runner script ONLY if it was the download process
        temp_runner_script_path = os.path.join(self.project_root_dir, "temp_gui_runner.py")
        if os.path.exists(temp_runner_script_path):
             # We only clean it up if the command *was* running this temp script
             # Check the command that finished? Or assume any finish cleans it?
             # Let's check the command. QProcess doesn't store command easily.
             # A simple way: just try removing it, if it's not the temp script, remove will fail gracefully.
            try:
                if self.process.program() == (sys.executable if sys.executable else 'python') and \
                   os.path.basename(self.process.arguments()[0]) == "temp_gui_runner.py":
                        os.remove(temp_runner_script_path)
                        self.console_widget.append_output("INFO: 已清理临时下载运行脚本。")
            except Exception as e:
                 # print(f"Debug: Error trying to cleanup temp script: {e}", file=sys.stderr) # Debug
                 pass # Ignore errors if the file wasn't the temp runner

        # Determine status message
        status_message = "已完成"
        # Use self.process.program() and arguments to identify the operation?
        # Or pass operation_description to handle_process_finished?
        # For simplicity now, use generic message

        if exit_status == QProcess.ExitStatus.NormalExit:
            if exit_code == 0:
                 status_message = "已正常完成"
            else:
                 status_message = f"完成 (退出码非零: {exit_code})"
        elif exit_status == QProcess.ExitStatus.CrashExit:
            status_message = "崩溃或异常退出"
        else: # QProcess.ExitStatus.UnknownExit
             status_message = f"结束 (未知状态: {exit_status})"


        self.console_widget.append_output(f"INFO: 操作过程 {status_message}.")
        self.statusBar().showMessage(f"操作过程 {status_message}", 5000)


    def handle_process_error(self, error):
        # This signal indicates an error *starting* the process, not error from stderr
        error_str = self.process.errorString()
        self.console_widget.append_output(f"ERROR: QProcess 启动或执行失败: {error_str}")
        # handle_process_finished will also be called after this


    def closeEvent(self, event):
        # Clean up running process if any
        if self.process and self.process.state() != QProcess.ProcessState.NotRunning:
            reply = QMessageBox.question(self, "确认退出",
                                         "有操作（下载、PDF转换、依赖安装等）正在进行中，确定要退出吗？这会终止正在进行的进程。",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.process.kill() # Terminate the process forcefully
                if not self.process.waitForFinished(2000): # Wait a bit
                    print("Warning: Process did not finish after kill.", file=sys.stderr)
                event.accept() # Accept the close event
            else:
                event.ignore() # Ignore the close event
        else:
            event.accept() # No process running, just close

    def _browse_input_dir(self):
        """打开目录对话框选择输入图片文件夹"""
        directory = QFileDialog.getExistingDirectory(
            self,
            self.tr("Select Input Directory"),
            self.input_dir_edit.text() or QDir.homePath()
        )
        if directory:
            self.input_dir_edit.setText(directory)
            # 根据输入目录自动填充输出PDF路径
            base_name = os.path.basename(directory) or "output"
            default_output_pdf = os.path.join(directory, f"{base_name}.pdf")
            self.output_pdf_edit.setText(default_output_pdf)

    def _browse_output_pdf(self):
        """打开保存文件对话框指定输出PDF文件"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            self.tr("Select Output PDF"),
            self.output_pdf_edit.text() or QDir.homePath(),
            "PDF files (*.pdf);;All files (*)"
        )
        if file_path:
            self.output_pdf_edit.setText(file_path)

    def _convert_to_pdf(self):
        """验证输入并转换图片为PDF"""
        input_dir = self.input_dir_edit.text().strip()
        output_pdf = self.output_pdf_edit.text().strip()

        # 基本验证
        if not input_dir:
            QMessageBox.warning(self, self.tr("Input Error"), self.tr("Please select an input directory"))
            return
        if not os.path.isdir(input_dir):
            QMessageBox.warning(self, self.tr("Input Error"), self.tr("error_invalid_dir"))
            return
        if not output_pdf:
            QMessageBox.warning(self, self.tr("Input Error"), self.tr("error_specify_output"))
            return
        if not output_pdf.lower().endswith(".pdf"):
            QMessageBox.warning(self, self.tr("Input Error"), self.tr("error_pdf_extension"))
            return

        # 构建命令列表
        script_path = os.path.join(self.project_root_dir, "文件合并2PDF.py")
        command = [sys.executable, script_path, "--input_dir", input_dir, "--output_pdf", output_pdf]

        self.console_widget.clear()
        self.console_widget.append_output(f"INFO: {self.tr('info_start_merge')}")
        self.console_widget.append_output(f"CMD: {' '.join(command)}")
        
        # 切换到控制台选项卡以查看输出
        self.tab_widget.setCurrentWidget(self.console_tab)
        
        # 禁用按钮
        self.start_button.setEnabled(False)
        self.convert_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        try:
            self.process.start(command[0], command[1:])
        except Exception as e:
            self.console_widget.append_output(f"ERROR: 启动PDF转换进程失败: {e}")
            self.start_button.setEnabled(True)
            self.convert_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def check_dependencies(self):
        """检查项目依赖"""
        # Check requirements.txt file
        req_file_path = os.path.join(self.project_root_dir, "requirements.txt")
        if not os.path.exists(req_file_path):
            req_file_path = os.path.join(self.project_root_dir, "requirements_.txt")
            if not os.path.exists(req_file_path):
                QMessageBox.warning(self, "依赖文件不存在", 
                                  "在项目根目录中未找到requirements.txt或requirements_.txt文件。\n无法检查依赖项。")
                return
        
        try:
            # Run pip list command to get installed packages
            result = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
            
            if result.returncode != 0:
                QMessageBox.critical(self, "依赖检查错误", f"运行pip list命令失败:\n{result.stderr}")
                return
                
            installed_packages = result.stdout
            
            # Read requirements file
            with open(req_file_path, "r") as f:
                requirements = f.readlines()
            
            missing_packages = []
            for req in requirements:
                req = req.strip()
                if not req or req.startswith("#"):
                    continue
                    
                # Simple parse requirement
                if "==" in req:
                    package_name = req.split("==")[0].strip()
                elif ">=" in req:
                    package_name = req.split(">=")[0].strip()
                elif "<=" in req:
                    package_name = req.split("<=")[0].strip()
                else:
                    package_name = req.strip()
                    
                if package_name.lower() not in installed_packages.lower():
                    missing_packages.append(req)
            
            if missing_packages:
                msg = "以下依赖项可能缺失或需要更新:\n\n"
                msg += "\n".join(missing_packages)
                msg += "\n\n是否要安装这些依赖项?"
                
                if QMessageBox.question(self, "缺少依赖项", msg, 
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
                    # Install missing dependencies
                    self.console_widget.clear()
                    self.console_widget.append_output(f"INFO: 准备安装依赖项...")
                    
                    cmd = [sys.executable, "-m", "pip", "install", "-r", req_file_path]
                    self.console_widget.append_output(f"CMD: {' '.join(cmd)}")
                    
                    # Switch to console tab
                    self.tab_widget.setCurrentWidget(self.console_tab)
                    
                    # Disable related buttons
                    self.start_button.setEnabled(False)
                    self.convert_button.setEnabled(False)
                    self.stop_button.setEnabled(True)
                    
                    try:
                        self.process.start(cmd[0], cmd[1:])
                    except Exception as e:
                        self.console_widget.append_output(f"ERROR: 启动pip安装进程失败: {e}")
                        self.start_button.setEnabled(True)
                        self.convert_button.setEnabled(True)
                        self.stop_button.setEnabled(False)
            else:
                QMessageBox.information(self, "依赖检查结果", "所有依赖项已安装。")
                
        except Exception as e:
            QMessageBox.critical(self, "依赖检查错误", f"检查依赖项时发生错误:\n{str(e)}")

    def change_language(self):
        """Switch application language"""
        action = self.sender()
        if action and action.isChecked():
            new_language = action.data()
            if new_language != self.current_language:
                self.current_language = new_language
                config.set("language", new_language)
                self.lang = available_languages[new_language]["data"]
                
                # Prompt user to restart application to apply new language
                QMessageBox.information(
                    self, 
                    "Language Changed / 语言已更改 / 言語が変更されました", 
                    "Please restart the application to apply the new language.\n"
                    "请重新启动应用程序以应用新语言。\n"
                    "新しい言語を適用するにはアプリケーションを再起動してください。"
                )

# Note: To add the Image to PDF functionality, you would add another tab or a menu action
# that opens a new dialog (e.g., ImgToPdfDialog), similar to how InferenceSettingsDialog
# and other dialogs work in the reference project. This dialog would have file/directory
# selectors and a button to run the 文件合并2PDF.py script via QProcess.
