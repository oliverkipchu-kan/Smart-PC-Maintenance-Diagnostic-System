import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox)
import os

class OptimizationInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('System Optimization Tool')
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()  
        self.status_label = QLabel('Status: Ready')

        self.cleanup_button = QPushButton('Clean Up')
        self.cleanup_button.clicked.connect(self.cleanup)

        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.cleanup_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def cleanup(self):
        self.status_label.setText('Status: Cleaning up...')
        self.perform_cleanup()

    def perform_cleanup(self):
        # Example cleanup operations, you can expand this
        try:
            # Simulate cleanup tasks (dummy implementation)
            temp_files = self.cleanup_temp_files()
            browser_cache = self.cleanup_browser_cache()
            deleted_files = len(temp_files) + len(browser_cache)
            self.status_label.setText(f'Status: Cleaned up {deleted_files} files.')
            self.show_statistics(deleted_files)
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def cleanup_temp_files(self):
        # Implement the actual cleanup logic here
        return []  # Dummy return

    def cleanup_browser_cache(self):
        # Implement the actual cleanup logic here
        return []  # Dummy return

    def show_statistics(self, deleted_files):
        QMessageBox.information(self, 'Statistics', f'Deleted {deleted_files} files.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OptimizationInterface()
    window.show()
    sys.exit(app.exec_())