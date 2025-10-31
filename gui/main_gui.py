import tkinter as tk
from tkinter import ttk, scrolledtext, font
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
    network_info
)
from modules import (
    risk_score,
    remediation,
    exporter,
    history as history_mod,
    permissions,
    config as config_mod
)

# Color scheme (GitHub Copilot dark theme inspired)
COLORS = {
    "bg": "#1e1e1e",
    "fg": "#ffffff",  # Brighter white for better contrast
    "selected": "#264f78",
    "hover": "#37373d",
    "button": "#2d2d2d",  # Slightly darker for buttons
    "button_text": "#0e0d0d",  # White text for buttons
    "button_hover": "#404040",  # Lighter hover state
    "button_hover_text": "#0e0d0d",  # White text on hover
    "success": "#4ec9b0",
    "warning": "#ce9178",
    "error": "#f14c4c",
    "border": "#3c3c3c",
    "separator": "#404040"
}

class SecurityCheckApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NEXUM-CHECKPOINT")
        self.root.geometry("1024x768")
        self.root.configure(bg=COLORS["bg"])
        
        # Configure root grid
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)  # Main content area
        
        # Configure custom styles
        self.setup_styles()
        
        # Load logo
        logo_path = Path(__file__).parent.parent / "assets" / "logo.txt"
        try:
            with open(logo_path, 'r') as f:
                self.logo_text = f.read()
        except:
            self.logo_text = "NEXUM-CHECKPOINT"
        
        # Setup the main layout
        self.setup_layout()
        
    def setup_styles(self):
        """Configure custom styles for the application"""
        style = ttk.Style()
        style.configure(".", background=COLORS["bg"], foreground=COLORS["fg"])
        
        # Configure custom fonts
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=10)
        
        # Button styles
        style.configure(
            "Custom.TButton",
            background=COLORS["button"],
            foreground=COLORS["button_text"],
            padding=(10, 5),
            font=("Segoe UI", 10, "bold"),  # Made text bold for better visibility
            borderwidth=1,  # Added subtle border
            relief="flat"
        )
        style.map(
            "Custom.TButton",
            background=[("active", COLORS["button_hover"]), ("pressed", COLORS["selected"])],
            foreground=[("active", COLORS["button_hover_text"])],
            relief=[("pressed", "sunken")]
        )
        
        # Label styles
        style.configure(
            "Header.TLabel",
            background=COLORS["bg"],
            foreground=COLORS["fg"],
            font=("Segoe UI", 20, "bold")
        )
        style.configure(
            "Subheader.TLabel",
            background=COLORS["bg"],
            foreground=COLORS["fg"],
            font=("Segoe UI", 12)
        )
        style.configure(
            "Status.TLabel",
            background=COLORS["bg"],
            foreground=COLORS["fg"],
            font=("Segoe UI", 10)
        )
        
        # Frame styles
        style.configure(
            "Nav.TFrame",
            background=COLORS["button"],
            relief="flat"
        )
        style.configure(
            "Content.TFrame",
            background=COLORS["bg"],
            relief="flat"
        )
        
        # Separator style
        style.configure(
            "TSeparator",
            background=COLORS["separator"]
        )

    def setup_layout(self):
        """Setup the main application layout"""
        # Left Navigation Panel
        nav_panel = ttk.Frame(self.root, style="Nav.TFrame", width=250)
        nav_panel.grid(row=0, column=0, rowspan=3, sticky="nsew")
        nav_panel.grid_propagate(False)
        
        # Logo area
        logo_frame = ttk.Frame(nav_panel, style="Nav.TFrame")
        logo_frame.pack(fill="x", pady=(20, 30))
        logo_label = ttk.Label(
            logo_frame,
            text=self.logo_text,
            style="Header.TLabel",
            anchor="center",
            justify="center"
        )
        logo_label.pack(pady=10)
        
        # Navigation buttons
        btn_frame = ttk.Frame(nav_panel, style="Nav.TFrame")
        btn_frame.pack(fill="x", padx=10)
        
        # Quick actions
        ttk.Label(btn_frame, text="QUICK ACTIONS", style="Subheader.TLabel").pack(fill="x", pady=(0, 10))
        ttk.Button(btn_frame, text="🔍 Quick Scan", command=self.run_quick_scan, style="Custom.TButton").pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="🔬 Full System Audit", command=self.run_full_audit, style="Custom.TButton").pack(fill="x", pady=2)
        
        ttk.Separator(btn_frame, orient="horizontal").pack(fill="x", pady=20)
        
        # Individual checks
        ttk.Label(btn_frame, text="SYSTEM CHECKS", style="Subheader.TLabel").pack(fill="x", pady=(0, 10))
        check_buttons = [
            ("🧠 OS Info", self.run_os_check),
            ("🔐 Firewall", self.run_firewall_check),
            ("🛡️ Antivirus", self.run_av_check),
            ("💾 Disk Encryption", self.run_disk_check),
            ("👤 User Accounts", self.run_user_audit),
            ("📡 Network Info", self.run_network_check)
        ]
        
        for text, command in check_buttons:
            ttk.Button(btn_frame, text=text, command=command, style="Custom.TButton").pack(fill="x", pady=2)
        
        # Main Content Area - use Notebook with tabs: Results / Fix Issues / History / Settings
        content_frame = ttk.Frame(self.root, style="Content.TFrame")
        content_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=20, pady=20)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # Notebook for content
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        # Results tab
        results_tab = ttk.Frame(self.notebook, style="Content.TFrame")
        self.notebook.add(results_tab, text="Results")
        results_header = ttk.Label(results_tab, text="Security Scan Results", style="Header.TLabel")
        results_header.pack(anchor="w", pady=(0, 10))

        # Risk score meter
        score_frame = ttk.Frame(results_tab, style="Content.TFrame")
        score_frame.pack(fill="x", pady=(0, 10))
        ttk.Label(score_frame, text="Risk Score:", style="Subheader.TLabel").pack(side=tk.LEFT)
        self.score_var = tk.IntVar(value=100)
        self.score_bar = ttk.Progressbar(score_frame, orient="horizontal", length=300, mode="determinate", maximum=100, variable=self.score_var)
        self.score_bar.pack(side=tk.LEFT, padx=10)
        self.score_label = ttk.Label(score_frame, text="100 / 100", style="Subheader.TLabel")
        self.score_label.pack(side=tk.LEFT, padx=10)

        # Results text area
        self.result_text = scrolledtext.ScrolledText(
            results_tab,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg=COLORS["bg"],
            fg=COLORS["fg"],
            insertbackground=COLORS["fg"],
            selectbackground=COLORS["selected"],
            selectforeground=COLORS["fg"],
            relief="flat",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["selected"]
        )
        self.result_text.pack(fill="both", expand=True)
        self.result_text.config(state=tk.DISABLED)

        # Fix Issues tab
        fix_tab = ttk.Frame(self.notebook, style="Content.TFrame")
        self.notebook.add(fix_tab, text="Fix Issues")
        ttk.Label(fix_tab, text="Available Fixes", style="Subheader.TLabel").pack(anchor="w", pady=(10, 5))
        self.fix_vars = {}
        for fid, desc in remediation.available_fixes().items():
            var = tk.BooleanVar(value=False)
            chk = ttk.Checkbutton(fix_tab, text=desc, variable=var)
            chk.pack(anchor="w", padx=10, pady=2)
            self.fix_vars[fid] = var

        ttk.Button(fix_tab, text="Apply Fixes", style="Custom.TButton", command=self.apply_fixes).pack(pady=10)
        self.fix_log = scrolledtext.ScrolledText(fix_tab, height=8, bg=COLORS["bg"], fg=COLORS["fg"]) 
        self.fix_log.pack(fill="both", expand=True, padx=5, pady=5)

        # History tab
        history_tab = ttk.Frame(self.notebook, style="Content.TFrame")
        self.notebook.add(history_tab, text="History")
        ttk.Label(history_tab, text="Past Scans", style="Subheader.TLabel").pack(anchor="w", pady=(10, 5))
        self.scan_list = ttk.Combobox(history_tab, values=[p.name for p in history_mod.list_scans()])
        self.scan_list.pack(fill="x", padx=5, pady=2)
        ttk.Button(history_tab, text="Load Scan", style="Custom.TButton", command=self.load_selected_scan).pack(pady=5)
        self.history_text = scrolledtext.ScrolledText(history_tab, height=12, bg=COLORS["bg"], fg=COLORS["fg"]) 
        self.history_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Settings tab
        settings_tab = ttk.Frame(self.notebook, style="Content.TFrame")
        self.notebook.add(settings_tab, text="Settings")
        ttk.Label(settings_tab, text="Application Settings", style="Subheader.TLabel").pack(anchor="w", pady=(10, 5))
        self.config = config_mod.load_config()
        self.offline_var = tk.BooleanVar(value=self.config.get("offline_mode", False))
        ttk.Checkbutton(settings_tab, text="Offline Mode (local-only scans)", variable=self.offline_var, command=self.toggle_offline).pack(anchor="w", padx=10, pady=5)
        
        # Status bar
        status_frame = ttk.Frame(self.root, style="Content.TFrame")
        status_frame.grid(row=2, column=1, sticky="ew")
        self.status_label = ttk.Label(status_frame, text="Ready", style="Status.TLabel")
        self.status_label.pack(side=tk.LEFT, padx=20, pady=5)
        
    def update_status(self, text, status_type="normal"):
        """Update status bar with text and appropriate color"""
        color = {
            "normal": COLORS["fg"],
            "success": COLORS["success"],
            "warning": COLORS["warning"],
            "error": COLORS["error"]
        }.get(status_type, COLORS["fg"])
        
        self.status_label.configure(text=text, foreground=color)
        self.root.update()

    def update_results(self, text):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        # Add timestamp header
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.result_text.insert(tk.END, f"Scan Time: {timestamp}\n", "timestamp")
        self.result_text.insert(tk.END, "═" * 50 + "\n\n", "separator")
        
        # Insert main content
        self.result_text.insert(tk.END, text)
        
        # Configure tags for styling
        self.result_text.tag_configure("timestamp", foreground=COLORS["success"])
        self.result_text.tag_configure("separator", foreground=COLORS["separator"])
        self.result_text.tag_configure("warning", foreground=COLORS["warning"])
        self.result_text.tag_configure("error", foreground=COLORS["error"])
        self.result_text.tag_configure("success", foreground=COLORS["success"])
        
        self.result_text.config(state=tk.DISABLED)
        self.result_text.see("1.0")

    def format_dict(self, data, indent=0):
        """Format dictionary data for display"""
        text = ""
        for key, value in data.items():
            if isinstance(value, dict):
                text += "  " * indent + f"{key}:\n"
                text += self.format_dict(value, indent + 1)
            elif isinstance(value, list):
                text += "  " * indent + f"{key}:\n"
                for item in value:
                    if isinstance(item, dict):
                        text += self.format_dict(item, indent + 1)
                    else:
                        text += "  " * (indent + 1) + f"- {item}\n"
            else:
                text += "  " * indent + f"{key}: {value}\n"
        return text

    def run_os_check(self):
        self.update_status("Checking OS information...")
        os_name, os_version = os_detect.get_os_info()
        self.update_results(f"Operating System Information:\n\n"
                            f"System: {os_name}\n"
                            f"Version: {os_version}")
        self.update_status("Ready")

    def apply_fixes(self):
        """Apply selected fixes (requires user approval/elevation)."""
        selected = [fid for fid, var in self.fix_vars.items() if var.get()]
        if not selected:
            self.fix_log.insert(tk.END, "No fixes selected.\n")
            return

        self.fix_log.insert(tk.END, f"Applying fixes: {', '.join(selected)}\n")
        for fid in selected:
            try:
                res = remediation.apply_fix(fid)
                self.fix_log.insert(tk.END, f"{fid}: {res}\n")
            except PermissionError as e:
                self.fix_log.insert(tk.END, f"{fid}: Permission denied - {e}\n")
        self.fix_log.see(tk.END)

    def load_selected_scan(self):
        sel = self.scan_list.get()
        if not sel:
            self.history_text.insert(tk.END, "No scan selected.\n")
            return
        # find path
        for p in history_mod.list_scans():
            if p.name == sel:
                data = history_mod.load_scan(p)
                self.history_text.config(state=tk.NORMAL)
                self.history_text.delete(1.0, tk.END)
                self.history_text.insert(tk.END, self.format_dict(data))
                self.history_text.config(state=tk.DISABLED)
                return
        self.history_text.insert(tk.END, "Selected scan not found.\n")

    def toggle_offline(self):
        self.config["offline_mode"] = bool(self.offline_var.get())
        config_mod.save_config(self.config)
        state = "ON" if self.config["offline_mode"] else "OFF"
        self.update_status(f"Offline Mode: {state}")

    def run_firewall_check(self):
        self.update_status("Checking firewall status...")
        fw_status = firewall_check.get_status()
        self.update_results("Firewall Status:\n\n" + self.format_dict(fw_status))
        self.update_status("Ready")

    def run_av_check(self):
        self.update_status("Checking antivirus status...")
        av_status = av_check.get_av_status()
        self.update_results("Antivirus Status:\n\n" + self.format_dict(av_status))
        self.update_status("Ready")

    def run_disk_check(self):
        self.update_status("Checking disk encryption...")
        disk_status = disk_encryption.get_encryption_status()
        self.update_results("Disk Encryption Status:\n\n" + self.format_dict(disk_status))
        self.update_status("Ready")

    def run_user_audit(self):
        self.update_status("Auditing user accounts...")
        user_status = user_audit.get_user_accounts()
        self.update_results("User Account Audit:\n\n" + self.format_dict(user_status))
        self.update_status("Ready")

    def run_network_check(self):
        self.update_status("Gathering network information...")
        net_info = network_info.get_network_info()
        self.update_results("Network Information:\n\n" + self.format_dict(net_info))
        self.update_status("Ready")

    def run_quick_scan(self):
        """Run essential security checks"""
        self.update_status("Initializing quick scan...", "normal")

        # OS Check
        self.update_status("Checking operating system...", "normal")
        os_name, os_version = os_detect.get_os_info()

        # Firewall Check
        self.update_status("Checking firewall status...", "normal")
        fw_status = firewall_check.get_status()

        # Antivirus Check
        self.update_status("Checking antivirus status...", "normal")
        av_status = av_check.get_av_status()

        # Compile results
        quick_findings = {
            "os": {"name": os_name, "version": os_version},
            "firewall": fw_status,
            "antivirus": av_status
        }

        # Compute risk score
        scorer = risk_score.RiskScorer()
        # Map quick_findings to expected keys for scorer
        mapped = {
            "firewall": fw_status,
            "antivirus": av_status,
            # other keys default
        }
        score, deductions = scorer.calculate_score(mapped)
        band, _ = risk_score.interpret_band(score)

        # Display results
        result_text = "� Quick Scan Results\n\n"
        result_text += f"🖥️ Operating System: {os_name} {os_version}\n\n"
        result_text += f"🔐 Firewall: {fw_status.get('status', 'unknown')}\n"
        result_text += f"🛡️ Antivirus: {av_status.get('status', 'unknown')}\n\n"
        if deductions:
            result_text += "Deductions:\n"
            for d in deductions:
                result_text += f" - {d['reason']}: -{d['points']}\n"

        result_text += f"\nRisk Score: {score}/100 ({band})\n"

        # Update score UI
        try:
            self.score_var.set(score)
            self.score_label.configure(text=f"{score} / 100")
        except Exception:
            pass

        self.update_results(result_text)

        # Save to history (quick)
        history_mod.save_scan({
            "timestamp": datetime.now().isoformat(),
            "type": "quick",
            "os": {"name": os_name, "version": os_version},
            "findings": quick_findings,
            "risk_score": score,
            "deductions": deductions
        })

        # Status
        if score >= 80:
            self.update_status("Quick scan completed - System secure", "success")
        elif score >= 50:
            self.update_status("Quick scan completed - Issues found", "warning")
        else:
            self.update_status("Quick scan completed - At risk", "error")

    def run_full_audit(self):
        """Run comprehensive system audit"""
        self.update_status("Running full system audit...")

        # Gather all information
        os_name, os_version = os_detect.get_os_info()
        fw_status = firewall_check.get_status()
        av_status = av_check.get_av_status()
        disk_status = disk_encryption.get_encryption_status()
        user_status = user_audit.get_user_accounts()
        net_info = network_info.get_network_info()

        # Compile audit data
        audit_data = {
            "timestamp": datetime.now().isoformat(),
            "os": {"name": os_name, "version": os_version},
            "firewall": fw_status,
            "antivirus": av_status,
            "disk_encryption": disk_status,
            "user_accounts": user_status,
            "network": net_info
        }

        # Score the audit
        scorer = risk_score.RiskScorer()
        mapped = {
            "firewall": fw_status,
            "antivirus": av_status,
            "disk_encryption": disk_status,
            "user_accounts": user_status,
            # updates key may be added elsewhere
        }
        score, deductions = scorer.calculate_score(mapped)
        audit_data["risk_score"] = score
        audit_data["deductions"] = deductions

        # Exports via exporter module
        json_file = exporter.export_json(audit_data)
        md_file = exporter.export_markdown({"os": audit_data.get("os"), "risk_score": score, "findings": audit_data})

        # Save to history folder
        history_mod.save_scan(audit_data)
        
        # Update score UI
        try:
            self.score_var.set(score)
            self.score_label.configure(text=f"{score} / 100")
        except Exception:
            pass

        # Display results
        self.update_results("Full System Audit Results:\n\n" + 
                            self.format_dict(audit_data) +
                            f"\nAudit logs have been saved to:\n" +
                            f"- {json_file.name}\n" +
                            f"- {md_file.name}")
        self.update_status("Ready")

if __name__ == "__main__":
    root = tk.Tk()
    app = SecurityCheckApp(root)
    root.mainloop()
