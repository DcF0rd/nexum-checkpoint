## 🛡️ NEXUM-CHECKPOINT

**A Cross-Platform GUI Tool for Local Device Health Auditing**

NEXUM-CHECKPOINT is a lightweight utility that provides a quick, visual **snapshot of a device's security and operational readiness** (Windows or Linux). It's built for students, new cyber learners, and anyone practicing **operational sovereignty**—delivering clarity and control over your own machine.

This project is part of my **Docf0rd** build series, documenting the process of learning and shipping a real-world tool.

-----

### **💡 Core Features (v0.1)**

NEXUM-CHECKPOINT focuses on the essential security and system data:

  * **Platform Agnostic:** Runs on Windows and Linux (and conceptually macOS).
  * **Security Checks:** Status of **Firewall** and **Antivirus** presence/status.
  * **System Integrity:** **Disk Encryption** check and a **User Account Audit**.
  * **Networking & Info:** Quick overview of **Network Interfaces** and core **System Info**.
  * **Visual Interface:** Simple, native **Tkinter-based GUI Dashboard**.

-----

### **🚀 How to Run**

To get the NEXUM-CHECKPOINT GUI running locally, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/DcF0rd/nexum-checkpoint
    cd nexum-checkpoint
    ```
2.  **Run the GUI:**
    ```bash
    python gui/main_gui.py
    ```

> **Requirements:** Requires **Python 3.10+** and the built-in **tkinter** library.

-----

### **🗺️ Roadmap (What I'm Learning Next)**

This tool is actively developed. Key features I'm working on include:

  * Export results to standard formats (Markdown/JSON).
  * **Risk Scoring Module** to assign a simple health rating.
  * Auto-remediation suggestions for common issues.
  * GUI enhancements like **Dark Mode** theming.
  * Integration with my **Docf0rd YouTube devlogs**.

-----

### **📁 Project Structure**

```
NEXUM-CHECKPOINT/
├── README.md
├── nexum_checkpoint.py           # Core logic/entry point
├── gui/
│   └── main_gui.py               # Main GUI application
├── modules/                      # Modular checks (os_detect, firewall_check, etc.)
├── assets/                       # UI assets (like logo.txt)
└── exports/                      # Where audit logs will be saved
```

### **📝 License & Author**

  * **License:** MIT — because learning and sovereignty should be **open source**.
  * **Author:** Zachary Ford ([@DcF0rd](https://github.com/DcF0rd))
      * *Building for fun and learning out loud.*
