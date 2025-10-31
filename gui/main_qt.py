"""Modern Qt-based GUI for NEXUM-CHECKPOINT security auditor.

This version uses PyQt5 for a more modern look while preserving all core functionality
of the original Tkinter version.
"""
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QProgressBar, QLabel, QTextEdit,
    QCheckBox, QComboBox, QFrame, QScrollArea, QSizePolicy,
    QStyle, QStyleFactory
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont

# Dark theme colors
DARK_PALETTE = {
    QPalette.Window: QColor("#1e1e1e"),
    QPalette.WindowText: QColor("#ffffff"),
    QPalette.Base: QColor("#2d2d2d"),
    QPalette.AlternateBase: QColor("#37373d"),
    QPalette.ToolTipBase: QColor("#1e1e1e"),
    QPalette.ToolTipText: QColor("#ffffff"),
    QPalette.Text: QColor("#ffffff"),
    QPalette.Button: QColor("#2d2d2d"),
    QPalette.ButtonText: QColor("#ffffff"),
    QPalette.BrightText: QColor("#ffffff"),
    QPalette.Link: QColor("#264f78"),
    QPalette.Highlight: QColor("#264f78"),
    QPalette.HighlightedText: QColor("#ffffff"),
    QPalette.Light: QColor("#3c3c3c"),
}

# Light theme colors
LIGHT_PALETTE = {
    QPalette.Window: QColor("#ffffff"),
    QPalette.WindowText: QColor("#000000"),
    QPalette.Base: QColor("#f0f0f0"),
    QPalette.AlternateBase: QColor("#e8e8e8"),
    QPalette.ToolTipBase: QColor("#ffffff"),
    QPalette.ToolTipText: QColor("#000000"),
    QPalette.Text: QColor("#000000"),
    QPalette.Button: QColor("#f0f0f0"),
    QPalette.ButtonText: QColor("#000000"),
    QPalette.BrightText: QColor("#000000"),
    QPalette.Link: QColor("#007acc"),
    QPalette.Highlight: QColor("#007acc"),
    QPalette.HighlightedText: QColor("#ffffff"),
    QPalette.Light: QColor("#d1d1d1"),
}
import sys
from pathlib import Path
from datetime import datetime
import json

sys.path.append(str(Path(__file__).parent.parent))
from modules import (
    os_detect,
    firewall_check,
    av_check,
    disk_encryption,
    user_audit,
    network_info,
    risk_score,
    remediation,
    exporter,
    history as history_mod,
    permissions,
    config as config_mod
)

# Color schemes for light/dark modes
DARK_COLORS = {
    "bg": "#1e1e1e",
    "fg": "#ffffff",
    "text": "#f0f0f0",
    "header": "#2a2a2a",
    "selected": "#264f78",
    "hover": "#37373d",
    "button": "#2d2d2d",
    "button_text": "#ffffff",
    "button_hover": "#404040",
    "success": "#4ec9b0",
    "warning": "#ce9178",
    "error": "#f14c4c",
    "border": "#3c3c3c",
    "disabled": "#555555",
}

LIGHT_COLORS = {
    "bg": "#ffffff",
    "fg": "#000000",
    "text": "#212121",
    "header": "#f5f5f5",
    "selected": "#007acc",
    "hover": "#e8e8e8",
    "button": "#f0f0f0",
    "button_text": "#000000",
    "button_hover": "#e0e0e0",
    "success": "#2ea043",
    "warning": "#d29922",
    "error": "#cb2431",
    "border": "#d1d1d1",
    "disabled": "#aaaaaa",
}

