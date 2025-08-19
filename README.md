# Plasma Stick 2040 W – Multi-Scene Romance Lights

**Author:** (shared publicly, consider thanking KarstenJohansson@gmail.com if you use this!)  
**License:** Public Domain / Unlicense  
**Hardware:** Pimoroni Plasma Stick 2040 W (or RP2040 board with WS2812/NeoPixel strip and MicroPython)

---

## 📖 Overview
This project transforms your Plasma Stick into a multi-scene ambient light generator.  
It’s designed for romantic, cozy, or atmospheric moods – ranging from candlelight flickers to icy forests to neon party vibes.

The code is **PUBLIC DOMAIN**. You are free to copy, modify, and share it however you like.  
If you do use it, I would appreciate a thank you — not for the code itself, but for the thought and care that went into creating it and making it available to others.

---

## 🛠 Installation (Choose the uf2 file for your Plasma device model)
1. Install plasma_stick_2040_w-v1.0.0-micropython-with-filesystem.uf2 from https://github.com/pimoroni/plasma/releases/tag/v1.0.0.
2. Copy the file `main.py` to the Plasma file system using device instructions.
3. Safely eject/unmount and press reset. The program auto-runs at power-on (no REPL needed).

---

## 🎛 Controls
- **BOOT/SEL button**
  - Short press → next scene
  - Long press  → next brightness preset (default levels: 18%, 30%, 45%)
- **REPL (after stopping with Ctrl‑C)**
  - `set_scene(n)` → jump to scene *n*
  - `next_scene()` → advance to next scene
  - `set_brightness(i)` → set brightness preset index
  - `next_brightness()` → advance brightness
  - `get_status()` → print current status
  - `run()` → start the main loop again
- **Onboard LED** blinks once per second as a heartbeat.

---

## 🌈 Scenes
1. **Candlelight Flicker + Embers** – warm golden/orange tones with subtle flicker and occasional embers.  
2. **Sunset Drift Panorama** – peach → amber → rose → wine with smooth spatial gradients.  
3. **Heartbeat Glow** – soft double‑thump pulse in romantic reds.  
4. **Warm Hearth** – per‑LED phase fades through ambers/embers/golds (very slow).  
5. **Icy Forest** – wintery blues/teals/aquas.  
6. **Rose Garden** – pinks and deep roses, floral and gentle.  
7. **Neon Candy** – playful neon pink/cyan/purple/lime (higher energy).

---

## 💡 Tips
- **Power:** USB has limited current. Keep brightness modest for long strips; for high brightness use a separate 5 V supply and share GND.
- **Debug flash:** A startup “debug flash” helper exists but is disabled by default. If you want instant wiring confirmation, uncomment the `_startup_flash()` call inside `run()`.

---

## ➕ Custom Scenes
You can add as many scenes as you like. The program auto‑discovers any function named exactly `scene_<number>` and cycles them via BOOT/SEL.

- Each scene must be defined as:

        def scene_<number>(t_ms, B):
            # t_ms: current time in ms (from time.ticks_ms())
            # B: global brightness scalar 0..1
            # Example body: use led_strip.set_hsv(i, h, s, v) or led_strip.set_rgb(i, r, g, b)
            ...

- `<number>` must always be an **integer**. You can go beyond single digits:
  - ✅ Valid: `scene_8`, `scene_9`, `scene_10`, `scene_11`, …
  - ❌ Invalid: `scene_a`, `scene_flames`, `scene_red` (will be ignored)

- After you add a new scene function, BOOT/SEL will include it in the cycle automatically.

### Example – Adding Scene 10
Define a palette and fade time, then implement `scene_10` using the shared `_fade_palette` helper:

    SCENE10_COLORS = [
        (255, 255, 200), (200, 255, 240), (180, 220, 255),
        (255, 200, 255), (255, 180, 220),
        (240, 220, 180), (200, 180, 255),
        (180, 255, 220), (220, 255, 200), (255, 240, 220),
    ]
    SCENE10_FADE_MS = 30000

    def scene_10(t_ms, B):
        _fade_palette(t_ms, B, SCENE10_COLORS, SCENE10_FADE_MS)

---

## ⚖️ License
This project is released into the **Public Domain** under the Unlicense.  
Do whatever you like with it.

If you find it useful, please consider adding a note of thanks to the author for the effort of building and sharing this project with the public.

---

✨ Enjoy your new ambient light show!
