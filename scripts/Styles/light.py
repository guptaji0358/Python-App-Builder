# A clean, bright, fully opaque light theme.

PALETTE = {
    "WindowBg": "rgba(245,247,250,255)",
    "Text": "#111318",
    "SubText": "rgba(17,19,24,160)",
    "CardBg": "rgba(0,0,0,6)",
    "CardBorder": "rgba(0,0,0,25)",
    "DialogBg": "rgba(255,255,255,250)",
    "InputBg": "rgba(0,120,220,16)",
    "InputHoverBg": "rgba(0,120,220,16)",
    "InputFocusBg": "rgba(0,120,220,35)",
    "InputDisabledBg": "rgba(0,0,0,15)",
    "InputDisabledText": "rgba(17,19,24,120)",
    "InputDisabledBorder": "rgba(0,0,0,25)",
    "ComboBg": "rgba(255,255,255,220)",
    "ComboBorder": "rgba(0,0,0,30)",
    "SecondaryBg": "rgba(0,0,0,7)",
    "SecondaryHoverBg": "rgba(0,0,0,12)",
    "SecondaryPressedBg": "rgba(0,0,0,18)",
    "SecondaryDisabledBg": "rgba(0,0,0,4)",
    "SecondaryDisabledText": "rgba(17,19,24,90)",
    "SecondaryDisabledBorder": "rgba(0,0,0,15)",
    "ScrollTrack": "#E3E6EB",
    "ScrollHandle": "rgba(0,0,0,35)",
    "TextEditBg": "rgba(0,0,0,10)",
    "AssetCardBg": "rgba(0,0,0,5)",
    "AssetCardBorder": "rgba(0,0,0,30)",

    "WindowOpacity": 1.0,
    # White check/radio glyphs and low-alpha accent fills were tuned for a
    # dark background and vanish here - Style.ApplyTheme swaps to the
    # dark-glyph icon variants and boosts accent alpha when IsLight is True.
    "IsLight": True,
    "AccentAlpha": 235,
    "AccentHoverAlpha": 235,
    "AccentPressedAlpha": 255,
}