class ResultsTab(QWidget):
    """Tab showing scan results and risk score."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Score meter section
        score_frame = QFrame()
        score_layout = QHBoxLayout(score_frame)
        
        score_label = QLabel("Risk Score:")
        score_label.setFont(QFont("Segoe UI", 12))
        score_layout.addWidget(score_label)

        self.score_bar = QProgressBar()
        self.score_bar.setRange(0, 100)
        self.score_bar.setValue(100)
        self.score_bar.setFixedWidth(300)
        self.score_bar.setTextVisible(True)
        self.score_bar.setFormat("%v / 100")
        score_layout.addWidget(self.score_bar)

        self.score_status = QLabel("Secure")
        self.score_status.setFont(QFont("Segoe UI", 12))
        score_layout.addWidget(self.score_status)
        
        score_layout.addStretch()
        layout.addWidget(score_frame)

        # Results text area
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setFont(QFont("Consolas", 10))
        layout.addWidget(self.results_text)

    def update_score(self, score):
        """Update the score meter and status."""
        self.score_bar.setValue(score)
        band, color = risk_score.interpret_band(score)
        self.score_status.setText(band)
        # Set color based on band
        if score >= 80:
            self.score_bar.setStyleSheet("QProgressBar::chunk { background-color: #4ec9b0; }")
        elif score >= 50:
            self.score_bar.setStyleSheet("QProgressBar::chunk { background-color: #ce9178; }")
        else:
            self.score_bar.setStyleSheet("QProgressBar::chunk { background-color: #f14c4c; }")

    def update_results(self, text):
        """Update the results text area with new scan results."""
        self.results_text.clear()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.results_text.append(f"Scan Time: {timestamp}\n")
        self.results_text.append("═" * 50 + "\n\n")
        self.results_text.append(text)

class RemediationTab(QWidget):
    """Tab for viewing and applying security fixes."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Header
        header = QLabel("Available Fixes")
        header.setFont(QFont("Segoe UI", 12))
        layout.addWidget(header)

        # Fixes area (scrollable)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        fixes_widget = QWidget()
        self.fixes_layout = QVBoxLayout(fixes_widget)
        
        self.fix_checkboxes = {}
        for fid, desc in remediation.available_fixes().items():
            cb = QCheckBox(desc)
            cb.setFont(QFont("Segoe UI", 10))
            self.fixes_layout.addWidget(cb)
            self.fix_checkboxes[fid] = cb

        self.fixes_layout.addStretch()
        scroll.setWidget(fixes_widget)
        layout.addWidget(scroll)

        # Apply button
        self.apply_btn = QPushButton("Apply Selected Fixes")
        self.apply_btn.setFont(QFont("Segoe UI", 10))
        self.apply_btn.clicked.connect(self.apply_fixes)
        layout.addWidget(self.apply_btn)

        # Log area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 10))
        layout.addWidget(self.log_text)

    def apply_fixes(self):
        """Apply selected remediation actions."""
        selected = [fid for fid, cb in self.fix_checkboxes.items() if cb.isChecked()]
        if not selected:
            self.log_text.append("No fixes selected.\n")
            return

        self.log_text.append(f"Applying fixes: {', '.join(selected)}\n")
        for fid in selected:
            try:
                res = remediation.apply_fix(fid)
                self.log_text.append(f"{fid}: {res}\n")
            except PermissionError as e:
                self.log_text.append(f"{fid}: Permission denied - {e}\n")
        
        # Ensure newest log entries are visible
        sb = self.log_text.verticalScrollBar()
        sb.setValue(sb.maximum())

