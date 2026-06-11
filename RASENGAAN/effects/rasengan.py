import cv2
import numpy as np
import random
import math
import pygame

class RasenganSound:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self._spin_sound  = self._make_spin()
        self._blast_sound = self._make_blast()
        self._spin_ch  = pygame.mixer.Channel(2)
        self._blast_ch = pygame.mixer.Channel(3)

    def _make_spin(self):
        sr = 44100; dur = 1.2; n = int(sr * dur)
        t  = np.linspace(0, dur, n)
        # rising whirling wind tone
        freq = 200 + 180 * t / dur
        s = 0.35 * np.sin(2 * math.pi * freq * t)
        s += 0.2  * np.sin(2 * math.pi * freq * 2 * t)
        s += np.random.uniform(-0.08, 0.08, n).astype(np.float32)
        s  = np.clip(s, -1, 1).astype(np.float32)
        pcm = (s * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.column_stack([pcm, pcm]))

    def _make_blast(self):
        sr = 44100; dur = 1.5; n = int(sr * dur)
        t  = np.linspace(0, dur, n)
        boom  = np.sin(2 * math.pi * 80  * t) * np.exp(-t * 4)
        boom += np.sin(2 * math.pi * 40  * t) * np.exp(-t * 2.5)
        boom += np.sin(2 * math.pi * 160 * t) * np.exp(-t * 8)
        crack = np.random.uniform(-1, 1, n).astype(np.float32) * np.exp(-t * 20)
        s = np.clip(boom * 0.75 + crack * 0.45, -1, 1).astype(np.float32)
        pcm = (s * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.column_stack([pcm, pcm]))

    def play_spin(self, vol):
        v = max(0.0, min(1.0, vol))
        if not self._spin_ch.get_busy():
            self._spin_ch.play(self._spin_sound, loops=-1)
        self._spin_ch.set_volume(v)

    def stop_spin(self):
        self._spin_ch.fadeout(400)

    def play_blast(self):
        self._blast_ch.play(self._blast_sound)

    def stop_all(self):
        self._spin_ch.stop()
        self._blast_ch.stop()


