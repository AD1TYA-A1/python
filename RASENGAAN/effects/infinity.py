import cv2
import numpy as np
import math
import random
import pygame


# ══════════════════════════════════════════════════════════════════════════════
#  SOUND
# ══════════════════════════════════════════════════════════════════════════════
class InfinitySound:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self._hum_sound   = self._make_hum()
        self._blast_sound = self._make_blast()
        self._hum_ch   = pygame.mixer.Channel(6)
        self._blast_ch = pygame.mixer.Channel(7)

    def _make_hum(self):
        sr = 44100; dur = 1.5; n = int(sr * dur)
        t  = np.linspace(0, dur, n)
        # deep resonant blue hum — low sine + harmonic overtones
        s  = 0.35 * np.sin(2 * math.pi * 90  * t)
        s += 0.20 * np.sin(2 * math.pi * 180 * t)
        s += 0.12 * np.sin(2 * math.pi * 270 * t)
        s += 0.08 * np.sin(2 * math.pi * 45  * t)
        # ethereal shimmer
        s += np.random.uniform(-0.04, 0.04, n).astype(np.float32)
        s  = np.clip(s, -1, 1).astype(np.float32)
        pcm = (s * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.column_stack([pcm, pcm]))

    def _make_blast(self):
        sr = 44100; dur = 2.0; n = int(sr * dur)
        t  = np.linspace(0, dur, n)
        # massive blue energy release — rising then dissolving
        boom  = np.sin(2 * math.pi * 100 * t) * np.exp(-t * 2.5)
        boom += np.sin(2 * math.pi * 200 * t) * np.exp(-t * 4)
        boom += np.sin(2 * math.pi * 50  * t) * np.exp(-t * 1.5)
        crack = np.random.uniform(-1, 1, n).astype(np.float32) * np.exp(-t * 15)
        tail  = np.random.uniform(-0.2, 0.2, n).astype(np.float32) * np.exp(-t * 3)
        s = np.clip(boom * 0.8 + crack * 0.4 + tail * 0.3, -1, 1).astype(np.float32)
        pcm = (s * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.column_stack([pcm, pcm]))

    def play_hum(self, vol):
        v = max(0.0, min(1.0, vol))
        if not self._hum_ch.get_busy():
            self._hum_ch.play(self._hum_sound, loops=-1)
        self._hum_ch.set_volume(v)

    def stop_hum(self):
        self._hum_ch.fadeout(400)

    def play_blast(self):
        self._blast_ch.play(self._blast_sound)

    def stop_all(self):
        self._hum_ch.stop()
        self._blast_ch.stop()