class HistoryTab(QWidget):
    """Tab for viewing past scan results."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Header
        header = QLabel("Past Scans")
        header.setFont(QFont("Segoe UI", 12))
        layout.addWidget(header)

        # Scan selector
        self.scan_combo = QComboBox()
        self.scan_combo.addItems([p.name for p in history_mod.list_scans()])
        layout.addWidget(self.scan_combo)

        load_btn = QPushButton("Load Selected Scan")
        load_btn.clicked.connect(self.load_selected_scan)
        layout.addWidget(load_btn)

        # History viewer
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        self.history_text.setFont(QFont("Consolas", 10))
        layout.addWidget(self.history_text)

    def load_selected_scan(self):
        """Load and display the selected scan's data."""
        scan_name = self.scan_combo.currentText()
        if not scan_name:
            self.history_text.setText("No scan selected.")
            return

        for p in history_mod.list_scans():
            if p.name == scan_name:
                data = history_mod.load_scan(p)
                self.history_text.clear()
                self.format_and_display_data(data)
                return
        
        self.history_text.setText("Selected scan not found.")

    def format_and_display_data(self, data):
        """Format and display scan data in the text area."""
        def format_dict(d, indent=0):
            text = []
            for k, v in d.items():
                if isinstance(v, dict):
                    text.append("  " * indent + f"{k}:")
                    text.append(format_dict(v, indent + 1))
                elif isinstance(v, list):
                    text.append("  " * indent + f"{k}:")
                    for item in v:
                        if isinstance(item, dict):
                            text.append(format_dict(item, indent + 1))
                        else:
                            text.append("  " * (indent + 1) + f"- {item}")
                else:
                    text.append("  " * indent + f"{k}: {v}")
            return "\n".join(text)

        formatted = format_dict(data)
        self.history_text.setText(formatted)

