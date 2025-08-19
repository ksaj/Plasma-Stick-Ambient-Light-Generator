# plasma_romance_scenes_1_to_7.py
# Multi‑scene ambient lighting for Pimoroni Plasma Stick 2040 W (MicroPython `plasma` API)
# API matches examples like fire.py: plasma.WS2812(NUM_LEDS, color_order=plasma.COLOR_ORDER_RGB)
#
# Controls
#   • BOOT/SEL short‑press  → next scene
#   • BOOT/SEL long‑press   → next brightness preset (>= 0.7 s)
#   • REPL (after stopping loop with Ctrl‑C): set_scene(n), next_scene(), set_brightness(i), next_brightness(), get_status(), run()
#
# Scenes
#   1) Candlelight Flicker + Embers   (warm, nuanced)
#   2) Sunset Drift Panorama          (brighter + dynamic + spatial gradient)
#   3) Heartbeat Glow                 (soft double thump)
#   4) Warm Hearth                    (per‑LED phase fades through warm palette)
#   5) Icy Forest                     (cool winter palette)
#   6) Rose Garden                    (romantic florals)
#   7) Neon Candy                     (playful/high‑energy palette)
#
# Notes
#   • Share GND between LED strip and the board. Keep brightness reasonable on USB power.
#   • Startup debug flash is included but DISABLED (call is commented out in run()). Uncomment when wiring/testing.
#
# License: Public Domain / Unlicense

import time, math, random
import plasma

# ---------------------- Configuration ----------------------
NUM_LEDS        = 50
BRIGHT_LEVELS   = [0.18, 0.30, 0.45]   # brightness presets (0..1)
BRIGHT_INDEX    = 1                    # start preset
SCENE_START     = 1                    # 1-based index
FPS             = 60
LONGPRESS_MS    = 700
COLOR_ORDER     = plasma.COLOR_ORDER_RGB

# Optional: if your firmware lacks a BOOT/SEL reader, set this to a GPIO fallback (active‑low to GND).
BUTTON_GPIO     = None   # e.g. 3 for GP3->GND; None to prefer BOOT/SEL reader

# ---------------------- Strip Setup ------------------------
led_strip = plasma.WS2812(NUM_LEDS, color_order=COLOR_ORDER)
led_strip.start()

# Onboard LED heartbeat (optional)
try:
    from machine import Pin
    _onboard = Pin('LED', Pin.OUT)
except Exception:
    Pin = None
    _onboard = None

# ---------------------- BOOT/SEL reader --------------------
def _noop_bootsel(): return False
read_bootsel = _noop_bootsel
_bootsel_available = False

# Try modern MicroPython
try:
    from machine import bootsel_button as _bootsel_button
    def read_bootsel():
        try: return bool(_bootsel_button())
        except Exception: return False
    _bootsel_available = True
except Exception:
    # Try rp2 variant
    try:
        from rp2 import bootsel_button as _rp2_bootsel_button
        def read_bootsel():
            try: return bool(_rp2_bootsel_button())
            except Exception: return False
        _bootsel_available = True
    except Exception:
        pass

# GPIO fallback (active‑low to GND)
_btn_pin = None
if BUTTON_GPIO is not None and Pin is not None:
    try:    _btn_pin = Pin(BUTTON_GPIO, Pin.IN, Pin.PULL_UP)
    except Exception: _btn_pin = None

def _read_button_fallback():
    if _btn_pin is None: return False
    try: return _btn_pin.value() == 0
    except Exception: return False

def read_button():
    """True while button is currently pressed."""
    if _bootsel_available: return read_bootsel()
    return _read_button_fallback()

# ---------------------- Helpers ----------------------------
def clamp(x, lo=0.0, hi=1.0):
    return lo if x < lo else hi if x > hi else x

def ease(t):
    # smootherstep 0..1
    return t*t*t*(t*(t*6 - 15) + 10)

def mix(a, b, t):
    return a + (b - a) * t

# ---------------------- REPL API / State -------------------
scene = SCENE_START
bright_idx = BRIGHT_INDEX

def _B(): return BRIGHT_LEVELS[bright_idx % len(BRIGHT_LEVELS)]

def set_scene(n):
    global scene
    n = int(n)
    if 1 <= n <= _scene_count():
        scene = n
        print("[multi] scene ->", scene)
    else:
        print("Scene must be 1..", _scene_count())

def next_scene(): set_scene(1 + (scene % _scene_count()))

def set_brightness(i):
    global bright_idx
    bright_idx = int(i) % len(BRIGHT_LEVELS)
    print("[multi] brightness -> idx", bright_idx, "value", _B())

def next_brightness(): set_brightness(bright_idx + 1)

def get_status():
    print({"scene": scene, "brightness": _B(), "bootsel_available": _bootsel_available, "button_gpio": BUTTON_GPIO, "scenes": _scene_names()})

