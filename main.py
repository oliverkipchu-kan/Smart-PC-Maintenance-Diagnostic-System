"""
Smart Computer Maintenance & Diagnostic System
Main entry point for the application.

Author: IT Support System
Version: 1.0
Description: Professional desktop application for Windows system maintenance,
diagnostics, and optimization.
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from utils.logger import setup_logger

logger = setup_logger()

def main():
    """
    Main application entry point.
    """
    try:
        app = QApplication(sys.argv)
        
        # Set application style
        app.setStyle('Fusion')
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        logger.info("Application initialized successfully")
        
        # Run application
        sys.exit(app.exec_())
    
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()