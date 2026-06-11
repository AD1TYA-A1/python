import cv2
import numpy as np
import random
import math
import pygame

class ChidoriSound:
    """Generates and plays electricity sound using pygame."""

    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self._elec_sound    = self._make_electricity()
        self._blast_sound   = self._make_blast()
        self._elec_channel  = pygame.mixer.Channel(0)
        self._blast_channel = pygame.mixer.Channel(1)

    def _make_electricity(self):
        sr = 44100
        duration = 1.0
        n  = int(sr * duration)
        t  = np.linspace(0, duration, n)
        samples = np.zeros(n, dtype=np.float32)
        samples += 0.3  * np.sin(2 * math.pi * 180 * t)
        samples += 0.2  * np.sin(2 * math.pi * 360 * t)
        samples += 0.15 * np.sin(2 * math.pi * 720 * t)
        for _ in range(80):
            pos       = random.randint(0, n - 300)
            burst_len = random.randint(50, 300)
            burst     = np.random.uniform(-1, 1, burst_len).astype(np.float32)
            burst    *= np.linspace(1, 0, burst_len)
            samples[pos:pos + burst_len] += burst * 0.6
        samples += np.random.uniform(-0.15, 0.15, n).astype(np.float32)
        samples  = np.clip(samples, -1, 1)
        return self._to_pygame_sound(samples)

    def _make_blast(self):
        sr = 44100
        duration = 1.2
        n  = int(sr * duration)
        t  = np.linspace(0, duration, n)
        boom    = np.sin(2 * math.pi * 60 * t) * np.exp(-t * 5)
        boom   += np.sin(2 * math.pi * 30 * t) * np.exp(-t * 3)
        crack   = np.random.uniform(-1, 1, n).astype(np.float32) * np.exp(-t * 25)
        crackle = np.random.uniform(-0.4, 0.4, n).astype(np.float32) * np.exp(-t * 8)
        samples = boom * 0.7 + crack * 0.5 + crackle * 0.4
        samples = np.clip(samples, -1, 1)
        return self._to_pygame_sound(samples)

    def _to_pygame_sound(self, samples):
        pcm    = (samples * 32767).astype(np.int16)
        stereo = np.column_stack([pcm, pcm])   # mono → stereo
        return pygame.sndarray.make_sound(stereo)

    def play_electricity(self, volume=0.0):
        vol = max(0.0, min(1.0, volume))
        if not self._elec_channel.get_busy():
            self._elec_channel.play(self._elec_sound, loops=-1)
        self._elec_channel.set_volume(vol)

    def stop_electricity(self):
        self._elec_channel.fadeout(300)

    def play_blast(self):
        self._blast_channel.play(self._blast_sound)

    def stop_all(self):
        pygame.mixer.stop()