# ---------------------- Debug Startup Flash ----------------
def _startup_flash(bright=0.35, dur_ms=600):
    """Debug helper: quick warm flash so you instantly know wiring is correct."""
    for i in range(NUM_LEDS):
        led_strip.set_hsv(i, 35/360, 0.35, bright)
    time.sleep_ms(dur_ms)
    for i in range(NUM_LEDS):
        led_strip.set_hsv(i, 0, 0, 0)

# ---------------------- Scenes 1–3 -------------------------
# 1) Candlelight (nuanced flicker + rare embers)
_flicker_phase = [random.random()*10.0 for _ in range(NUM_LEDS)]
def scene_1(t_ms, B):
    t = t_ms / 1000.0
    base_h = 30/360
    for i in range(NUM_LEDS):
        p = _flicker_phase[i]
        slow = 0.5 + 0.5*math.sin((t*0.9) + i*0.07 + p)
        fast = 0.5 + 0.5*math.sin((t*7.0) + i*0.31 + p*1.7)
        flicker = (slow*(1-0.35) + fast*0.35) * 0.35 + random.uniform(-0.02, 0.02)
        v = clamp(0.22 + flicker) * B
        h = (base_h + (0.011*math.sin(t*0.5 + i*0.05))) % 1.0
        s = clamp(0.75 + 0.1*math.sin(t*0.8 + i*0.19))
        if random.random() < 0.002:  # rare ember twinkle
            h, s, v = 0.95, 0.6, max(v, 0.35 * B)
        led_strip.set_hsv(i, h, s, v)

# 2) Sunset Drift (brighter + dynamic + spatial)
SUNSET_LOOP_MS  = 30_000
SUNSET_KEYS     = [
    (0.04, 0.40, 0.38),  # peach
    (0.10, 0.85, 0.55),  # amber
    (0.95, 0.60, 0.45),  # rose
    (0.98, 0.88, 0.28),  # wine
]
def scene_2(t_ms, B):
    ph = (t_ms % SUNSET_LOOP_MS) / SUNSET_LOOP_MS
    segs = len(SUNSET_KEYS)
    seg  = int(ph * segs) % segs
    seg2 = (seg + 1) % segs
    tt   = ease((ph * segs) % 1.0)
    h = mix(SUNSET_KEYS[seg][0], SUNSET_KEYS[seg2][0], tt) % 1.0
    s = mix(SUNSET_KEYS[seg][1], SUNSET_KEYS[seg2][1], tt)
    v = mix(SUNSET_KEYS[seg][2], SUNSET_KEYS[seg2][2], tt) * B
    for i in range(NUM_LEDS):
        k = i/(NUM_LEDS-1) if NUM_LEDS > 1 else 0.0
        hh = (h + 0.02*math.sin((k-0.5)*math.pi)) % 1.0
        vv = v * (0.88 + 0.12*math.cos(k*math.pi))
        vv *= 0.97 + 0.03*math.sin((t_ms/900.0) + i*0.11)
        led_strip.set_hsv(i, hh, s, clamp(vv))

# 3) Heartbeat Glow (double thump + decay)
HEART_BPM = 50
def scene_3(t_ms, B):
    beat_ms = 60_000 / HEART_BPM
    phase = t_ms % (beat_ms*2.5)
    def env(x_ms, w=180.0):
        x = x_ms / w
        return math.exp(-x*x*2.5)
    if phase < beat_ms*0.2:      a = env(phase - beat_ms*0.1)
    elif phase < beat_ms*1.0:    a = 0.0
    elif phase < beat_ms*1.2:    a = env(phase - beat_ms*1.1)
    else:                        a = 0.0
    base_h, base_s = 0.96, 0.85
    for i in range(NUM_LEDS):
        offset = (i / max(1, NUM_LEDS-1)) * 140.0
        v = clamp(0.07 + 0.35*a*math.exp(-offset/400.0)) * B
        h = (base_h + 0.003*math.sin((t_ms+offset)/1500.0)) % 1.0
        led_strip.set_hsv(i, h, base_s, v)

# ---------------------- Scenes 4–7 (palette fades) ---------
# Shared fade engine (per-LED phase offset)
def _fade_palette(t_ms, B, colors, fade_ms):
    """
    Smooth per-LED fade between colors in a list.
    colors: list of RGB tuples (0..255)
    fade_ms: milliseconds per transition (set small for debug, large for mood)
    """
    n = len(colors)
    if n < 1: return
    cycle_ms = max(1, n * fade_ms)

    for idx in range(NUM_LEDS):
        # Per-LED phase offset (gives gradient across strip)
        offset = (idx / max(1, NUM_LEDS - 1)) * fade_ms
        t = (t_ms + offset) % cycle_ms
        fade_pos = t / fade_ms            # 0..n
        i = int(fade_pos) % n
        j = (i + 1) % n
        f = fade_pos - int(fade_pos)      # 0..1 within this crossfade
        ff = ease(f)

        r1, g1, b1 = [c/255.0 for c in colors[i]]
        r2, g2, b2 = [c/255.0 for c in colors[j]]
        r = (r1 + (r2 - r1) * ff) * B
        g = (g1 + (g2 - g1) * ff) * B
        b = (b1 + (b2 - b1) * ff) * B

        led_strip.set_rgb(idx,
                          int(255 * clamp(r)),
                          int(255 * clamp(g)),
                          int(255 * clamp(b)))

