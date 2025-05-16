class Language:
    def __init__(self, translations):
        self.translations = translations
    
    def get(self, key, default=None):
        return self.translations.get(key, default or key)

# 中文翻译
zh_CN = Language({
    # 主窗口
    "app_title": "漫画下载器 GUI",
    "settings_tab": "下载设置",
    "console_tab": "控制台输出",
    "img_to_pdf_tab": "图片转PDF",
    "start_button": "开始下载",
    "stop_button": "停止下载",
    
    # 菜单
    "menu_file": "文件",
    "menu_settings": "设置...",
    "menu_check_deps": "检查/安装依赖",
    "menu_exit": "退出",
    "menu_help": "帮助",
    "menu_about": "关于...",
    "menu_language": "语言",
    
    # 设置对话框
    "settings_title": "设置",
    "project_root": "项目根目录:",
    "browse_button": "浏览...",
    "project_root_help": "项目根目录是包含原始 main.py 和 downloader.py 文件的文件夹。\n更改此设置将影响下载功能和图片转PDF功能的工作目录。",
    "chrome_path": "Chrome浏览器路径:",
    "chromedriver_path": "ChromeDriver路径:",
    "chrome_version_help": "指定Chrome和ChromeDriver的路径。\n确保两者版本匹配，否则可能导致下载失败。",
    
    # 图片转PDF
    "input_dir": "输入图片目录：",
    "output_pdf": "输出PDF文件：",
    "convert_button": "转换为PDF",
    
    # 消息
    "error_invalid_dir": "指定的输入目录不存在或不是一个有效的目录。",
    "error_specify_output": "请指定输出的PDF文件路径。",
    "error_pdf_extension": "输出文件路径应以 '.pdf' 结尾。",
    "info_start_merge": "开始将图片合并为PDF...",
    "info_start_download": "准备开始下载...",
    "process_complete": "进程已正常完成",
    "path_updated": "项目根目录已更新",
    "invalid_path": "选择的不是一个有效的目录，项目根目录未更改。",
    
    # 关于对话框
    "about_title": "关于漫画下载器",
    "version": "版本 1.0.0",
    "about_description": """
        <p style='text-align:center;'>这是一个用于下载漫画和将图片合成PDF的图形界面工具。</p>
        
        <p style='text-align:center;'>主要功能:</p>
        <ul>
            <li>下载漫画图片</li>
            <li>将图片合并为PDF</li>
            <li>配置下载参数</li>
        </ul>
        
        <p><b>使用说明:</b></p>
        <ol>
            <li>在"下载设置"选项卡中配置漫画下载参数</li>
            <li>点击"开始下载"按钮开始下载漫画</li>
            <li>在"图片转PDF"选项卡中选择图片目录并生成PDF</li>
        </ol>
        
        <p style='text-align:center;'>© 2023 漫画下载器团队</p>
    """,
    "close_button": "关闭"
})

# 英文翻译
en_US = Language({
    # Main Window
    "app_title": "Manga Downloader GUI",
    "settings_tab": "Download Settings",
    "console_tab": "Console Output",
    "img_to_pdf_tab": "Image to PDF",
    "start_button": "Start Download",
    "stop_button": "Stop Download",
    
    # Menu
    "menu_file": "File",
    "menu_settings": "Settings...",
    "menu_check_deps": "Check/Install Dependencies",
    "menu_exit": "Exit",
    "menu_help": "Help",
    "menu_about": "About...",
    "menu_language": "Language",
    
    # Settings Dialog
    "settings_title": "Settings",
    "project_root": "Project Root Directory:",
    "browse_button": "Browse...",
    "project_root_help": "The project root directory contains the original main.py and downloader.py files.\nChanging this setting will affect the working directory for download and PDF conversion.",
    "chrome_path": "Chrome Browser Path:",
    "chromedriver_path": "ChromeDriver Path:",
    "chrome_version_help": "Specify the paths for Chrome and ChromeDriver.\nMake sure they match in version, otherwise download may fail.",
    
    # Image to PDF
    "input_dir": "Input Image Directory:",
    "output_pdf": "Output PDF File:",
    "convert_button": "Convert to PDF",
    
    # Messages
    "error_invalid_dir": "The specified input directory does not exist or is not a valid directory.",
    "error_specify_output": "Please specify the output PDF file path.",
    "error_pdf_extension": "Output file path should end with '.pdf'.",
    "info_start_merge": "Starting to merge images to PDF...",
    "info_start_download": "Preparing to start download...",
    "process_complete": "Process completed successfully",
    "path_updated": "Project root directory has been updated",
    "invalid_path": "Selected path is not a valid directory, project root directory remains unchanged.",
    
    # About Dialog
    "about_title": "About Manga Downloader",
    "version": "Version 1.0.0",
    "about_description": """
        <p style='text-align:center;'>This is a GUI tool for downloading manga and converting images to PDF.</p>
        
        <p style='text-align:center;'>Main Features:</p>
        <ul>
            <li>Download manga images</li>
            <li>Merge images to PDF</li>
            <li>Configure download parameters</li>
        </ul>
        
        <p><b>Usage Instructions:</b></p>
        <ol>
            <li>Configure manga download parameters in the "Download Settings" tab</li>
            <li>Click "Start Download" button to start downloading manga</li>
            <li>Select image directory and generate PDF in the "Image to PDF" tab</li>
        </ol>
        
        <p style='text-align:center;'>© 2023 Manga Downloader Team</p>
    """,
    "close_button": "Close"
})

