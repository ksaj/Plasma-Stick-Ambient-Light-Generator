# 🎨 Plasma Stick Color Palettes

Extended 10-color palettes for custom scenes.  
Each palette is a Python list of RGB tuples (0–255).  
Comments describe the intended mood or color name.

Use them by copying into your `main.py` and referencing with `_fade_palette`.

---

## 🌅 Sunset Warmth

    SUNSET_COLORS = [
        (255, 94, 19),    # Fiery orange
        (255, 147, 41),   # Golden amber
        (255, 196, 79),   # Soft peach
        (220, 90, 130),   # Rose pink
        (160, 45, 110),   # Wine red
        (100, 30, 80),    # Twilight plum
        (255, 120, 60),   # Burnt orange
        (255, 80, 50),    # Sunset red
        (200, 100, 150),  # Dusty mauve
        (240, 160, 90),   # Evening gold
    ]

---

## ❄️ Icy Blues

    ICY_COLORS = [
        (180, 220, 255),  # Pale sky blue
        (120, 200, 255),  # Frosty cyan
        (80, 160, 220),   # Glacier blue
        (60, 120, 180),   # Deep arctic
        (200, 240, 255),  # Ice shimmer white
        (100, 180, 240),  # Winter lake
        (160, 210, 255),  # Crisp frost
        (50, 100, 160),   # Cold twilight
        (140, 180, 220),  # Frozen cloud
        (220, 250, 255),  # Sparkling ice
    ]

---

## 🌹 Rose Garden

    ROSE_COLORS = [
        (255, 182, 193),  # Light rose pink
        (255, 105, 180),  # Hot pink
        (220, 20, 60),    # Crimson
        (199, 21, 133),   # Magenta rose
        (255, 240, 245),  # Lavender blush
        (255, 160, 180),  # Coral rose
        (210, 40, 100),   # Deep fuchsia
        (255, 200, 210),  # Pale pink
        (230, 120, 140),  # Garden bloom
        (180, 50, 80),    # Dark rose
    ]

---

## 🔥 Hearth & Ember

    HEARTH_COLORS = [
        (255, 140, 0),    # Fire orange
        (255, 69, 0),     # Hot ember red-orange
        (255, 215, 0),    # Warm gold
        (178, 34, 34),    # Deep ember red
        (139, 69, 19),    # Smoky brown
        (255, 120, 30),   # Bright flame
        (200, 80, 20),    # Charcoal glow
        (255, 170, 60),   # Ash gold
        (150, 40, 10),    # Burnt coal
        (255, 200, 90),   # Soft amber
    ]

---

## 🎉 Neon Party

    NEON_COLORS = [
        (255, 20, 147),   # Neon pink
        (0, 255, 255),    # Electric cyan
        (57, 255, 20),    # Acid green
        (138, 43, 226),   # Neon purple
        (255, 255, 0),    # Bright yellow
        (0, 128, 255),    # Laser blue
        (255, 0, 128),    # Shocking magenta
        (0, 255, 128),    # Lime neon
        (255, 64, 64),    # Hot red neon
        (200, 0, 255),    # Ultra violet
    ]

---

## 🍂 Autumn Glow

    AUTUMN_COLORS = [
        (255, 99, 71),    # Tomato red
        (255, 165, 0),    # Pumpkin orange
        (218, 112, 214),  # Orchid leaf
        (210, 105, 30),   # Burnt sienna
        (244, 164, 96),   # Autumn tan
        (178, 34, 34),    # Brick red
        (255, 140, 0),    # Harvest orange
        (205, 92, 92),    # Chestnut
        (222, 184, 135),  # Dry wheat
        (255, 215, 0),    # Harvest gold
    ]

---

## 🌊 Ocean Depths

    OCEAN_COLORS = [
        (0, 105, 148),    # Deep sea blue
        (0, 191, 255),    # Tropical cyan
        (25, 25, 112),    # Midnight navy
        (70, 130, 180),   # Steel blue surf
        (32, 178, 170),   # Teal wave
        (0, 128, 128),    # Dark teal
        (64, 224, 208),   # Turquoise
        (100, 149, 237),  # Cornflower blue
        (176, 224, 230),  # Powder aqua
        (95, 158, 160),   # Seafoam gray
    ]

---

💡 **Tip:**  
You can drop any of these into a scene using `_fade_palette`. For example:

    def scene_10(t_ms, B):
        _fade_palette(t_ms, B, SUNSET_COLORS, 40000)  # 40s per fade