# Scene 4: Warm Hearth
SCENE4_FADE_MS = 25000
SCENE4_COLORS = [
    (255, 180, 120), (255, 140, 60), (220, 80, 30), (255, 200, 100),
    (255, 100, 80), (200, 60, 20), (255, 160, 70), (180, 50, 30),
    (255, 120, 90), (255, 200, 140),
]
def scene_4(t_ms, B):
    _fade_palette(t_ms, B, SCENE4_COLORS, SCENE4_FADE_MS)

# Scene 5: Icy Forest
SCENE5_FADE_MS = 30000
SCENE5_COLORS = [
    (180, 220, 255), (140, 200, 255), (100, 180, 240), (80, 160, 200),
    (160, 220, 255), (120, 180, 220), (60, 140, 200), (200, 240, 255),
    (140, 220, 240), (100, 160, 220),
]
def scene_5(t_ms, B):
    _fade_palette(t_ms, B, SCENE5_COLORS, SCENE5_FADE_MS)

# Scene 6: Rose Garden
SCENE6_FADE_MS = 28000
SCENE6_COLORS = [
    (255, 180, 200), (255, 120, 160), (220, 80, 120), (255, 100, 140),
    (255, 160, 190), (180, 60, 90), (255, 200, 210), (220, 140, 160),
    (255, 120, 150), (200, 80, 110),
]
def scene_6(t_ms, B):
    _fade_palette(t_ms, B, SCENE6_COLORS, SCENE6_FADE_MS)

# Scene 7: Neon Candy
SCENE7_FADE_MS = 20000
SCENE7_COLORS = [
    (255, 60, 180), (80, 220, 255), (255, 255, 120), (180, 100, 255),
    (255, 100, 100), (100, 255, 180), (255, 180, 60), (120, 120, 255),
    (255, 80, 220), (140, 255, 140),
]
def scene_7(t_ms, B):
    _fade_palette(t_ms, B, SCENE7_COLORS, SCENE7_FADE_MS)

# ---------------------- Auto‑discovery ---------------------
def _scene_funcs():
    # find globals named 'scene_<number>' and return sorted list of callables
    items = []
    for name, fn in globals().items():
        if not name.startswith('scene_'): continue
        try:
            idx = int(name.split('_', 1)[1])
        except Exception:
            continue
        if callable(fn):
            items.append((idx, fn))
    items.sort(key=lambda x: x[0])
    return [fn for _, fn in items]

def _scene_count(): return len(_scene_funcs())
def _scene_names(): return ["scene_{}".format(i+1) for i in range(_scene_count())]

# ---------------------- Runtime ----------------------------
def _heartbeat(now_ms):
    if _onboard:
        try: _onboard.value((now_ms // 500) % 2)
        except Exception: pass

def _poll_button(now_ms, state):
    pressed = read_button()
    if pressed and not state["down"]:
        state["down"] = True
        state["t0"] = now_ms
    elif not pressed and state["down"]:
        dt = time.ticks_diff(now_ms, state["t0"] or now_ms)
        state["down"] = False
        return "long" if dt >= LONGPRESS_MS else "short"
    return None

def _print_ready():
    print("[multi] ready. bootsel_available:", bool(_bootsel_available), "button_gpio:", BUTTON_GPIO)
    get_status()
    print("[multi] discovered scenes:", _scene_names())

_state = {"down": False, "t0": None}

def run():
    global scene
    # _startup_flash()   # ← enable for quick wiring/debug feedback
    _print_ready()
    funcs = _scene_funcs()
    if not funcs:
        print("[multi] ERROR: No scene_* functions found."); return
    if scene < 1 or scene > len(funcs): scene = 1
    while True:
        now = time.ticks_ms()
        B = _B()
        funcs = _scene_funcs()  # allows hot‑adding scenes during dev
        funcs[(scene-1) % len(funcs)](now, B)
        ev = _poll_button(now, _state)
        if ev == "short": next_scene()
        elif ev == "long": next_brightness()
        _heartbeat(now)
        if FPS > 0:
            elapsed = time.ticks_diff(time.ticks_ms(), now)
            delay = max(0, int(1000/FPS) - elapsed)
            if delay: time.sleep_ms(delay)

# Auto‑run
try:
    run()
except KeyboardInterrupt:
    # Clear LEDs on Ctrl‑C
    for i in range(NUM_LEDS):
        led_strip.set_hsv(i, 0, 0, 0)
    print("\n[multi] stopped.")
