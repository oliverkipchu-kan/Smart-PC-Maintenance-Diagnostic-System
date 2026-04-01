import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, 
    QMenuBar, QStatusBar, QLabel, QProgressBar
)
from PyQt5.QtCore import QThread, pyqtSignal

class Worker(QThread):
    update_progress = pyqtSignal(int)
    finished = pyqtSignal(dict)

    def run(self):
        # Simulating system diagnostics and cleanup
        import time
        progress = 0
        while progress < 100:
            time.sleep(0.1)  # Simulate work being done
            progress += 10
            self.update_progress.emit(progress)
        # Simulated results summary
        results = {"status": "Cleanup completed successfully", "details": "No issues found."}
        self.finished.emit(results)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Smart PC Maintenance Diagnostic System")
        self.setGeometry(100, 100, 800, 600)

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.create_dashboard_tab(), "Dashboard")
        self.tab_widget.addTab(self.create_diagnostics_tab(), "Diagnostics")
        self.tab_widget.addTab(self.create_optimization_tab(), "Optimization")
        self.tab_widget.addTab(self.create_reports_tab(), "Reports")

        self.setMenuBar(self.create_menu_bar())
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.setCentralWidget(self.tab_widget)

    def create_dashboard_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Dashboard content goes here."))
        tab.setLayout(layout)
        return tab

    def create_diagnostics_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.one_click_fix_btn = QPushButton("ONE-CLICK FIX")
        self.one_click_fix_btn.setStyleSheet("background-color: red; color: white; font-size: 16px;")
        self.one_click_fix_btn.clicked.connect(self.run_diagnostics)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.one_click_fix_btn)
        layout.addWidget(self.progress_bar)
        tab.setLayout(layout)
        return tab

    def create_optimization_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Optimization content goes here."))
        tab.setLayout(layout)
        return tab

    def create_reports_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Reports content goes here."))
        tab.setLayout(layout)
        return tab

    def create_menu_bar(self):
        menu_bar = QMenuBar(self)
        file_menu = menu_bar.addMenu("File")
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        return menu_bar

    def run_diagnostics(self):
        self.worker = Worker()
        self.worker.update_progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.show_results)
        self.worker.start()
    
    def show_results(self, results):
        self.status_bar.showMessage(results["status"])
        # Display results details (could be a dialog or another widget)
        print(results["details"])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
