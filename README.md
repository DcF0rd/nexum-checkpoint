# NEXUM-CHECKPOINT

**Cross-platform GUI audit tool for local device security posture and operational readiness.**

---

## What Is This?

**NEXUM-CHECKPOINT** is a lightweight, branded audit utility designed to snapshot the security posture of any local device—Windows or Linux. Built for sovereign operators, sysadmins, and cyber newcomers, it delivers clarity, credibility, and control in a single scan.

This is part of the [Apolune Co.](https://github.com/DcFord) artifact arc and the Docf0rd grind series. It’s not just a tool—it’s a legacy move.

---

## Core Features (v0.1)

- OS Detection (Windows/Linux/macOS)
-  Firewall Status
-  Antivirus Status
-  Disk Encryption Check
-  User Account Audit
-  Network Interface Overview
-  System Info Snapshot
-  GUI Dashboard (Tkinter-based)

---

##  How to Run

```bash
git clone https://github.com/yourusername/nexum-checkpoint
cd nexum-checkpoint
python gui/main_gui.py
```

> Requires Python 3.10+ and `tkinter`. Cross-platform compatible.

---

##  File Structure

```
NEXUM-CHECKPOINT/
├── README.md
├── nexum_checkpoint.py
├── gui/
│   └── main_gui.py
├── modules/
│   ├── os_detect.py
│   ├── firewall_check.py
│   ├── av_check.py
│   ├── disk_encryption.py
│   ├── user_audit.py
│   └── network_info.py
├── assets/
│   └── logo.txt
├── exports/
│   └── audit_log_YYYYMMDD.md
└── .gitignore
```

---

##  Roadmap

- [ ] Export results to Markdown/JSON
- [ ] Risk scoring module
- [ ] Auto-remediation suggestions
- [ ] Remote node scan via SSH
- [ ] GUI theming (dark mode, custom fonts)
- [ ] Devlog integration (Docf0rd YouTube series)

---

##  License

MIT — because sovereignty should be open source.

---

##  Author

**Zachary Ford**  
Founder of Apolune Co.  
Architect of Titianix OS(coming soon), Nexum Security(more to come), and Docf0rd  
---
