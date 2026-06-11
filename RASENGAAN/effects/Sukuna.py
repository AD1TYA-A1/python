import cv2
import numpy as np
import random
import math
import pygame

class SukunaSound:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self._charge_sound = self._make_charge()
        self._blast_sound  = self._make_blast()
        self._charge_ch    = pygame.mixer.Channel(4)
        self._blast_ch     = pygame.mixer.Channel(5)

    def _make_charge(self):
        sr = 44100; dur = 1.5; n = int(sr * dur)
        t  = np.linspace(0, dur, n)
        # deep ominous low hum + dark crackle
        s  = 0.4  * np.sin(2 * math.pi * 60  * t)
        s += 0.25 * np.sin(2 * math.pi * 120 * t)
        s += 0.15 * np.sin(2 * math.pi * 30  * t)
        # dark crackle bursts
        for _ in range(40):
            pos = random.randint(0, n - 400)
            blen = random.randint(80, 400)
            burst = np.random.uniform(-1, 1, blen).astype(np.float32)
            burst *= np.linspace(1, 0, blen)
            s[pos:pos+blen] += burst * 0.3
        s = np.clip(s, -1, 1).astype(np.float32)
        pcm = (s * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.column_stack([pcm, pcm]))

    def _make_blast(self):
        sr = 44100; dur = 1.8; n = int(sr * dur)
        t  = np.linspace(0, dur, n)
        # massive low boom
        boom  = np.sin(2 * math.pi * 45  * t) * np.exp(-t * 3)
        boom += np.sin(2 * math.pi * 25  * t) * np.exp(-t * 1.8)
        boom += np.sin(2 * math.pi * 90  * t) * np.exp(-t * 6)
        crack = np.random.uniform(-1, 1, n).astype(np.float32) * np.exp(-t * 18)
        # dark rumble tail
        rumble = np.random.uniform(-0.3, 0.3, n).astype(np.float32) * np.exp(-t * 4)
        s = np.clip(boom*0.8 + crack*0.5 + rumble*0.4, -1, 1).astype(np.float32)
        pcm = (s * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.column_stack([pcm, pcm]))

    def play_charge(self, vol):
        v = max(0.0, min(1.0, vol))
        if not self._charge_ch.get_busy():
            self._charge_ch.play(self._charge_sound, loops=-1)
        self._charge_ch.set_volume(v)

    def stop_charge(self):
        self._charge_ch.fadeout(350)

    def play_blast(self):
        self._blast_ch.play(self._blast_sound)

    def stop_all(self):
        self._charge_ch.stop()
        self._blast_ch.stop()


