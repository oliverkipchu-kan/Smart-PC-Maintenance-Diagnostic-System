"""
Diagnostics Widget
System diagnostics and troubleshooting interface.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QTextEdit, QProgressBar, QComboBox, QGroupBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from core.troubleshooter import Troubleshooter
from utils.logger import setup_logger

logger = setup_logger()

class DiagnosticsWidget(QWidget):
    """
    Diagnostics interface for running system diagnostics and troubleshooting.
    """
    
    def __init__(self, system_monitor=None):
        """
        Initialize diagnostics widget.
        
        Args:
            system_monitor: SystemMonitor instance
        """
        super().__init__()
        self.system_monitor = system_monitor
        self.troubleshooter = Troubleshooter()
        self.setup_ui()
    
    def setup_ui(self):
        """Set up diagnostics interface."""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Control panel
        control_layout = self._create_control_panel()
        layout.addLayout(control_layout)
        
        # Progress indicator
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Results display
        results_group = QGroupBox("Diagnostic Results")
        results_layout = QVBoxLayout()
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setStyleSheet("""
            QTextEdit {
                background-color: #ecf0f1;
                font-family: 'Courier New';
                font-size: 10px;
            }
        """)
        results_layout.addWidget(self.results_text)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
    
    def _create_control_panel(self):
        """Create control panel for diagnostics."""
        layout = QHBoxLayout()
        
        # Diagnostics selector
        layout.addWidget(QLabel("Select Diagnostic:"))
        self.diagnostic_combo = QComboBox()
        self.diagnostic_combo.addItem("Full System Scan")
        self.diagnostic_combo.addItem("CPU Check")
        self.diagnostic_combo.addItem("Memory Check")
        self.diagnostic_combo.addItem("Disk Check")
        self.diagnostic_combo.addItem("Network Check")
        self.diagnostic_combo.addItem("Performance Analysis")
        layout.addWidget(self.diagnostic_combo)
        
        layout.addStretch()
        
        # Run button
        run_button = QPushButton("▶ Run Diagnostics")
        run_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        run_button.clicked.connect(self.run_diagnostics)
        layout.addWidget(run_button)
        
        # Export button
        export_button = QPushButton("💾 Export Results")
        export_button.clicked.connect(self.export_results)
        layout.addWidget(export_button)
        
        return layout
    
    def run_diagnostics(self):
        """Run selected diagnostics."""
        self.progress_bar.setVisible(True)
        self.results_text.clear()
        
        diagnostic_type = self.diagnostic_combo.currentText()
        self.results_text.setText(f"Running: {diagnostic_type}\n{'=' * 60}\n\n")
        
        try:
            # Run full diagnostics
            results = self.troubleshooter.diagnose_system()
            
            # Format output
            output = self._format_diagnostics_output(results)
            self.results_text.setText(output)
            
            self.progress_bar.setValue(100)
            
        except Exception as e:
            self.results_text.setText(f"Error running diagnostics: {str(e)}")
            logger.error(f"Diagnostics error: {str(e)}")
        
        finally:
            self.progress_bar.setVisible(False)
    
    def _format_diagnostics_output(self, results):
        """
        Format diagnostics results for display.
        
        Args:
            results (dict): Diagnostics results
        
        Returns:
            str: Formatted output
        """
        lines = []
        
        lines.append("SYSTEM DIAGNOSTICS REPORT")
        lines.append("=" * 60)
        lines.append("")
        
        # Summary
        lines.append(f"Issues Found: {results['critical_issues']} Critical, {results['warnings']} Warnings")
        lines.append("")
        
        # Issues
        if results['issues_found']:
            lines.append("DETECTED ISSUES")
            lines.append("-" * 60)
            
            for issue in results['issues_found']:
                lines.append(f"\n✕ {issue['name']} [{issue['severity'].upper()}]")
                lines.append(f"  Status: {issue.get('current_value', 'N/A')}")
                
                if 'top_processes' in issue:
                    lines.append("  Top Processes:")
                    for proc in issue.get('top_processes', [])[:3]:
                        lines.append(f"    - {proc['name']}")
                
                if 'solutions' in issue:
                    lines.append("  Solutions:")
                    for solution in issue['solutions']:
                        lines.append(f"    • {solution}")
                
                lines.append("")
        
        # Healthy checks
        if results['healthy_checks']:
            lines.append("\nHEALTHY COMPONENTS")
            lines.append("-" * 60)
            for check in results['healthy_checks']:
                lines.append(f"✓ {check}")
        
        return "\n".join(lines)
    
    def export_results(self):
        """Export diagnostics results."""
        results = self.results_text.toPlainText()
        
        # Save to file
        from pathlib import Path
        import os
        from datetime import datetime
        
        export_dir = Path('diagnostic_exports')
        export_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = export_dir / f'diagnostics_{timestamp}.txt'
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(results)
            
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(
                self,
                "Export Successful",
                f"Results exported to: {filepath}"
            )
            logger.info(f"Diagnostics exported to {filepath}")
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Export Failed", f"Error exporting results: {str(e)}")
            logger.error(f"Export error: {str(e)}")
