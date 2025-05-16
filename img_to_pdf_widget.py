import sys
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QGroupBox, QFileDialog, QMessageBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QProcess, pyqtSignal, QDir # Added QDir

class ImgToPdfWidget(QWidget):
    # Signal to request running a command in the main window's console/process
    # Emits (command_list, operation_description, working_directory)
    # We'll connect this signal in MainWindow to the main window's command execution method
    runCommandRequested = pyqtSignal(list, str, str) # command is a list of strings

    def __init__(self, parent=None, project_root_dir=""):
        super().__init__(parent)
        self.project_root_dir = project_root_dir # Store project root for working directory

        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- Input Directory ---
        input_group = QGroupBox("图片目录")
        input_layout = QHBoxLayout()
        input_label = QLabel("选择包含图片的文件夹:")
        self.input_dir_edit = QLineEdit()
        self.input_dir_browse_button = QPushButton("浏览...")
        self.input_dir_browse_button.clicked.connect(self._browse_input_dir)

        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_dir_edit)
        input_layout.addWidget(self.input_dir_browse_button)
        input_group.setLayout(input_layout)
        self.layout().addWidget(input_group)

        # --- Output File ---
        output_group = QGroupBox("输出文件")
        output_layout = QHBoxLayout()
        output_label = QLabel("指定输出PDF文件路径:")
        self.output_pdf_edit = QLineEdit()
        self.output_pdf_browse_button = QPushButton("浏览...")
        self.output_pdf_browse_button.clicked.connect(self._browse_output_pdf)

        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_pdf_edit)
        output_layout.addWidget(self.output_pdf_browse_button)
        output_group.setLayout(output_layout)
        self.layout().addWidget(output_group)

        # --- Convert Button ---
        self.convert_button = QPushButton("开始合并为PDF")
        self.convert_button.clicked.connect(self._start_conversion)
        self.layout().addWidget(self.convert_button)

        # Add a stretch to push everything to the top
        self.layout().addStretch()

    def _browse_input_dir(self):
        """Opens a directory dialog to select the input image folder."""
        directory = QFileDialog.getExistingDirectory(
            self,
            "选择图片所在的文件夹",
            self.input_dir_edit.text() or self.project_root_dir or QDir.homePath() # Start from current or project root or home
        )
        if directory:
            self.input_dir_edit.setText(os.path.normpath(directory))
            # Auto-fill output PDF path based on input dir
            base_name = os.path.basename(directory) or "output"
            default_output_pdf = os.path.join(directory, f"{base_name}.pdf")
            self.output_pdf_edit.setText(os.path.normpath(default_output_pdf))


    def _browse_output_pdf(self):
        """Opens a save file dialog to specify the output PDF file."""
        # Suggest a default filename based on input dir if available
        input_dir = self.input_dir_edit.text()
        suggested_dir = input_dir if input_dir and os.path.isdir(input_dir) else (self.project_root_dir or QDir.homePath())
        
        # Suggest a default filename
        default_filename = ""
        if input_dir and os.path.isdir(input_dir):
             default_filename = os.path.basename(input_dir) + ".pdf"
        elif self.output_pdf_edit.text():
             default_filename = os.path.basename(self.output_pdf_edit.text())
             suggested_dir = os.path.dirname(self.output_pdf_edit.text()) # Use existing path's dir

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存PDF文件",
            os.path.join(suggested_dir, default_filename), # Initial directory and filename
            "PDF files (*.pdf);;All files (*)" # File filter
        )
        if file_path:
            self.output_pdf_edit.setText(os.path.normpath(file_path))


    def _start_conversion(self):
        """Validates inputs and emits signal to run the conversion script."""
        input_dir = self.input_dir_edit.text().strip()
        output_pdf = self.output_pdf_edit.text().strip()

        # Basic validation
        if not input_dir:
            QMessageBox.warning(self, "输入错误", "请选择包含图片的文件夹。")
            return
        if not os.path.isdir(input_dir):
             QMessageBox.warning(self, "输入错误", f"指定的输入目录 '{input_dir}' 不存在或不是一个有效的目录。")
             return
        if not output_pdf:
            QMessageBox.warning(self, "输入错误", "请指定输出的PDF文件路径。")
            return
        # Optional: Check if output_pdf is a valid file name (e.g., ends with .pdf)
        if not output_pdf.lower().endswith(".pdf"):
             QMessageBox.warning(self, "输入错误", "输出文件路径应以 '.pdf' 结尾。")
             return

        # Determine the path to the conversion script relative to the project root
        # Assumes the script is in the original project root
        script_name = "文件合并2PDF.py"
        script_path_relative = script_name # Assumes script is in project root

        # Build the command list for QProcess
        # command = [sys.executable, os.path.join(self.project_root_dir, script_path_relative),
        #           "--input_dir", input_dir, "--output_pdf", output_pdf]
        # It's better to set working directory and run the script relative to it
        command = [sys.executable, script_path_relative, # Run script relative to working dir
                  "--input_dir", input_dir, "--output_pdf", output_pdf]

        operation_description = f"合并图片 ({os.path.basename(input_dir)}) 为 PDF"

        # Emit the signal to the main window to run the command
        # The working directory for this script should be the original project root
        self.runCommandRequested.emit(command, operation_description, self.project_root_dir)

        # Switch to the console tab to see the output (this is handled in MainWindow)
        # self.parent().tab_widget.setCurrentWidget(self.parent().console_tab)