class CursedBlast:
    """Full-screen cursed energy explosion — deep red + black."""

    def __init__(self):
        self.active      = False
        self.frame_count = 0
        self.total       = 40
        self.origin      = (320, 240)
        self.particles   = []

    def trigger(self, origin):
        self.active      = True
        self.frame_count = 0
        self.origin      = origin
        self.particles   = []
        cx, cy = origin
        for _ in range(150):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(5, 22)
            self.particles.append({
                "x":  float(cx), "y": float(cy),
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": random.randint(15, 35), "max": 35,
                "r":    random.randint(3, 9),
                "color": random.choice([
                    (0, 0, 200),(0, 0, 160),(30, 0, 220),
                    (60, 0, 180),(0, 30, 255),(20, 20, 255),
                    (80, 0, 140),(100, 0, 100),
                ]),
            })

    def update(self, frame):
        if not self.active:
            return frame

        p    = self.frame_count / self.total
        h, w = frame.shape[:2]
        cx, cy = self.origin

        # ── phase 1 (0–0.25): dark implosion + red pulse ─────────────────
        if p < 0.25:
            darkness = 1.0 - (p / 0.25)
            overlay  = np.zeros_like(frame)
            cv2.addWeighted(overlay, darkness * 0.7, frame,
                            1 - darkness * 0.7, 0, frame)
            # pulsing red ring
            r_imp = int((1.0 - p / 0.25) * 120)
            ov2   = frame.copy()
            cv2.circle(ov2, (cx, cy), r_imp, (0, 0, 255), 4)
            cv2.circle(ov2, (cx, cy), max(1, r_imp-8), (0, 0, 180), 2)
            cv2.addWeighted(ov2, 0.7, frame, 0.3, 0, frame)

        # ── phase 2 (0.2–0.5): deep red FLASH ────────────────────────────
        if 0.18 < p < 0.48:
            intensity = 1.0 - abs(p - 0.33) / 0.15
            intensity = max(0, min(1, intensity))
            overlay   = np.zeros_like(frame)
            overlay[:, :, 2] = 200   # red channel only
            cv2.addWeighted(overlay, intensity * 0.88, frame,
                            1 - intensity * 0.88, 0, frame)

        # ── phase 3 (0.4–1.0): explosion outward ─────────────────────────
        if p > 0.4:
            prog = (p - 0.4) / 0.6

            # expanding shockwave rings — red/dark red
            for i in range(4):
                r = int(prog * w * 0.75 + i * 35)
                a = max(0, 1.0 - prog - i * 0.18)
                ov3 = frame.copy()
                red = 180 - i * 30
                cv2.circle(ov3, (cx, cy), r, (0, 0, red), 3 - min(i,2))
                cv2.addWeighted(ov3, a * 0.75, frame, 1 - a * 0.75, 0, frame)

            # cursed energy cracks radiating outward
            if prog < 0.7:
                for i in range(12):
                    base_a = (i / 12) * 2 * math.pi
                    jitter = random.uniform(-0.4, 0.4)
                    angle  = base_a + jitter
                    dist1  = random.randint(20, int(prog * 200 + 30))
                    dist2  = dist1 + random.randint(20, 60)
                    sx2    = int(cx + math.cos(angle) * dist1)
                    sy2    = int(cy + math.sin(angle) * dist1)
                    ex2    = int(cx + math.cos(angle + random.uniform(-0.3,0.3)) * dist2)
                    ey2    = int(cy + math.sin(angle + random.uniform(-0.3,0.3)) * dist2)
                    crack_bright = int(200 * (1 - prog))
                    cv2.line(frame, (sx2, sy2), (ex2, ey2),
                             (0, 0, crack_bright), 1)

            # particles
            pov = frame.copy()
            for pt in self.particles:
                if pt["life"] > 0:
                    ratio = pt["life"] / pt["max"]
                    r_draw = max(1, int(pt["r"] * ratio))
                    cv2.circle(pov, (int(pt["x"]), int(pt["y"])),
                               r_draw, pt["color"], -1)
            cv2.addWeighted(pov, 0.85, frame, 0.15, 0, frame)

            # dark smoke wisps
            if 0.4 < prog < 0.9:
                for _ in range(6):
                    smoke_x = cx + random.randint(-int(prog*150), int(prog*150))
                    smoke_y = cy + random.randint(-int(prog*150), int(prog*150))
                    smoke_r = random.randint(15, 45)
                    sov = frame.copy()
                    cv2.circle(sov, (smoke_x, smoke_y), smoke_r,
                               (0, 0, 0), -1)
                    cv2.addWeighted(sov, 0.15, frame, 0.85, 0, frame)

        # ── SUKUNA / CURSED ENERGY text ───────────────────────────────────
        if 0.3 < p < 0.68:
            ta = 1.0 - abs(p - 0.49) / 0.19
            ta = max(0, min(1, ta))
            to = frame.copy()
            cv2.putText(to, "CURSED TECHNIQUE!!",
                        (w//2 - 195, h//2 + 25),
                        cv2.FONT_HERSHEY_DUPLEX, 1.9,
                        (0, 0, 255), 3)
            cv2.addWeighted(to, ta * 0.92, frame, 1 - ta * 0.92, 0, frame)

        # age particles
        for pt in self.particles:
            pt["x"] += pt["vx"]; pt["y"] += pt["vy"]
            pt["vy"] += 0.25;    pt["vx"] *= 0.95
            pt["life"] -= 1

        self.frame_count += 1
        if self.frame_count >= self.total:
            self.active = False
        return frame


class SukunaEffect:
    """
    Sukuna cursed energy red ball.
    Gesture: thumb + index + middle fingers up (3-finger salute).
    Grows in palm, then fast movement = BLAST.
    """

    def __init__(self):
        self.intensity    = 0
        self.orb_radius   = 0.0
        self.frame_count  = 0
        self.particles    = []        # dark orbiting cursed energy wisps
        self.cracks       = []        # static crack lines on orb surface

        self._last_center  = None
        self._prev_center  = None
        self._throw_cd     = 0

        self.sound = SukunaSound()
        self.blast = CursedBlast()

    # ── public API ────────────────────────────────────────────────────────────

    def update(self, frame, gesture_detected, palm_center):
        h, w = frame.shape[:2]

        if self._throw_cd > 0:
            self._throw_cd -= 1

        # ── throw: fast hand movement while gesture held ───────────────────
        threw = False
        if gesture_detected and palm_center and self.intensity > 30 \
                and self._throw_cd == 0:
            threw = self._detect_throw(palm_center)
            if threw:
                self.blast.trigger(palm_center)
                self.sound.play_blast()
                self.sound.stop_charge()
                self.intensity  = 0
                self.orb_radius = 0
                self._throw_cd  = 55
                self.particles  = []
                self.cracks     = []

        if self.blast.active:
            frame = self.blast.update(frame)
            self._prev_center = palm_center
            return frame

        # ── charging ──────────────────────────────────────────────────────
        if gesture_detected and palm_center and not threw:
            self._ramp_up()
            self._last_center = palm_center
            self.orb_radius   = min(55.0, self.orb_radius + 1.2)

            self.sound.play_charge(self.intensity / 100.0 * 0.88)

            self._spawn_particles(palm_center)
            self._draw_dark_aura(frame, palm_center)
            self._draw_orb(frame, palm_center)
            self._draw_particles(frame)
            self._draw_hud(frame, w, h)

        else:
            self._ramp_down()
            self.orb_radius = max(0.0, self.orb_radius - 1.5)
            self.sound.play_charge(self.intensity / 100.0 * 0.4)
            if self.intensity <= 0:
                self.sound.stop_charge()
            if self.intensity > 5 and self._last_center:
                self._draw_orb(frame, self._last_center)
                self._draw_particles(frame)

        self._age_particles()
        self.frame_count  += 1
        self._prev_center  = palm_center
        return frame

    def cleanup(self):
        self.sound.stop_all()

    # ── throw detection ────────────────────────────────────────────────────────

    def _detect_throw(self, center):
        if self._prev_center is None:
            return False
        dx = center[0] - self._prev_center[0]
        dy = center[1] - self._prev_center[1]
        return math.sqrt(dx*dx + dy*dy) > 38

    # ── ramp ──────────────────────────────────────────────────────────────────

    def _ramp_up(self):
        self.intensity = min(100, self.intensity + 2)

    def _ramp_down(self):
        self.intensity = max(0, self.intensity - 4)

    # ── visuals ───────────────────────────────────────────────────────────────

    def _draw_dark_aura(self, frame, center):
        """Dark red / black cursed energy aura."""
        cx, cy  = center
        a       = self.intensity / 100.0
        overlay = frame.copy()

        for radius, op in [
            (int(110 + self.intensity * 0.6), 0.10),
            (int(75  + self.intensity * 0.4), 0.18),
            (int(45  + self.intensity * 0.2), 0.28),
        ]:
            # dark red — BGR = (0, 0, red)
            red = int(180 * op * a)
            cv2.circle(overlay, (cx, cy), radius, (0, 0, red), -1)

        # darken background slightly for cursed energy feel
        dark_ov = np.zeros_like(frame)
        cv2.circle(dark_ov, (cx, cy),
                   int(120 + self.intensity * 0.7), (1, 1, 1), -1)
        cv2.addWeighted(dark_ov, a * 0.3, frame, 1.0, 0, frame)

        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    def _draw_orb(self, frame, center):
        if self.orb_radius < 3:
            return
        cx, cy = center
        r      = int(self.orb_radius)
        pulse  = abs(math.sin(self.frame_count * 0.12)) * 0.15 + 0.85
        r      = int(r * pulse)

        # outer glow layers — dark red to bright red core
        layers = [
            (r + 12, (0,   0,  80), 2),
            (r +  6, (0,   0, 140), 3),
            (r,      (0,   0, 200), -1),
            (int(r * 0.70), (0,   0, 230), -1),
            (int(r * 0.45), (20,  0, 255), -1),
            (int(r * 0.25), (60, 20, 255), -1),
            (int(r * 0.10), (120,60, 255), -1),
        ]
        for radius, color, thickness in layers:
            if radius > 0:
                cv2.circle(frame, (cx, cy), radius, color, thickness)

        # rotating cursed energy cracks on surface
        self._draw_surface_cracks(frame, cx, cy, r)

    def _draw_surface_cracks(self, frame, cx, cy, r):
        """Dark glowing crack lines on orb surface."""
        if r < 8:
            return
        n_cracks = int(3 + self.intensity / 25)
        for i in range(n_cracks):
            base_angle = (i / n_cracks) * 2 * math.pi + self.frame_count * 0.03
            # crack goes from surface inward
            outer_x = int(cx + math.cos(base_angle) * r)
            outer_y = int(cy + math.sin(base_angle) * r)
            inner_x = int(cx + math.cos(base_angle + 0.3) * r * 0.5)
            inner_y = int(cy + math.sin(base_angle + 0.3) * r * 0.5)
            mid_x   = int(cx + math.cos(base_angle - 0.2) * r * 0.75)
            mid_y   = int(cy + math.sin(base_angle - 0.2) * r * 0.75)
            # dark crack
            cv2.line(frame, (outer_x, outer_y), (mid_x, mid_y),
                     (0, 0, 0), 2)
            cv2.line(frame, (mid_x, mid_y), (inner_x, inner_y),
                     (0, 0, 0), 1)
            # glow edge on crack
            cv2.line(frame, (outer_x, outer_y), (mid_x, mid_y),
                     (0, 0, 180), 1)

    def _spawn_particles(self, center):
        cx, cy = center
        r      = max(10, int(self.orb_radius))
        n      = int(self.intensity / 18) + 1

        for _ in range(n):
            angle = random.uniform(0, 2 * math.pi)
            orbit = r + random.randint(5, 25)
            self.particles.append({
                "angle":  angle,
                "orbit":  float(orbit),
                "speed":  random.uniform(0.06, 0.15),
                "cx":     float(cx), "cy": float(cy),
                "life":   random.randint(12, 28),
                "max":    28,
                "r":      random.randint(2, 5),
                "escape": random.random() < 0.2,
                "vx":     random.uniform(-1.5, 1.5),
                "vy":     random.uniform(-2.5, -0.5),
            })
        if len(self.particles) > 200:
            self.particles = self.particles[-200:]

    def _draw_particles(self, frame):
        for p in self.particles:
            ratio = p["life"] / p["max"]
            r     = max(1, int(p["r"] * ratio))
            if p["escape"]:
                age = p["max"] - p["life"]
                x   = int(p["cx"] + p["vx"] * age)
                y   = int(p["cy"] + p["vy"] * age)
            else:
                x = int(p["cx"] + math.cos(p["angle"]) * p["orbit"])
                y = int(p["cy"] + math.sin(p["angle"]) * p["orbit"] * 0.6)
            # dark red particles
            red   = int(180 * ratio + 40)
            color = (0, 0, red)
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

        cv2.rectangle(frame, (12, h-28), (12+bar_max, h-10), (10, 5, 20), -1)
        cv2.rectangle(frame, (12, h-28), (12+bar_max, h-10), (60, 0, 100), 1)

        red = int(100 + self.intensity * 1.5)
        if bar_w > 0:
            cv2.rectangle(frame, (12, h-28), (12+bar_w, h-10),
                          (0, 0, min(red, 255)), -1)

        label = "DOMAIN EXPANSION!!" if self.intensity >= 95 else "CURSED ENERGY"
        cv2.putText(frame, label, (12, h-34),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, min(red, 255)), 1)
        cv2.putText(frame, f"{int(self.intensity)}%", (w-55, h-34),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 220), 1)

        if self.intensity > 30:
            cv2.putText(frame, "MOVE FAST TO RELEASE!!",
                        (12, h-48),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 0, 200), 1)