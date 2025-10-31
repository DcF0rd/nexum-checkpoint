## NEXUM-CHECKPOINT: Feature Expansion Summary

This file summarizes the new features added as part of the Feature Expansion Blueprint.

1) Risk Scoring Engine

- Implemented in `modules/risk_score.py`.
- Produces a 0–100 score with deductions and bands (Secure / Needs Attention / At Risk).

2) Remediation Tab

- Implemented in `modules/remediation.py` and integrated into the GUI.
- Fixes are simulated unless the process is run with admin/root privileges. Actions are logged to `logs/remediation.log`.

3) Export + Logging

- `modules/exporter.py` exports JSON and Markdown files to `exports/`.

4) Scan History Viewer

- `modules/history.py` saves and loads scan JSON files under `history/`.

5) Permission Elevation Logic

- `modules/permissions.py` provides `is_admin()` helper.

6) Offline Mode Toggle

- `modules/config.py` persists an `offline_mode` toggle to `config.json` and is exposed in the GUI Settings tab.

Usage and next steps

- Run `python gui/main_gui.py` to open the GUI. Use the Settings tab to toggle Offline Mode.
- To actually apply remediation actions, run the app as administrator/root.
