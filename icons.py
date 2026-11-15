"""
SkillSync 2.0 - Lucide SVG Icon System
Provides clean, consistent, line-based SVG icons without emoji or external font dependencies.
Matches the Obsidian Gold & Ivory Light luxury design system.
"""

from typing import Dict, Optional

# Standard Lucide SVG Path Definitions (viewBox="0 0 24 24", stroke-width="2", fill="none")
LUCIDE_PATHS: Dict[str, str] = {
    "layout-dashboard": (
        '<rect width="7" height="9" x="3" y="3" rx="1"/>'
        '<rect width="7" height="5" x="14" y="3" rx="1"/>'
        '<rect width="7" height="9" x="14" y="12" rx="1"/>'
        '<rect width="7" height="5" x="3" y="16" rx="1"/>'
    ),
    "route": (
        '<circle cx="6" cy="19" r="3"/>'
        '<path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/>'
        '<circle cx="18" cy="5" r="3"/>'
    ),
    "chart-no-axes-combined": (
        '<path d="M12 16v5"/>'
        '<path d="M16 14v7"/>'
        '<path d="M20 10v11"/>'
        '<path d="m22 3-8.646 8.646a.5.5 0 0 1-.708 0L9.354 8.354a.5.5 0 0 0-.707 0L2 15"/>'
        '<path d="M4 18v3"/>'
        '<path d="M8 14v7"/>'
    ),
    "file-search": (
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
        '<polyline points="14 2 14 8 20 8"/>'
        '<circle cx="11.5" cy="14.5" r="2.5"/>'
        '<path d="m13.3 16.3 1.7 1.7"/>'
    ),
    "messages-square": (
        '<path d="M14 9a2 2 0 0 1-2 2H6l-4 4V4c0-1.1.9-2 2-2h8a2 2 0 0 1 2 2z"/>'
        '<path d="M18 9h2a2 2 0 0 1 2 2v11l-4-4h-6a2 2 0 0 1-2-2v-1"/>'
    ),
    "briefcase-business": (
        '<rect width="20" height="14" x="2" y="7" rx="2"/>'
        '<path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>'
        '<path d="M12 12v.01"/>'
    ),
    "book-open": (
        '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>'
        '<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>'
    ),
    "settings": (
        '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>'
        '<circle cx="12" cy="12" r="3"/>'
    ),
    "search": (
        '<circle cx="11" cy="11" r="8"/>'
        '<path d="m21 21-4.3-4.3"/>'
    ),
    "bell": (
        '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/>'
        '<path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>'
    ),
    "user-round": (
        '<circle cx="12" cy="8" r="5"/>'
        '<path d="M20 21a8 8 0 0 0-16 0"/>'
    ),
    "sun": (
        '<circle cx="12" cy="12" r="4"/>'
        '<path d="M12 2v2"/>'
        '<path d="M12 20v2"/>'
        '<path d="m4.93 4.93 1.41 1.41"/>'
        '<path d="m17.66 17.66 1.41 1.41"/>'
        '<path d="M2 12h2"/>'
        '<path d="M20 12h2"/>'
        '<path d="m6.34 17.66-1.41 1.41"/>'
        '<path d="m19.07 4.93-1.41 1.41"/>'
    ),
    "moon": (
        '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>'
    ),
    "trending-up": (
        '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>'
        '<polyline points="16 7 22 7 22 13"/>'
    ),
    "brain": (
        '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/>'
        '<path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/>'
        '<path d="M12 5v14"/>'
    ),
    "circle-check": (
        '<circle cx="12" cy="12" r="10"/>'
        '<path d="m9 12 2 2 4-4"/>'
    ),
    "triangle-alert": (
        '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>'
        '<line x1="12" y1="9" x2="12" y2="13"/>'
        '<line x1="12" y1="17" x2="12.01" y2="17"/>'
    ),
    "download": (
        '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
        '<polyline points="7 10 12 15 17 10"/>'
        '<line x1="12" y1="15" x2="12" y2="3"/>'
    ),
    "upload": (
        '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
        '<polyline points="17 8 12 3 7 8"/>'
        '<line x1="12" y1="3" x2="12" y2="15"/>'
    ),
    "calendar-days": (
        '<rect width="18" height="18" x="3" y="4" rx="2" ry="2"/>'
        '<line x1="16" y1="2" x2="16" y2="6"/>'
        '<line x1="8" y1="2" x2="8" y2="6"/>'
        '<line x1="3" y1="10" x2="21" y2="10"/>'
        '<path d="M8 14h.01"/>'
        '<path d="M12 14h.01"/>'
        '<path d="M16 14h.01"/>'
        '<path d="M8 18h.01"/>'
        '<path d="M12 18h.01"/>'
        '<path d="M16 18h.01"/>'
    ),
    "clock": (
        '<circle cx="12" cy="12" r="10"/>'
        '<polyline points="12 6 12 12 16 14"/>'
    ),
    "external-link": (
        '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>'
        '<polyline points="15 3 21 3 21 9"/>'
        '<line x1="10" y1="14" x2="21" y2="3"/>'
    ),
    "rotate-ccw": (
        '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>'
        '<path d="M3 3v5h5"/>'
    ),
    "chevron-down": (
        '<path d="m6 9 6 6 6-6"/>'
    ),
    "chevron-right": (
        '<path d="m9 18 6-6-6-6"/>'
    ),
    "zap": (
        '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>'
    ),
    "sparkles": (
        '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/>'
    ),
    "target": (
        '<circle cx="12" cy="12" r="10"/>'
        '<circle cx="12" cy="12" r="6"/>'
        '<circle cx="12" cy="12" r="2"/>'
    ),
    "arrow-right": (
        '<path d="M5 12h14"/>'
        '<path d="m12 5 7 7-7 7"/>'
    ),
    "shield-check": (
        '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/>'
        '<path d="m9 12 2 2 4-4"/>'
    ),
    "sliders": (
        '<line x1="4" y1="21" x2="4" y2="14"/>'
        '<line x1="4" y1="10" x2="4" y2="3"/>'
        '<line x1="12" y1="21" x2="12" y2="12"/>'
        '<line x1="12" y1="8" x2="12" y2="3"/>'
        '<line x1="20" y1="21" x2="20" y2="16"/>'
        '<line x1="20" y1="12" x2="20" y2="3"/>'
        '<line x1="1" y1="14" x2="7" y2="14"/>'
        '<line x1="9" y1="8" x2="15" y2="8"/>'
        '<line x1="17" y1="16" x2="23" y2="16"/>'
    ),
    "cpu": (
        '<rect width="16" height="16" x="4" y="4" rx="2"/>'
        '<rect width="6" height="6" x="9" y="9" rx="1"/>'
        '<path d="M15 2v2"/>'
        '<path d="M15 20v2"/>'
        '<path d="M2 15h2"/>'
        '<path d="M2 9h2"/>'
        '<path d="M20 15h2"/>'
        '<path d="M20 9h2"/>'
        '<path d="M9 2v2"/>'
        '<path d="M9 20v2"/>'
    ),
    "globe": (
        '<circle cx="12" cy="12" r="10"/>'
        '<path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/>'
        '<path d="M2 12h20"/>'
    ),
    "graduation-cap": (
        '<path d="M21.42 10.922a1 1 0 0 0-.019-.396l-8.5-4a1 1 0 0 0-.802 0l-8.5 4A1 1 0 0 0 3 11.5v5a1 1 0 0 0 2 0v-4.148l7 3.294 7-3.294V16.5a1 1 0 0 0 2 0v-5a1 1 0 0 0-.58-.578Z"/>'
        '<path d="M6 13.5V17c0 2 3 3 6 3s6-1 6-3v-3.5"/>'
    )
}