# 日文翻译
ja_JP = Language({
    # メインウィンドウ
    "app_title": "漫画ダウンローダー GUI",
    "settings_tab": "ダウンロード設定",
    "console_tab": "コンソール出力",
    "img_to_pdf_tab": "画像からPDF",
    "start_button": "ダウンロード開始",
    "stop_button": "ダウンロード停止",
    
    # メニュー
    "menu_file": "ファイル",
    "menu_settings": "設定...",
    "menu_check_deps": "依存関係の確認/インストール",
    "menu_exit": "終了",
    "menu_help": "ヘルプ",
    "menu_about": "バージョン情報...",
    "menu_language": "言語",
    
    # 設定ダイアログ
    "settings_title": "設定",
    "project_root": "プロジェクトルートディレクトリ:",
    "browse_button": "参照...",
    "project_root_help": "プロジェクトルートディレクトリには、元のmain.pyとdownloader.pyファイルが含まれています。\nこの設定を変更すると、ダウンロードとPDF変換の作業ディレクトリに影響します。",
    "chrome_path": "Chromeブラウザのパス:",
    "chromedriver_path": "ChromeDriverのパス:",
    "chrome_version_help": "ChromeとChromeDriverのパスを指定します。\nバージョンが一致していることを確認してください。一致していないとダウンロードが失敗する可能性があります。",
    
    # 画像からPDF
    "input_dir": "入力画像ディレクトリ:",
    "output_pdf": "出力PDFファイル:",
    "convert_button": "PDFに変換",
    
    # メッセージ
    "error_invalid_dir": "指定された入力ディレクトリは存在しないか、有効なディレクトリではありません。",
    "error_specify_output": "出力PDFファイルのパスを指定してください。",
    "error_pdf_extension": "出力ファイルのパスは'.pdf'で終わる必要があります。",
    "info_start_merge": "画像のPDF変換を開始しています...",
    "info_start_download": "ダウンロードの準備中...",
    "process_complete": "プロセスが正常に完了しました",
    "path_updated": "プロジェクトルートディレクトリが更新されました",
    "invalid_path": "選択されたパスは有効なディレクトリではありません。プロジェクトルートディレクトリは変更されません。",
    
    # バージョン情報ダイアログ
    "about_title": "漫画ダウンローダーについて",
    "version": "バージョン 1.0.0",
    "about_description": """
        <p style='text-align:center;'>これは漫画のダウンロードと画像のPDF変換のためのGUIツールです。</p>
        
        <p style='text-align:center;'>主な機能:</p>
        <ul>
            <li>漫画画像のダウンロード</li>
            <li>画像のPDF変換</li>
            <li>ダウンロードパラメータの設定</li>
        </ul>
        
        <p><b>使用方法:</b></p>
        <ol>
            <li>「ダウンロード設定」タブで漫画ダウンロードパラメータを設定</li>
            <li>「ダウンロード開始」ボタンをクリックして漫画のダウンロードを開始</li>
            <li>「画像からPDF」タブで画像ディレクトリを選択しPDFを生成</li>
        </ol>
        
        <p style='text-align:center;'>© 2023 漫画ダウンローダーチーム</p>
    """,
    "close_button": "閉じる"
})

# 可用语言列表
available_languages = {
    "zh_CN": {"name": "中文", "data": zh_CN},
    "en_US": {"name": "English", "data": en_US},
    "ja_JP": {"name": "日本語", "data": ja_JP}
}

# 默认语言
default_language = "zh_CN" 