# ══════════════════════════════════════════════════════════════════════════════
#  BLUE BLAST (Gojo's "Blue" / Hollow Purple explosion)
# ══════════════════════════════════════════════════════════════════════════════
class BlueBlast:
    def __init__(self):
        self.active      = False
        self.frame_count = 0
        self.total       = 45
        self.origin      = (320, 240)
        self.particles   = []

    def trigger(self, origin):
        self.active      = True
        self.frame_count = 0
        self.origin      = origin
        self.particles   = []
        cx, cy = origin
        for _ in range(120):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(4, 26)
            self.particles.append({
                "x": float(cx), "y": float(cy),
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": random.randint(12, 42), "max": 42,
                "r":    random.randint(2, 6),
                "color": random.choice([
                    (255, 255, 255), (220, 240, 255),
                    (180, 220, 255), (120, 190, 255),
                    (60,  150, 255), (20,  100, 255),
                ]),
            })

    def update(self, frame):
        if not self.active:
            return frame

        p    = self.frame_count / self.total
        h, w = frame.shape[:2]
        cx, cy = self.origin

        # ── blue-tint entire frame ────────────────────────────────────────
        tint = frame.copy()
        tint[:, :, 0] = np.clip(tint[:, :, 0].astype(np.int16) + int(60*(1-p)), 0, 255)
        cv2.addWeighted(tint, 0.3*(1-p), frame, 1-0.3*(1-p), 0, frame)

        # ── phase 1 (0–0.3): imploding pull-in rings ─────────────────────
        if p < 0.3:
            flash = 1.0 - (p / 0.3)
            ov = np.full_like(frame, (200, 220, 255))
            cv2.addWeighted(ov, flash * 0.75, frame, 1 - flash * 0.75, 0, frame)
            for i in range(5):
                r = int((1.0 - p/0.3) * (50 + i * 40))
                ov2 = frame.copy()
                cv2.circle(ov2, (cx, cy), r, (100 + i*25, 180 + i*12, 255), 2 + i)
                cv2.addWeighted(ov2, (1.0 - i*0.15)*0.6, frame,
                                1-(1.0-i*0.15)*0.6, 0, frame)

        # ── phase 2 (0.25–0.55): WHITE FLASH ─────────────────────────────
        if 0.22 < p < 0.52:
            intensity = 1.0 - abs(p - 0.37) / 0.15
            intensity = max(0, min(1, intensity))
            ov = np.full_like(frame, (220, 235, 255))
            cv2.addWeighted(ov, intensity * 0.92, frame,
                            1 - intensity * 0.92, 0, frame)

        # ── phase 3 (0.45–1.0): explosion outward ────────────────────────
        if p > 0.42:
            # shockwave rings
            for i in range(4):
                r = int((p - 0.42) / 0.58 * w * 0.75 + i * 35)
                a = max(0, 1.0 - (p - 0.42)/0.58 - i * 0.18)
                ov3 = frame.copy()
                cv2.circle(ov3, (cx, cy), r,
                           (200 - i*30, 220 - i*20, 255), 3)
                cv2.addWeighted(ov3, a * 0.65, frame, 1 - a * 0.65, 0, frame)

            # particles
            part_ov = frame.copy()
            for pt in self.particles:
                if pt["life"] > 0:
                    ratio = pt["life"] / pt["max"]
                    cv2.circle(part_ov, (int(pt["x"]), int(pt["y"])),
                               int(pt["r"] * ratio), pt["color"], -1)
            cv2.addWeighted(part_ov, 0.85, frame, 0.15, 0, frame)

            # blue streak lines
            if p < 0.82:
                for i in range(14):
                    angle  = (i / 14) * 2 * math.pi + p * 4
                    length = (p - 0.42) / 0.38 * min(w, h) * 0.65
                    ex = int(cx + math.cos(angle) * length)
                    ey = int(cy + math.sin(angle) * length)
                    bright = int(255 * (1.0 - (p - 0.42) / 0.38))
                    cv2.line(frame, (cx, cy), (ex, ey),
                             (bright, int(bright*0.9), 255), 1)

        # ── "BLUE!!" text ─────────────────────────────────────────────────
        if 0.28 < p < 0.72:
            ta = 1.0 - abs(p - 0.50) / 0.22
            ta = max(0, min(1, ta))
            if ta > 0.05:
                to = frame.copy()
                cv2.putText(to, "BLUE!!",
                            (w//2 - 130, h//2 + 25),
                            cv2.FONT_HERSHEY_DUPLEX, 2.8,
                            (20, 60, 160), 10)
                cv2.putText(to, "BLUE!!",
                            (w//2 - 130, h//2 + 25),
                            cv2.FONT_HERSHEY_DUPLEX, 2.8,
                            (200, 230, 255), 3)
                cv2.addWeighted(to, ta * 0.95, frame, 1 - ta * 0.95, 0, frame)

        # age particles
        for pt in self.particles:
            pt["x"] += pt["vx"]; pt["y"] += pt["vy"]
            pt["vy"] += 0.18;    pt["vx"] *= 0.97
            pt["life"] -= 1

        self.frame_count += 1
        if self.frame_count >= self.total:
            self.active = False
        return frame


# ══════════════════════════════════════════════════════════════════════════════
#  INFINITY EFFECT  (Gojo's Blue / Infinity ability)
# ══════════════════════════════════════════════════════════════════════════════
class InfinityEffect:
    """
    Gesture : OPEN PALM facing camera (all 5 fingers extended, palm forward).
    Charge  : hold open palm → blue orb grows + infinity rings spin.
    Blast   : drop hand / close fingers → Blue explosion.
    """

    def __init__(self):
        self.intensity    = 0.0
        self.orb_scale    = 0.0
        self.spin_angle   = 0.0
        self.particles    = []
        self.frame_count  = 0
        self._last_center = None
        self._was_palm    = False
        self._throw_cd    = 0

        self.sound = InfinitySound()
        self.blast = BlueBlast()

    # ── public API ────────────────────────────────────────────────────────────
    def update(self, frame, palm_open, palm_center):
        h, w = frame.shape[:2]

        if self._throw_cd > 0:
            self._throw_cd -= 1

        # ── blast trigger: palm was open, now closed/gone ─────────────────
        palm_just_closed = self._was_palm and not palm_open
        if palm_just_closed and self.intensity > 25 and self._throw_cd == 0:
            origin = self._last_center or (w//2, h//2)
            self.blast.trigger(origin)
            self.sound.play_blast()
            self.sound.stop_hum()
            self.intensity   = 0
            self._throw_cd   = 45
            self.particles   = []

        if self.blast.active:
            frame = self.blast.update(frame)
            self._was_palm = palm_open
            return frame

        if palm_open and palm_center:
            self._ramp_up()
            self._last_center = palm_center
            self.orb_scale    = min(1.0, self.orb_scale + 0.04)

            self.sound.play_hum(self.intensity / 100.0 * 0.85)

            self._spawn_particles(palm_center)
            self._draw_aura(frame, palm_center)
            self._draw_orb(frame, palm_center)
            self._draw_infinity_rings(frame, palm_center)
            self._draw_particles(frame)
            self._draw_hud(frame, w, h)

        else:
            self._ramp_down()
            self.orb_scale = max(0.0, self.orb_scale - 0.05)
            self.sound.play_hum(self.intensity / 100.0 * 0.4)
            if self.intensity <= 0:
                self.sound.stop_hum()
            if self.intensity > 5 and self._last_center:
                self._draw_orb(frame, self._last_center)
                self._draw_particles(frame)
            self.particles = [p for p in self.particles if p["life"] > 0]

        self._age_particles()
        self.spin_angle  += 0.06 + self.intensity * 0.0018
        self.frame_count += 1
        self._was_palm    = palm_open
        return frame

    def cleanup(self):
        self.sound.stop_all()

    # ── ramp ──────────────────────────────────────────────────────────────────
    def _ramp_up(self):
        self.intensity = min(100, self.intensity + 2.2)

    def _ramp_down(self):
        self.intensity = max(0, self.intensity - 3.5)

    # ── aura ──────────────────────────────────────────────────────────────────
    def _draw_aura(self, frame, center):
        cx, cy = center
        a = self.intensity / 100.0
        ov = frame.copy()
        for radius, op in [
            (int(130 + self.intensity * 0.7), 0.06),
            (int(90  + self.intensity * 0.5), 0.12),
            (int(55  + self.intensity * 0.3), 0.20),
        ]:
            col = (int(255*op*a), int(220*op*a), int(100*op*a))  # blue-white glow
            cv2.circle(ov, (cx, cy), max(1, radius), col, -1)
        cv2.addWeighted(ov, 0.55, frame, 0.45, 0, frame)

        # draw gravitational pull streaks (every other frame)
        if self.intensity > 20 and self.frame_count % 2 == 0:
            wov = frame.copy()
            base_r = int(75 + self.intensity * 0.45)
            for i in range(10):
                ang = (i / 10) * 2 * math.pi + self.spin_angle * 0.4
                sx  = cx + int(base_r * math.cos(ang))
                sy  = cy + int(base_r * 0.6 * math.sin(ang))
                cv2.line(wov, (sx, sy), (cx, cy), (255, 200, 80), 1)
            cv2.addWeighted(wov, 0.20 * a, frame, 1 - 0.20 * a, 0, frame)

    # ── orb ───────────────────────────────────────────────────────────────────
    def _draw_orb(self, frame, center):
        if self.orb_scale < 0.05:
            return
        cx, cy  = center
        base_r  = int(30 * self.orb_scale + self.intensity * 0.20)
        pulse   = abs(math.sin(self.frame_count * 0.14)) * 0.10 + 0.90
        r       = int(base_r * pulse)

        # layers: outer dark blue → mid blue → light → white core
        layers = [
            (r + 10, (15,  80, 220), 2),
            (r +  5, (40, 130, 255), 3),
            (r,      (100, 180, 255), -1),
            (int(r*0.65), (180, 220, 255), -1),
            (int(r*0.30), (230, 245, 255), -1),
            (int(r*0.12), (255, 255, 255), -1),
        ]
        for radius, color, thickness in layers:
            if radius > 0:
                cv2.circle(frame, (cx, cy), radius, color, thickness)

    # ── infinity rings ────────────────────────────────────────────────────────
    def _draw_infinity_rings(self, frame, center):
        """
        Three rotating elliptical rings — like Gojo's Infinity sphere.
        Each ring tilted at a different angle for the spherical look.
        """
        cx, cy  = center
        base_r  = int(32 + self.intensity * 0.22)
        a       = min(self.intensity / 100.0, 1.0)
        ov      = frame.copy()

        for i, (tilt_deg, speed_mult) in enumerate([(0, 1.0), (60, -0.8), (120, 1.2)]):
            angle_offset = self.spin_angle * speed_mult + math.radians(tilt_deg)
            ring_r       = base_r + i * 9
            pts          = []
            for deg in range(0, 360, 7):
                rad = math.radians(deg) + angle_offset
                x   = cx + int(ring_r * math.cos(rad))
                y   = cy + int(ring_r * 0.42 * math.sin(rad))
                pts.append((x, y))

            brightness = 160 + i * 28
            color      = (int(brightness*0.6), int(brightness*0.85), brightness)

            for j in range(0, len(pts), 2):   # dashed
                p1 = pts[j]
                p2 = pts[(j+1) % len(pts)]
                cv2.line(ov, p1, p2, color, 2)

        cv2.addWeighted(ov, min(a, 0.92), frame, 1 - min(a, 0.92), 0, frame)

    # ── particles ─────────────────────────────────────────────────────────────
    def _spawn_particles(self, center):
        cx, cy  = center
        n       = int(self.intensity / 28) + 1
        base_r  = int(32 + self.intensity * 0.22)
        for _ in range(n):
            angle = random.uniform(0, 2 * math.pi)
            orbit = base_r + random.randint(-8, 18)
            self.particles.append({
                "angle": angle,
                "orbit": orbit,
                "speed": random.uniform(0.07, 0.16),
                "cx": float(cx), "cy": float(cy),
                "life": random.randint(10, 22), "max": 22,
                "r":   random.randint(2, 4),
                "escape": random.random() < 0.2,
                "vx": random.uniform(-2, 2) if random.random() < 0.2 else 0,
                "vy": random.uniform(-3, -1) if random.random() < 0.2 else 0,
            })
        if len(self.particles) > 90:
            self.particles = self.particles[-90:]

    def _draw_particles(self, frame):
        for p in self.particles:
            ratio = p["life"] / p["max"]
            r     = max(1, int(p["r"] * ratio))
            if p["escape"]:
                x = int(p["cx"] + p["vx"] * (p["max"] - p["life"]))
                y = int(p["cy"] + p["vy"] * (p["max"] - p["life"]))
            else:
                x = int(p["cx"] + math.cos(p["angle"]) * p["orbit"])
                y = int(p["cy"] + math.sin(p["angle"]) * p["orbit"] * 0.5)
            bright = int(180 + 75 * ratio)
            color  = (int(bright * 0.6), int(bright * 0.85), bright)
            cv2.circle(frame, (x, y), r, color, -1)

    def _age_particles(self):
        for p in self.particles:
            p["angle"] += p["speed"]
            p["life"]  -= 1
        self.particles = [p for p in self.particles if p["life"] > 0]

    # ── HUD ───────────────────────────────────────────────────────────────────
    def _draw_hud(self, frame, w, h):
        bar_max = int(w * 0.28)
        bar_w   = int(bar_max * (self.intensity / 100))
        bx = w // 2 + int(w * 0.15)
        by = h - 50

        cv2.rectangle(frame, (bx, by), (bx+bar_max, by+14), (5, 10, 30),  -1)
        cv2.rectangle(frame, (bx, by), (bx+bar_max, by+14), (20, 60, 160),  1)

        blue = int(180 + self.intensity * 0.75)
        if bar_w > 0:
            cv2.rectangle(frame, (bx, by), (bx+bar_w, by+14),
                          (int(60+self.intensity*0.6), int(140+self.intensity*0.5), blue), -1)

        label = "💠 MAX — CLOSE HAND TO BLAST!" if self.intensity >= 95 else "💠 INFINITY"
        cv2.putText(frame, label, (bx, by - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, (120, 200, 255), 1)
        cv2.putText(frame, f"{int(self.intensity)}%",
                    (bx + bar_max + 4, by + 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.38, (100, 180, 255), 1)
        if 20 < self.intensity < 95:
            cv2.putText(frame, "Hold open palm... then CLOSE FIST!",
                        (bx, by - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.38, (80, 160, 255), 1)