class RasenganBlast:
    """Full-screen Rasengan explosion — blue-white spiral implosion then BOOM."""

    def __init__(self):
        self.active      = False
        self.frame_count = 0
        self.total       = 35
        self.origin      = (320, 240)
        self.particles   = []

    def trigger(self, origin):
        self.active      = True
        self.frame_count = 0
        self.origin      = origin
        self.particles   = []
        cx, cy = origin
        for _ in range(100):  # reduced from 200
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 24)
            self.particles.append({
                "x": float(cx), "y": float(cy),
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": random.randint(10, 38),
                "max":  38,
                "r":    random.randint(2, 7),
                "color": random.choice([
                    (255,255,255),(220,240,255),(180,220,255),
                    (120,200,255),(70,170,255),(30,130,230),(0,90,200),
                ]),
            })

    def update(self, frame):
        if not self.active:
            return frame

        p    = self.frame_count / self.total
        h, w = frame.shape[:2]
        cx, cy = self.origin

        # blue tint the whole frame during blast
        tint_ov = frame.copy()
        tint_ov[:,:,0] = np.clip(tint_ov[:,:,0].astype(np.int16) + int(30*(1-p)), 0, 255)
        cv2.addWeighted(tint_ov, 0.25*(1-p), frame, 1-0.25*(1-p), 0, frame)

        # ── phase 1 (0–0.3): implosion ────────────────────────────────────
        if p < 0.3:
            flash = 1.0 - (p / 0.3)
            overlay = np.full_like(frame, (180, 220, 255))
            cv2.addWeighted(overlay, flash * 0.85, frame, 1 - flash * 0.85, 0, frame)
            for i in range(4):   # reduced from 7
                r = int((1.0 - p / 0.3) * (60 + i * 45))
                alpha_r = 1.0 - i * 0.18
                ov2 = frame.copy()
                cv2.circle(ov2, (cx, cy), r,
                           (80 + i*25, 180 + i*10, 255), 2 + i)
                cv2.addWeighted(ov2, alpha_r * 0.6, frame, 1 - alpha_r * 0.6, 0, frame)

        # ── phase 2 (0.3–0.6): full white FLASH ─────────────────────────────
        if 0.25 < p < 0.55:
            intensity = 1.0 - abs(p - 0.4) / 0.15
            intensity = max(0, min(1, intensity))
            overlay   = np.full_like(frame, 255)
            cv2.addWeighted(overlay, intensity * 0.95, frame,
                            1 - intensity * 0.95, 0, frame)

        # ── phase 3 (0.45–1.0): explosion outward ───────────────────────────
        if p > 0.45:
            # expanding shockwave rings
            for i in range(3):
                r = int((p - 0.45) / 0.55 * (w * 0.7) + i * 40)
                a = max(0, 1.0 - (p - 0.45) / 0.55 - i * 0.2)
                ov3 = frame.copy()
                cv2.circle(ov3, (cx, cy), r,
                           (180 - i*30, 220 - i*20, 255), 3)
                cv2.addWeighted(ov3, a * 0.7, frame, 1 - a * 0.7, 0, frame)

            # particles
            part_ov = frame.copy()
            for pt in self.particles:
                if pt["life"] > 0:
                    ratio = pt["life"] / pt["max"]
                    cv2.circle(part_ov, (int(pt["x"]), int(pt["y"])),
                               int(pt["r"] * ratio), pt["color"], -1)
            cv2.addWeighted(part_ov, 0.8, frame, 0.2, 0, frame)

            # spiral streak lines radiating out
            if p < 0.8:
                for i in range(10):   # reduced from 16
                    angle  = (i / 10) * 2 * math.pi + p * 6
                    length = (p - 0.45) / 0.35 * min(w, h) * 0.6
                    ex = int(cx + math.cos(angle) * length)
                    ey = int(cy + math.sin(angle) * length)
                    bright = int(255 * (1.0 - (p - 0.45) / 0.35))
                    cv2.line(frame, (cx, cy), (ex, ey),
                             (bright//2, bright, 255), 1)

        # ── RASENGAN text ─────────────────────────────────────────────────
        if 0.32 < p < 0.75:
            ta = 1.0 - abs(p - 0.53) / 0.21
            ta = max(0, min(1, ta))
            to = frame.copy()
            cv2.putText(to, "RASENGAN!!",
                        (w//2 - 185, h//2 + 28),
                        cv2.FONT_HERSHEY_DUPLEX, 2.8,
                        (10, 50, 140), 10)
            cv2.putText(to, "RASENGAN!!",
                        (w//2 - 185, h//2 + 28),
                        cv2.FONT_HERSHEY_DUPLEX, 2.8,
                        (200, 235, 255), 3)
            cv2.addWeighted(to, ta * 0.94, frame, 1 - ta * 0.94, 0, frame)

        # age particles
        for pt in self.particles:
            pt["x"] += pt["vx"]; pt["y"] += pt["vy"]
            pt["vy"] += 0.2;     pt["vx"] *= 0.96
            pt["life"] -= 1

        self.frame_count += 1
        if self.frame_count >= self.total:
            self.active = False
        return frame


class RasenganEffect:
    def __init__(self):
        self.intensity   = 0
        self.spin_angle  = 0.0       # rotating ring angle
        self.orb_scale   = 0.0       # size of the orb 0-1
        self.particles   = []        # orbiting energy particles
        self.frame_count = 0

        self._last_center    = None
        self._throw_cooldown = 0
        self._prev_center    = None
        self._was_claw       = False   # claw state last frame

        self.sound = RasenganSound()
        self.blast = RasenganBlast()

    # ── public API ────────────────────────────────────────────────────────────

    def update(self, frame, claw_detected, palm_center):
        h, w = frame.shape[:2]

        if self._throw_cooldown > 0:
            self._throw_cooldown -= 1

        # ── blast trigger: claw was held, now released (hand opened) ────────
        claw_just_opened = self._was_claw and not claw_detected
        if claw_just_opened and self.intensity > 30 and self._throw_cooldown == 0:
            origin = self._last_center if self._last_center else (w // 2, h // 2)
            self.blast.trigger(origin)
            self.sound.play_blast()
            self.sound.stop_spin()
            self.intensity       = 0
            self.orb_scale       = 0
            self._throw_cooldown = 50
            self.particles       = []

        # ── throw: fast movement while claw active ────────────────────────
        threw = False
        if claw_detected and palm_center and self.intensity > 25 \
                and self._throw_cooldown == 0:
            threw = self._detect_throw(palm_center)
            if threw:
                origin = palm_center
                self.blast.trigger(origin)
                self.sound.play_blast()
                self.sound.stop_spin()
                self.intensity       = 0
                self.orb_scale       = 0
                self._throw_cooldown = 50
                self.particles       = []

        if self.blast.active:
            frame = self.blast.update(frame)
            self._prev_center = palm_center
            return frame

        # ── charging ─────────────────────────────────────────────────────
        if claw_detected and palm_center and not threw:
            self._ramp_up()
            self._last_center = palm_center
            self.orb_scale    = min(1.0, self.orb_scale + 0.04)
            self.sound.play_spin(self.intensity / 100.0 * 0.9)

            self._spawn_orb_particles(palm_center)
            self._draw_aura(frame, palm_center)
            self._draw_orb(frame, palm_center)
            self._draw_spin_rings(frame, palm_center)
            self._draw_particles(frame)
            self._draw_hud(frame, w, h)

        else:
            self._ramp_down()
            self.orb_scale = max(0.0, self.orb_scale - 0.05)
            self.sound.play_spin(self.intensity / 100.0 * 0.4)
            if self.intensity <= 0:
                self.sound.stop_spin()
            if self.intensity > 5 and self._last_center:
                self._draw_orb(frame, self._last_center)
                self._draw_particles(frame)
            self.particles = [p for p in self.particles if p["life"] > 0]

        self._age_particles()
        self.spin_angle  += 0.08 + self.intensity * 0.002
        self.frame_count += 1
        self._prev_center = palm_center
        self._was_claw    = claw_detected
        return frame

    def cleanup(self):
        self.sound.stop_all()

    # ── throw detection ───────────────────────────────────────────────────────

    def _detect_throw(self, center):
        if self._prev_center is None:
            return False
        dx = center[0] - self._prev_center[0]
        dy = center[1] - self._prev_center[1]
        return math.sqrt(dx*dx + dy*dy) > 40

    # ── ramp ──────────────────────────────────────────────────────────────────

    def _ramp_up(self):
        self.intensity = min(100, self.intensity + 2.5)

    def _ramp_down(self):
        self.intensity = max(0, self.intensity - 4)

    # ── orb visuals ───────────────────────────────────────────────────────────

    def _draw_aura(self, frame, center):
        cx, cy  = center
        a       = self.intensity / 100.0
        overlay = frame.copy()
        for radius, op in [
            (int(100 + self.intensity * 0.6), 0.07),   # fewer layers, merged
            (int(55  + self.intensity * 0.3), 0.18),
            (int(32  + self.intensity * 0.2), 0.28),
        ]:
            col = (int(255*op*a), int(240*op*a), int(180*op*a))
            cv2.circle(overlay, (cx, cy), max(1, radius), col, -1)
        cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)
        # wind streak lines — fewer, every other frame
        if self.intensity > 20 and self.frame_count % 2 == 0:
            wov = frame.copy()
            base_r = int(70 + self.intensity * 0.45)
            for i in range(8):   # reduced from 12
                ang = (i / 8) * 2 * math.pi + self.spin_angle * 0.5
                sx  = cx + int(base_r * math.cos(ang))
                sy  = cy + int(base_r * 0.6 * math.sin(ang))
                cv2.line(wov, (sx, sy), (cx, cy), (100, 190, 255), 1)
            cv2.addWeighted(wov, 0.22 * a, frame, 1 - 0.22*a, 0, frame)

    def _draw_orb(self, frame, center):
        if self.orb_scale < 0.05:
            return
        cx, cy   = center
        base_r   = int(28 * self.orb_scale + self.intensity * 0.18)
        pulse    = abs(math.sin(self.frame_count * 0.15)) * 0.12 + 0.88
        r        = int(base_r * pulse)

        # layers from outer to inner — blue-white Rasengan palette
        layers = [
            (r + 8, (30,  120, 255), 2),
            (r + 4, (80,  170, 255), 3),
            (r,     (150, 210, 255), -1),
            (int(r*0.65), (210, 235, 255), -1),
            (int(r*0.30), (245, 250, 255), -1),
            (int(r*0.12), (255, 255, 255), -1),
        ]
        for radius, color, thickness in layers:
            if radius > 0:
                cv2.circle(frame, (cx, cy), radius, color, thickness)

    def _draw_spin_rings(self, frame, center):
        """Rotating dashed rings around the orb — the iconic Rasengan spiral."""
        cx, cy   = center
        base_r   = int(30 + self.intensity * 0.2)
        a        = min(self.intensity / 100.0, 1.0)
        overlay  = frame.copy()

        # draw 3 rotating ellipses at different tilt angles
        for i, tilt in enumerate([0, 60, 120]):
            angle_offset = self.spin_angle + math.radians(tilt)
            ring_r       = base_r + i * 8
            pts          = []
            for deg in range(0, 360, 8):
                rad  = math.radians(deg) + angle_offset
                x    = cx + int(ring_r * math.cos(rad))
                y    = cy + int(ring_r * 0.45 * math.sin(rad))
                pts.append((x, y))

            brightness = 180 + i * 25
            color      = (int(brightness * 0.4), int(brightness * 0.8), brightness)

            for j in range(0, len(pts), 2):   # skip every other = dashed look
                p1 = pts[j]
                p2 = pts[(j+1) % len(pts)]
                cv2.line(overlay, p1, p2, color, 2)

        cv2.addWeighted(overlay, min(a, 0.9), frame, 1 - min(a, 0.9), 0, frame)

    # ── orbiting particles ────────────────────────────────────────────────────

    def _spawn_orb_particles(self, center):
        cx, cy = center
        n      = int(self.intensity / 30) + 1   # reduced from /20+1
        base_r = int(30 + self.intensity * 0.2)

        for _ in range(n):
            angle = random.uniform(0, 2 * math.pi)
            orbit = base_r + random.randint(-10, 20)
            speed = random.uniform(0.08, 0.18)
            self.particles.append({
                "angle":  angle,
                "orbit":  orbit,
                "speed":  speed,
                "cx":     float(cx),
                "cy":     float(cy),
                "life":   random.randint(10, 20),
                "max":    20,
                "r":      random.randint(2, 4),
                "escape": random.random() < 0.2,
                "vx":     random.uniform(-2, 2) if random.random() < 0.2 else 0,
                "vy":     random.uniform(-3, -1) if random.random() < 0.2 else 0,
            })
        if len(self.particles) > 100:   # reduced cap from 200
            self.particles = self.particles[-100:]

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
            bright = int(200 + 55 * ratio)
            color  = (int(bright * 0.5), int(bright * 0.85), bright)
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

        cv2.rectangle(frame, (12, h-28), (12+bar_max, h-10), (10, 20, 40),  -1)
        cv2.rectangle(frame, (12, h-28), (12+bar_max, h-10), (40, 80, 160),  1)

        blue = int(200 + self.intensity * 0.55)
        if bar_w > 0:
            cv2.rectangle(frame, (12, h-28), (12+bar_w, h-10),
                          (20, int(120 + self.intensity*0.8), blue), -1)

        label = "MAX RASENGAN!! — OPEN HAND TO BLAST!" if self.intensity >= 95 else "RASENGAN"
        cv2.putText(frame, label, (12, h-34),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (20, int(120+self.intensity*0.8), blue), 1)
        cv2.putText(frame, f"{int(self.intensity)}%", (w-55, h-34),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (100, 180, 255), 1)

        if self.intensity > 25:
            cv2.putText(frame, "Keep charging... then OPEN YOUR HAND!",
                        (12, h-48),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.42, (120, 190, 255), 1)