class BlastEffect:
    """Full-screen Chidori explosion — white flash, shockwave rings, debris bolts."""

    def __init__(self):
        self.active       = False
        self.frame_count  = 0
        self.total_frames = 40
        self.rings        = []
        self.origin       = (320, 240)
        self.debris       = []

    def trigger(self, origin):
        self.active      = True
        self.frame_count = 0
        self.origin      = origin
        self.rings       = [
            {"r":  10, "speed": 22, "alpha": 1.0, "color": (255, 255, 255), "thick": 4},
            {"r":  20, "speed": 32, "alpha": 1.0, "color": (180, 230, 255), "thick": 3},
            {"r":  35, "speed": 42, "alpha": 1.0, "color": (100, 200, 255), "thick": 2},
            {"r":  50, "speed": 55, "alpha": 1.0, "color": ( 60, 160, 255), "thick": 2},
            {"r":  10, "speed": 70, "alpha": 0.7, "color": (220, 240, 255), "thick": 1},
        ]
        cx, cy = origin
        self.debris = []
        for _ in range(35):  # reduced from 60
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(5, 22)
            self.debris.append({
                "x": float(cx), "y": float(cy),
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": random.randint(10, 28), "max": 28,
                "type": random.choice(["dot", "bolt"]),
            })

    def update(self, frame):
        if not self.active:
            return frame

        progress = self.frame_count / self.total_frames
        h, w     = frame.shape[:2]
        cx, cy   = self.origin

        # chromatic aberration on flash
        if progress < 0.35:
            strength = int((1.0 - progress / 0.35) * 8)
            if strength > 0:
                b_ch, g_ch, r_ch = cv2.split(frame)
                M_r = np.float32([[1,0, strength],[0,1,0]])
                M_b = np.float32([[1,0,-strength],[0,1,0]])
                r_ch = cv2.warpAffine(r_ch, M_r, (w, h))
                b_ch = cv2.warpAffine(b_ch, M_b, (w, h))
                shifted = cv2.merge([b_ch, g_ch, r_ch])
                cv2.addWeighted(shifted, 0.5, frame, 0.5, 0, frame)

        # white flash
        if progress < 0.38:
            flash_a = 1.0 - (progress / 0.38)
            overlay = np.full_like(frame, 255)
            cv2.addWeighted(overlay, flash_a * 0.94, frame,
                            1 - flash_a * 0.94, 0, frame)

        # expanding rings — single overlay pass
        if progress > 0.18:
            ring_ov = frame.copy()
            for ring in self.rings:
                ring["r"]    += ring["speed"] * 0.6
                ring["alpha"] = max(0, ring["alpha"] - 0.038)
                cv2.circle(ring_ov, (cx, cy), max(1, int(ring["r"])),
                           ring["color"], ring["thick"] + 2)
                cv2.circle(ring_ov, (cx, cy), max(1, int(ring["r"]) - 4),
                           ring["color"], ring["thick"])
            cv2.addWeighted(ring_ov, 0.75, frame, 0.25, 0, frame)

        # debris
        if 0.12 < progress < 0.82:
            dov = frame.copy()
            for d in self.debris:
                if d["life"] > 0:
                    ratio = d["life"] / d["max"]
                    col   = (int(80+(1-ratio)*175), int(210*ratio), int(255*ratio))
                    px, py = int(d["x"]), int(d["y"])
                    if d["type"] == "bolt":
                        ex2 = int(d["x"] - d["vx"] * 2)
                        ey2 = int(d["y"] - d["vy"] * 2)
                        cv2.line(dov, (px, py), (ex2, ey2), col, 2)
                        cv2.line(dov, (px, py), (ex2, ey2), (255,255,255), 1)
                    else:
                        cv2.circle(dov, (px, py), max(1, int(3*ratio)), col, -1)
            cv2.addWeighted(dov, 0.85, frame, 0.15, 0, frame)

        # ground strike lines — draw directly, no copy needed
        if 0.3 < progress < 0.7:
            fade = 1.0 - abs(progress - 0.5) / 0.2
            for _ in range(4):  # reduced from 6
                ang = random.uniform(-math.pi/2 - 0.4, -math.pi/2 + 0.4)
                lg  = random.randint(80, 220)
                ex_ = cx + int(math.cos(ang) * lg)
                ey_ = cy + int(math.sin(ang) * lg)
                alpha_line = int(fade * 180)
                cv2.line(frame, (cx, cy), (ex_, ey_), (200, 240, 255), 2)
                cv2.line(frame, (cx, cy), (ex_, ey_), (255, 255, 255), 1)

        # CHIDORI text
        if 0.22 < progress < 0.68:
            ta = 1.0 - abs(progress - 0.45) / 0.23
            ta = max(0, min(1, ta))
            to = frame.copy()
            cv2.putText(to, "CHIDORI!!",
                        (w//2 - 165, h//2 + 20),
                        cv2.FONT_HERSHEY_DUPLEX, 2.5, (30, 80, 160), 8)
            cv2.putText(to, "CHIDORI!!",
                        (w//2 - 165, h//2 + 20),
                        cv2.FONT_HERSHEY_DUPLEX, 2.5, (220, 245, 255), 3)
            cv2.addWeighted(to, ta * 0.93, frame, 1 - ta * 0.93, 0, frame)

        for d in self.debris:
            d["x"] += d["vx"]; d["y"] += d["vy"]
            d["vy"] += 0.3;    d["vx"] *= 0.96
            d["life"] -= 1

        self.frame_count += 1
        if self.frame_count >= self.total_frames:
            self.active = False
        return frame


class ChidoriEffect:
    def __init__(self):
        self.intensity          = 0
        self.sparks             = []
        self.bolt_timer         = 0
        self.screen_flash       = 0
        self.ring_radius        = 0
        self.ring_alpha         = 0.0
        self.chirp_frame        = 0
        self.trail_points       = []
        self._was_fist          = False           # fist state last frame
        self._last_known_center = None            # where fist was before release
        self._throw_cooldown    = 0

        self.sound = ChidoriSound()
        self.blast = BlastEffect()
        self._body_bolt_timer = 0

    # ── public API ────────────────────────────────────────────────────────────

    def update(self, frame, fist_detected, fist_center):
        h, w = frame.shape[:2]

        # cooldown ticker
        if self._throw_cooldown > 0:
            self._throw_cooldown -= 1

        # ── BLAST TRIGGER: fist was closed, now open ──────────────────────
        fist_just_opened = self._was_fist and not fist_detected
        if fist_just_opened and self.intensity > 30 and self._throw_cooldown == 0:
            origin = self._last_known_center if self._last_known_center else (w//2, h//2)
            self.blast.trigger(origin)
            self.sound.play_blast()
            self.sound.stop_electricity()
            self.intensity       = 0
            self._throw_cooldown = 45
            self.sparks          = []

        # ── blast animation takes over ────────────────────────────────────
        if self.blast.active:
            frame = self.blast.update(frame)
            self._was_fist = fist_detected
            return frame

        # ── normal chidori charging ───────────────────────────────────────
        if fist_detected and fist_center:
            prev = self.intensity
            self._ramp_up()
            self._last_known_center = fist_center   # remember position

            if prev < 15 and self.intensity >= 15:
                self.screen_flash = 8
                self.ring_radius  = 20
                self.ring_alpha   = 1.0

            self.sound.play_electricity(self.intensity / 100.0 * 0.85)

            self._add_trail(fist_center)
            self._draw_screen_distortion(frame)
            self._draw_trail(frame)
            self._draw_aura(frame, fist_center)
            self._draw_bolts(frame, fist_center)
            self._draw_sparks(frame)
            self._draw_core(frame, fist_center)
            self._draw_shock_ring(frame, fist_center)
            self._draw_screen_flash(frame)
            self._draw_hud(frame, w, h)
            self._spawn_sparks(fist_center)
            self._draw_body_bolts(frame, fist_center)
            self.chirp_frame += 1

        else:
            self._ramp_down()
            self.sound.play_electricity(self.intensity / 100.0 * 0.5)
            if self.intensity <= 0:
                self.sound.stop_electricity()
            if self.intensity > 5:
                self._draw_sparks(frame)
                self._draw_screen_flash(frame)
            self.trail_points = []

        self._age_sparks()
        self._update_ring()
        if self.screen_flash > 0:
            self.screen_flash -= 1

        self._was_fist = fist_detected   # save for next frame
        return frame

    def cleanup(self):
        self.sound.stop_all()
        pygame.mixer.quit()

    # ── ramp ──────────────────────────────────────────────────────────────────

    def _ramp_up(self):
        self.intensity = min(100, self.intensity + 3)

    def _ramp_down(self):
        self.intensity = max(0, self.intensity - 5)

    # ── trail ─────────────────────────────────────────────────────────────────

    def _add_trail(self, center):
        self.trail_points.append(center)
        if len(self.trail_points) > 12:
            self.trail_points.pop(0)

    def _draw_trail(self, frame):
        if len(self.trail_points) < 2:
            return
        overlay = frame.copy()
        for i in range(1, len(self.trail_points)):
            alpha     = i / len(self.trail_points)
            thickness = int(alpha * 6)
            color     = (int(255*alpha), int(220*alpha), int(80*alpha))
            cv2.line(overlay, self.trail_points[i-1], self.trail_points[i],
                     color, max(thickness, 1))
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)

    # ── screen distortion ─────────────────────────────────────────────────────

    def _draw_screen_distortion(self, frame):
        if self.intensity < 50:
            return
        strength = int((self.intensity - 50) / 50 * 3)
        if strength < 1:
            return
        b, g, r = cv2.split(frame)
        h, w    = frame.shape[:2]
        M_r = np.float32([[1, 0,  strength], [0, 1, 0]])
        M_b = np.float32([[1, 0, -strength], [0, 1, 0]])
        r   = cv2.warpAffine(r, M_r, (w, h))
        b   = cv2.warpAffine(b, M_b, (w, h))
        cv2.addWeighted(cv2.merge([b, g, r]), 0.35, frame, 0.65, 0, frame)

    # ── aura ──────────────────────────────────────────────────────────────────

    def _draw_aura(self, frame, center):
        cx, cy  = center
        a       = self.intensity / 100.0
        overlay = frame.copy()
        for radius, opacity in [
            (int(90 + self.intensity * 0.5), 0.10),
            (int(60 + self.intensity * 0.3), 0.20),
            (int(35 + self.intensity * 0.2), 0.35),
        ]:
            color = (int(255*opacity*a), int(230*opacity*a), int(100*opacity*a))
            cv2.circle(overlay, (cx, cy), radius, color, -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # ── bolts ─────────────────────────────────────────────────────────────────

    def _draw_bolts(self, frame, center):
        self.bolt_timer += 1
        if self.bolt_timer % 2 != 0:
            return
        cx, cy  = center
        n_bolts = int(3 + self.intensity / 22)   # slightly fewer bolts
        length  = int(45 + self.intensity * 0.85)
        a       = min(self.intensity / 100.0, 1.0)
        overlay = frame.copy()
        for _ in range(n_bolts):
            self._jagged_bolt(overlay, cx, cy,
                              random.uniform(0, 2*math.pi), length,
                              random.randint(4, 8))
        for _ in range(int(n_bolts * 0.4)):    # fewer thin bolts
            self._jagged_bolt(overlay, cx, cy,
                              random.uniform(0, 2*math.pi), int(length*0.5),
                              random.randint(3, 5), thin=True)
        cv2.addWeighted(overlay, min(a*1.1, 1.0), frame,
                        1 - min(a*1.1, 1.0), 0, frame)

    def _jagged_bolt(self, img, sx, sy, angle, length, segments, thin=False):
        pts  = [(sx, sy)]
        step = length / segments
        for _ in range(segments):
            a    = angle + random.uniform(-0.55, 0.55)
            prev = pts[-1]
            pts.append((int(prev[0] + math.cos(a)*step),
                        int(prev[1] + math.sin(a)*step)))
        if not thin:
            for i in range(len(pts)-1):
                cv2.line(img, pts[i], pts[i+1], (200, 255, 255), 4)
            for i in range(len(pts)-1):
                cv2.line(img, pts[i], pts[i+1], (255, 255, 255), 2)
            for i in range(len(pts)-1):
                cv2.line(img, pts[i], pts[i+1], (200, 230, 255), 1)
        else:
            for i in range(len(pts)-1):
                cv2.line(img, pts[i], pts[i+1], (150, 220, 255), 1)

    # ── sparks ────────────────────────────────────────────────────────────────

    def _spawn_sparks(self, center):
        cx, cy = center
        for _ in range(int(self.intensity / 20) + 1):   # reduced from /15+2
            angle = random.uniform(0, 2*math.pi)
            speed = random.uniform(2, 5 + self.intensity*0.06)
            self.sparks.append({
                "x": float(cx), "y": float(cy),
                "vx": math.cos(angle)*speed,
                "vy": math.sin(angle)*speed,
                "life": random.randint(8, 18), "max": 18,
                "type": random.choice(["dot", "line"]),
            })
        if len(self.sparks) > 90:   # reduced cap from 160
            self.sparks = self.sparks[-90:]

    def _draw_sparks(self, frame):
        for s in self.sparks:
            ratio = s["life"] / s["max"]
            color = (int(80+(1-ratio)*175), int(210*ratio), int(255*ratio))
            if s["type"] == "line" and s["life"] > 2:
                ex = int(s["x"] - s["vx"]*1.8)
                ey = int(s["y"] - s["vy"]*1.8)
                cv2.line(frame, (int(s["x"]), int(s["y"])), (ex, ey), color, 1)
            else:
                cv2.circle(frame, (int(s["x"]), int(s["y"])),
                           max(1, int(ratio*3)), color, -1)

    def _age_sparks(self):
        for s in self.sparks:
            s["x"]  += s["vx"];  s["y"]  += s["vy"]
            s["vy"] += 0.18;     s["vx"] *= 0.97
            s["life"] -= 1
        self.sparks = [s for s in self.sparks if s["life"] > 0]

    # ── core ──────────────────────────────────────────────────────────────────

    def _draw_core(self, frame, center):
        if self.intensity < 15:
            return
        cx, cy = center
        pulse  = abs(math.sin(self.chirp_frame * 0.25)) * 0.4 + 0.6
        r_out  = int((12 + self.intensity * 0.16) * pulse)
        r_mid  = max(1, int(r_out * 0.55))
        r_in   = max(1, int(r_out * 0.25))
        # outer bloom — single overlay with largest ring only (lighter cost)
        ov = frame.copy()
        cv2.circle(ov, (cx, cy), max(1, r_out + 18), (60, 160, 255), -1)
        cv2.addWeighted(ov, 0.22 * (self.intensity/100), frame,
                        1 - 0.22 * (self.intensity/100), 0, frame)
        cv2.circle(frame, (cx, cy), r_out + 4, (80,  180, 255), 2)
        cv2.circle(frame, (cx, cy), r_out,     (140, 220, 255), -1)
        cv2.circle(frame, (cx, cy), r_mid,     (210, 245, 255), -1)
        cv2.circle(frame, (cx, cy), r_in,      (255, 255, 255), -1)

    def _draw_body_bolts(self, frame, center):
        """Occasional wide arcs that crawl up the arm/body for drama."""
        self._body_bolt_timer += 1
        if self._body_bolt_timer % 7 != 0 or self.intensity < 50:  # less frequent
            return
        cx, cy = center
        h, w   = frame.shape[:2]
        ov     = frame.copy()
        n      = max(1, int(self.intensity / 50))  # fewer bolts
        for _ in range(n):
            tx = random.randint(0, w)
            ty = random.randint(0, h // 2)
            pts = [(cx, cy)]
            steps = 7  # reduced from 10
            for s in range(1, steps + 1):
                t = s / steps
                mx = int(cx + (tx - cx) * t + random.randint(-25, 25))
                my = int(cy + (ty - cy) * t + random.randint(-15, 15))
                pts.append((mx, my))
            for i in range(len(pts)-1):
                cv2.line(ov, pts[i], pts[i+1], (160, 220, 255), 2)
                cv2.line(ov, pts[i], pts[i+1], (240, 255, 255), 1)
        cv2.addWeighted(ov, 0.5, frame, 0.5, 0, frame)

    # ── shock ring ────────────────────────────────────────────────────────────

    def _update_ring(self):
        if self.ring_radius > 0:
            self.ring_radius += 8
            self.ring_alpha   = max(0.0, self.ring_alpha - 0.06)
            if self.ring_alpha <= 0:
                self.ring_radius = 0

    def _draw_shock_ring(self, frame, center):
        if self.ring_radius <= 0 or self.ring_alpha <= 0:
            return
        overlay = frame.copy()
        cv2.circle(overlay, center, self.ring_radius, (200, 240, 255), 3)
        cv2.addWeighted(overlay, self.ring_alpha, frame,
                        1 - self.ring_alpha, 0, frame)

    # ── screen flash ──────────────────────────────────────────────────────────

    def _draw_screen_flash(self, frame):
        if self.screen_flash <= 0:
            return
        a       = (self.screen_flash / 8) * 0.35
        overlay = np.full_like(frame, (220, 240, 255))
        cv2.addWeighted(overlay, a, frame, 1-a, 0, frame)

    # ── HUD ───────────────────────────────────────────────────────────────────

    def _draw_hud(self, frame, w, h):
        bar_max = int(w * 0.28)
        bar_w   = int(bar_max * (self.intensity / 100))

        cv2.rectangle(frame, (12, h-28), (12+bar_max, h-10), (20, 20, 30), -1)
        cv2.rectangle(frame, (12, h-28), (12+bar_max, h-10), (60, 80, 120),  1)

        r = int(max(0, 255 - self.intensity * 2))
        g = int(180 + self.intensity * 0.7)
        if bar_w > 0:
            cv2.rectangle(frame, (12, h-28), (12+bar_w, h-10), (r, g, 255), -1)

        label = "MAX CHIDORI!! — OPEN FIST TO BLAST!" if self.intensity >= 95 else "CHIDORI"
        cv2.putText(frame, label, (12, h-34),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (r, g, 255), 1)
        cv2.putText(frame, f"{int(self.intensity)}%", (w-55, h-34),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (160, 210, 255), 1)

        # hint appears once charged enough
        if 30 < self.intensity < 95:
            cv2.putText(frame, "Keep charging... then OPEN YOUR FIST!",
                        (12, h-48),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.42, (180, 220, 255), 1)