# Streamlit native Material icon mappings for st.button / st.page_link
MATERIAL_ICON_MAP = {
    "Dashboard": ":material/dashboard:",
    "Career Roadmap": ":material/route:",
    "Skill Gap Analysis": ":material/bar_chart:",
    "Resume Analyzer": ":material/find_in_page:",
    "Mock Interview": ":material/forum:",
    "Project Recommendations": ":material/business_center:",
    "Learning Resources": ":material/menu_book:",
    "Settings": ":material/settings:",
    "Generate": ":material/auto_awesome:",
    "Explore": ":material/explore:",
    "Download": ":material/download:",
    "Upload": ":material/upload_file:",
    "Reset": ":material/refresh:",
    "Submit": ":material/send:",
    "Next": ":material/arrow_forward:",
    "Search": ":material/search:",
    "Check": ":material/check_circle:",
    "Alert": ":material/warning:",
    "Target": ":material/track_changes:"
}


def get_lucide_svg(
    name: str,
    size: int = 20,
    color: str = "currentColor",
    stroke_width: float = 2.0,
    class_name: str = ""
) -> str:
    """
    Returns an inline SVG string for the requested Lucide icon.
    Falls back to 'zap' if the icon is not recognized.
    """
    path_data = LUCIDE_PATHS.get(name, LUCIDE_PATHS["zap"])
    cls_attr = f' class="{class_name}"' if class_name else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round"{cls_attr} style="vertical-align: middle; display: inline-block;">'
        f'{path_data}'
        f'</svg>'
    )


def get_material_icon(name: str) -> Optional[str]:
    """
    Returns the Streamlit :material/icon_name: string if available.
    """
    return MATERIAL_ICON_MAP.get(name, None)