class SettingsTab(QWidget):
    """Tab for application settings."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = config_mod.load_config()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Header
        header = QLabel("Application Settings")
        header.setFont(QFont("Segoe UI", 12))
        layout.addWidget(header)

        # Offline mode toggle
        self.offline_cb = QCheckBox("Offline Mode (local-only scans)")
        self.offline_cb.setChecked(self.config.get("offline_mode", False))
        self.offline_cb.stateChanged.connect(self.toggle_offline)
        layout.addWidget(self.offline_cb)

        # Theme toggle
        self.theme_cb = QCheckBox("Dark Theme")
        self.theme_cb.setChecked(True)  # Default to dark
        self.theme_cb.stateChanged.connect(self.toggle_theme)
        layout.addWidget(self.theme_cb)

        layout.addStretch()

    def toggle_offline(self, state):
        """Toggle and save offline mode setting."""
        self.config["offline_mode"] = bool(state)
        config_mod.save_config(self.config)
        if self.parent():
            self.parent().parent().update_status(
                f"Offline Mode: {'ON' if state else 'OFF'}"
            )

    def toggle_theme(self, state):
        """Toggle application theme."""
        if self.parent():
            self.parent().parent().apply_theme(dark=bool(state))

class SecurityCheckApp(QMainWindow):
    """Main application window."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NEXUM-CHECKPOINT")
        self.setMinimumSize(1024, 768)
        
        # Set the fusion style for better theme support
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        
        self.setup_ui()
        self.apply_theme(dark=True)  # Start with dark theme

    def setup_ui(self):
        """Initialize the main UI components."""
        # Central widget and main layout
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Create tab widget and tabs
        self.tabs = QTabWidget()
        self.results_tab = ResultsTab()
        self.remediation_tab = RemediationTab()
        self.history_tab = HistoryTab()
        self.settings_tab = SettingsTab()

        self.tabs.addTab(self.results_tab, "Results")
        self.tabs.addTab(self.remediation_tab, "Fix Issues")
        self.tabs.addTab(self.history_tab, "History")
        self.tabs.addTab(self.settings_tab, "Settings")

        # Left sidebar with scan buttons
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)

        # Logo/title
        title = QLabel("NEXUM-CHECKPOINT")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(title)

        # Quick actions section
        actions_label = QLabel("QUICK ACTIONS")
        actions_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        sidebar_layout.addWidget(actions_label)

        quick_scan_btn = QPushButton("🔍 Quick Scan")
        quick_scan_btn.clicked.connect(self.run_quick_scan)
        sidebar_layout.addWidget(quick_scan_btn)

        full_audit_btn = QPushButton("🔬 Full System Audit")
        full_audit_btn.clicked.connect(self.run_full_audit)
        sidebar_layout.addWidget(full_audit_btn)

        sidebar_layout.addWidget(QFrame(frameShape=QFrame.HLine))

        # Individual checks section
        checks_label = QLabel("SYSTEM CHECKS")
        checks_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        sidebar_layout.addWidget(checks_label)

        check_buttons = [
            ("🧠 OS Info", self.run_os_check),
            ("🔐 Firewall", self.run_firewall_check),
            ("🛡️ Antivirus", self.run_av_check),
            ("💾 Disk Encryption", self.run_disk_check),
            ("👤 User Accounts", self.run_user_audit),
            ("📡 Network Info", self.run_network_check)
        ]

        for text, slot in check_buttons:
            btn = QPushButton(text)
            btn.clicked.connect(slot)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # Horizontal layout for sidebar and tabs
        h_layout = QHBoxLayout()
        h_layout.addWidget(sidebar)
        h_layout.addWidget(self.tabs)
        layout.addLayout(h_layout)

        # Status bar
        self.statusBar().showMessage("Ready")

    def apply_theme(self, dark=True):
        """Apply dark or light theme to the application."""
        # Create new palette
        palette = QPalette()
        colors = DARK_PALETTE if dark else LIGHT_PALETTE
        
        # Apply colors to palette
        for role, color in colors.items():
            palette.setColor(role, color)
        
        # Apply palette
        QApplication.setPalette(palette)
        
        # Basic stylesheet for widget appearance
        self.setStyleSheet("""
            QPushButton {
                padding: 5px;
                border: 1px solid;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: palette(Highlight);
            }
            QProgressBar {
                border: 1px solid;
                border-radius: 2px;
                text-align: center;
            }
            QTextEdit {
                border: 1px solid;
                padding: 5px;
            }
            QTabBar::tab {
                padding: 5px 10px;
                border: 1px solid;
            }
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
            }
            QComboBox {
                border: 1px solid;
                border-radius: 3px;
                padding: 5px;
            }
        """)

    def update_status(self, message, timeout=0):
        """Update status bar with optional timeout."""
        self.statusBar().showMessage(message, timeout)

    def format_dict(self, data, indent=0):
        """Format dictionary data for display."""
        text = []
        for key, value in data.items():
            if isinstance(value, dict):
                text.append("  " * indent + f"{key}:")
                text.extend(self.format_dict(value, indent + 1))
            elif isinstance(value, list):
                text.append("  " * indent + f"{key}:")
                for item in value:
                    if isinstance(item, dict):
                        text.extend(self.format_dict(item, indent + 1))
                    else:
                        text.append("  " * (indent + 1) + f"- {item}")
            else:
                text.append("  " * indent + f"{key}: {value}")
        return text

    # Scan methods
    def run_quick_scan(self):
        """Run essential security checks."""
        self.update_status("Running quick scan...")
        
        # OS Check
        os_name, os_version = os_detect.get_os_info()

        # Firewall Check
        fw_status = firewall_check.get_status()

        # Antivirus Check
        av_status = av_check.get_av_status()

        # Compile findings
        quick_findings = {
            "os": {"name": os_name, "version": os_version},
            "firewall": fw_status,
            "antivirus": av_status
        }

        # Score calculation
        scorer = risk_score.RiskScorer()
        mapped = {"firewall": fw_status, "antivirus": av_status}
        score, deductions = scorer.calculate_score(mapped)
        band, _ = risk_score.interpret_band(score)

        # Update UI
        result_text = f"Quick Scan Results\n\n"
        result_text += f"Operating System: {os_name} {os_version}\n\n"
        result_text += f"Firewall: {fw_status.get('status', 'unknown')}\n"
        result_text += f"Antivirus: {av_status.get('status', 'unknown')}\n\n"
        
        if deductions:
            result_text += "Deductions:\n"
            for d in deductions:
                result_text += f" - {d['reason']}: -{d['points']}\n"

        result_text += f"\nRisk Score: {score}/100 ({band})\n"

        self.results_tab.update_results(result_text)
        self.results_tab.update_score(score)
        
        # Save to history
        history_mod.save_scan({
            "timestamp": datetime.now().isoformat(),
            "type": "quick",
            "os": {"name": os_name, "version": os_version},
            "findings": quick_findings,
            "risk_score": score,
            "deductions": deductions
        })

        # Update status
        if score >= 80:
            self.update_status("Quick scan completed - System secure")
        elif score >= 50:
            self.update_status("Quick scan completed - Issues found")
        else:
            self.update_status("Quick scan completed - At risk")

    def run_full_audit(self):
        """Run comprehensive system audit."""
        self.update_status("Running full system audit...")

        # Gather all information
        os_name, os_version = os_detect.get_os_info()
        fw_status = firewall_check.get_status()
        av_status = av_check.get_av_status()
        disk_status = disk_encryption.get_encryption_status()
        user_status = user_audit.get_user_accounts()
        net_info = network_info.get_network_info()

        # Compile data
        audit_data = {
            "timestamp": datetime.now().isoformat(),
            "os": {"name": os_name, "version": os_version},
            "firewall": fw_status,
            "antivirus": av_status,
            "disk_encryption": disk_status,
            "user_accounts": user_status,
            "network": net_info
        }

        # Score calculation
        scorer = risk_score.RiskScorer()
        mapped = {
            "firewall": fw_status,
            "antivirus": av_status,
            "disk_encryption": disk_status,
            "user_accounts": user_status
        }
        score, deductions = scorer.calculate_score(mapped)
        audit_data["risk_score"] = score
        audit_data["deductions"] = deductions

        # Export
        json_file = exporter.export_json(audit_data)
        md_file = exporter.export_markdown({
            "os": audit_data["os"],
            "risk_score": score,
            "findings": audit_data
        })

        # Save to history
        history_mod.save_scan(audit_data)

        # Update UI
        result_lines = ["Full System Audit Results\n"]
        result_lines.extend(self.format_dict(audit_data))
        result_lines.append(f"\nAudit logs saved to:")
        result_lines.append(f"- {json_file.name}")
        result_lines.append(f"- {md_file.name}")

        self.results_tab.update_results("\n".join(result_lines))
        self.results_tab.update_score(score)
        self.update_status("Full audit completed")

    def run_os_check(self):
        self.update_status("Checking OS information...")
        os_name, os_version = os_detect.get_os_info()
        self.results_tab.update_results(
            f"Operating System Information:\n\n"
            f"System: {os_name}\n"
            f"Version: {os_version}"
        )
        self.update_status("Ready")

    def run_firewall_check(self):
        self.update_status("Checking firewall status...")
        fw_status = firewall_check.get_status()
        self.results_tab.update_results(
            "Firewall Status:\n\n" + "\n".join(self.format_dict(fw_status))
        )
        self.update_status("Ready")

    def run_av_check(self):
        self.update_status("Checking antivirus status...")
        av_status = av_check.get_av_status()
        self.results_tab.update_results(
            "Antivirus Status:\n\n" + "\n".join(self.format_dict(av_status))
        )
        self.update_status("Ready")

    def run_disk_check(self):
        self.update_status("Checking disk encryption...")
        disk_status = disk_encryption.get_encryption_status()
        self.results_tab.update_results(
            "Disk Encryption Status:\n\n" + "\n".join(self.format_dict(disk_status))
        )
        self.update_status("Ready")

    def run_user_audit(self):
        self.update_status("Auditing user accounts...")
        user_status = user_audit.get_user_accounts()
        self.results_tab.update_results(
            "User Account Audit:\n\n" + "\n".join(self.format_dict(user_status))
        )
        self.update_status("Ready")

    def run_network_check(self):
        self.update_status("Gathering network information...")
        net_info = network_info.get_network_info()
        self.results_tab.update_results(
            "Network Information:\n\n" + "\n".join(self.format_dict(net_info))
        )
        self.update_status("Ready")

def main():
    app = QApplication(sys.argv)
    window = SecurityCheckApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()