import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow
import os # Import os to help determine project root

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Determine the path to the original Manga_downloader-master project
    # Assumes this GUI folder is INSIDE the original project folder
    # If your GUI folder is a SIBLING, adjust this path determination logic
    # For example, if GUI is in G:\Manga_downloader-master\GUI, and original project is in G:\Manga_downloader-master\Manga_downloader-master
    # You might need os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Manga_downloader-master")
    # Based on your console output, it seems your GUI files are directly in Manga_downloader-master
    # Let's assume the project root IS the directory containing app.py for simplicity for now.
    # The MainWindow constructor has logic to validate this path.
    # Alternatively, if the structure is Manga_downloader-master/GUI and Manga_downloader-master/OriginalProject
    # gui_dir = os.path.dirname(os.path.abspath(__file__))
    # project_root_dir = os.path.dirname(gui_dir) # Go up one level if GUI is in a subfolder

    # Let's stick to the logic in MainWindow for determining project root initially.
    # But ensure sys.path includes the directory containing main_window.py, etc.
    gui_dir = os.path.dirname(os.path.abspath(__file__))
    if gui_dir not in sys.path:
        sys.path.insert(0, gui_dir)

    # Create the main window
    main_window = MainWindow() # MainWindow constructor will handle project root validation

    # Show the main window
    main_window.show()

    # Start the application event loop
    sys.exit(app.exec())
