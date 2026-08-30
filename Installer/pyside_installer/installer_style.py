"""Self-contained dark stylesheet for the installer UI.

Deliberately independent from scripts/Styles/ - the installer is a separate
executable that must run before the target app exists on disk at all, so it
cannot import anything from the app it is about to install.
"""

BACKGROUND = "#0d0f17"
SIDEBAR_TOP = "#141827"
SIDEBAR_BOTTOM = "#0a0c14"
PANEL = "#171b28"
BORDER = "#262a3a"
TEXT = "#eef0f6"
SUBTEXT = "#9aa0b8"
MUTED = "#5b6178"
ACCENT = "#00aaff"
ACCENT_2 = "#7c5cff"

WizardStyle = f"""
QWizard {{
    background: {BACKGROUND};
    color: {TEXT};
}}
QWizard QWidget {{
    background: transparent;
    color: {TEXT};
    font-family: 'Segoe UI';
}}

/* --- sidebar --- */
QFrame#Sidebar {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                 stop:0 {SIDEBAR_TOP}, stop:1 {SIDEBAR_BOTTOM});
    border-right: 1px solid {BORDER};
}}
QLabel#SidebarBrand {{
    color: {TEXT};
    font-size: 14px;
    font-weight: 700;
}}
QLabel#SidebarStep {{
    color: {MUTED};
    font-size: 12px;
    padding: 6px 0;
}}
QLabel#SidebarStepActive {{
    color: {TEXT};
    font-size: 12px;
    font-weight: 700;
    padding: 6px 0;
}}
QLabel#SidebarStepDone {{
    color: {ACCENT};
    font-size: 12px;
    padding: 6px 0;
}}

/* --- content --- */
QLabel#TitleLabel {{
    font-size: 22px;
    font-weight: 700;
    color: {TEXT};
}}
QLabel#SubLabel {{
    font-size: 12px;
    color: {SUBTEXT};
}}
QLabel#BadgeLabel {{
    font-size: 11px;
    color: {ACCENT};
    font-weight: 600;
    letter-spacing: 1px;
}}
QLabel#BigPercent {{
    font-size: 40px;
    font-weight: 700;
    color: {TEXT};
}}
QLabel#StatusLine {{
    font-size: 12px;
    color: {SUBTEXT};
}}
QLabel#ChecklistItem {{
    font-size: 12px;
    color: {MUTED};
    padding: 3px 0;
}}
QLabel#ChecklistItemDone {{
    font-size: 12px;
    color: {TEXT};
    padding: 3px 0;
}}

QLineEdit {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 8px 10px;
    color: {TEXT};
}}
QLineEdit:focus {{
    border: 1px solid {ACCENT};
}}
QPushButton {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 8px 18px;
    color: {TEXT};
}}
QPushButton:hover {{
    border: 1px solid {ACCENT};
}}
QPushButton#PrimaryButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                 stop:0 {ACCENT}, stop:1 {ACCENT_2});
    border: none;
    font-weight: 700;
}}
QPushButton#PrimaryButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                 stop:0 {ACCENT_2}, stop:1 {ACCENT});
}}
QCheckBox {{
    color: {TEXT};
    spacing: 10px;
    font-size: 13px;
}}
QProgressBar {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 8px;
    text-align: center;
    color: transparent;
    height: 16px;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                 stop:0 {ACCENT}, stop:1 {ACCENT_2});
    border-radius: 8px;
}}
QFrame#Card {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 12px;
}}
QFrame#IconCircle {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                 stop:0 {ACCENT}, stop:1 {ACCENT_2});
    border-radius: 34px;
}}
QFrame#HeaderRule {{
    background: {BORDER};
    max-height: 1px;
    min-height: 1px;
}}
"""
