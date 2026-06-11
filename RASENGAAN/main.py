import cv2
import numpy as np
import math
import random
import time

from utils.hand_detector import HandDetector
from effects.chidori import ChidoriEffect
from effects.rasengan import RasenganEffect
from effects.heart_effect import HeartEffect
from effects.Sukuna import SukunaEffect
from effects.infinity import InfinityEffect

# ── Gesture-based assignment (no fixed hand) ──────────────────────────────────
# Any hand can trigger any jutsu. Gestures are checked in priority order
# to prevent overlap. See _resolve_gestures() in main().

# ═══════════════════════════════════════════════════════════════════════════════
#  FIRE INTRO
# ═══════════════════════════════════════════════════════════════════════════════
class FireIntro:
    """
    Full-screen fire curtain that plays when the webcam first opens.
    Fire rises from the bottom, then burns away to reveal the live feed.
    Duration: ~3 seconds (90 frames at 30fps).
    """
    TOTAL = 90

    def __init__(self):
        self.frame_count = 0
        self.active      = True
        self._embers     = []
        for _ in range(80):   # reduced from 180 — still looks great
            self._embers.append({
                "x":    random.uniform(0, 640),
                "y":    random.uniform(400, 500),
                "vy":   random.uniform(-4, -1.5),
                "vx":   random.uniform(-1, 1),
                "life": random.randint(20, 60),
                "max":  60,
                "r":    random.randint(2, 5),
            })

    def _noise_fire(self, h, w, t):
        """Vectorised fire texture — same look, ~100× faster than Python loops."""
        rows = np.arange(h, dtype=np.float32)
        cols = np.arange(w, dtype=np.float32)
        C, R = np.meshgrid(cols, rows)

        norm_y  = 1.0 - R / h
        flame_h = norm_y ** 1.4

        noise = (np.sin(C * 0.05 + t * 3) * 0.5 +
                 np.sin(C * 0.13 - t * 5) * 0.3 +
                 np.sin(R * 0.07 + t * 2) * 0.2)
        val = np.clip(flame_h + noise * 0.25, 0.0, 1.0)

        r_ch = np.clip(val * 2.0,       0.0, 1.0)
        g_ch = np.clip((val - 0.3) * 1.5 * (180/255), 0.0, 1.0)
        b_ch = np.clip((val - 0.6) * 2.5 * (60/255),  0.0, 1.0)

        buf = np.stack([b_ch, g_ch, r_ch], axis=2)
        return (buf * 255).astype(np.uint8)

    def update(self, frame):
        if not self.active:
            return frame

        p = self.frame_count / self.TOTAL
        h, w = frame.shape[:2]
        t    = self.frame_count * 0.05

        # phase 1 (0–0.55): full fire curtain
        # phase 2 (0.55–1.0): fire burns upward revealing webcam feed
        if p < 0.55:
            fire = self._noise_fire(h, w, t)
            alpha = 0.92
            cv2.addWeighted(fire, alpha, frame, 1 - alpha, 0, frame)
        else:
            reveal = (p - 0.55) / 0.45          # 0→1
            cut_y  = int(h * reveal)             # webcam shows from top down
            fire   = self._noise_fire(h, w, t)
            # bottom part still fire
            frame[cut_y:] = cv2.addWeighted(
                fire[cut_y:], 0.88, frame[cut_y:], 0.12, 0)
            # fire-edge glow line
            if cut_y < h - 2:
                cv2.line(frame, (0, cut_y), (w, cut_y), (30, 140, 255), 3)
                cv2.line(frame, (0, cut_y+1),(w, cut_y+1),(10, 80, 200), 2)

        # ember particles — draw directly (no full-frame copy needed)
        for e in self._embers:
            if e["life"] > 0:
                ratio = e["life"] / e["max"]
                r_c = int(255 * ratio)
                g_c = int(120 * ratio * ratio)
                cv2.circle(frame, (int(e["x"]), int(e["y"])), e["r"],
                           (0, g_c, r_c), -1)

        for e in self._embers:
            e["x"] += e["vx"]; e["y"] += e["vy"]
            e["life"] -= 1
            if e["life"] <= 0:
                e["x"]   = random.uniform(0, w)
                e["y"]   = random.uniform(h * 0.7, h)
                e["vy"]  = random.uniform(-4, -1.5)
                e["vx"]  = random.uniform(-1, 1)
                e["life"] = random.randint(20, 60)

        # title stamp
        if p < 0.75:
            ta = min(1.0, p / 0.15) * (1.0 - max(0.0, (p - 0.6) / 0.15))
            to = frame.copy()
            cv2.putText(to, "DUAL JUTSU", (w//2 - 175, h//2 - 20),
                        cv2.FONT_HERSHEY_DUPLEX, 2.2, (30, 120, 255), 4)
            cv2.putText(to, "DUAL JUTSU", (w//2 - 175, h//2 - 20),
                        cv2.FONT_HERSHEY_DUPLEX, 2.2, (180, 220, 255), 2)
            cv2.putText(to, "CHIDORI  |  RASENGAN", (w//2 - 175, h//2 + 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.85, (200, 160, 60), 2)
            cv2.addWeighted(to, ta * 0.95, frame, 1 - ta * 0.95, 0, frame)

        self.frame_count += 1
        if self.frame_count >= self.TOTAL:
            self.active = False
        return frame


# ═══════════════════════════════════════════════════════════════════════════════
#  ARMOUR OVERLAY
# ═══════════════════════════════════════════════════════════════════════════════
class ArmourOverlay:
    """
    Draws glowing chakra-armour lines over the body using estimated
    face/shoulder positions from the frame.  No pose model needed —
    we approximate from frame proportions and face cascade.
    """
    def __init__(self):
        # try to load face detector for better positioning
        self._face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self._face_box  = None
        self._frame_cnt = 0
        self._pulse     = 0.0

    def _detect_face(self, frame):
        """Runs face detection every 10 frames to save CPU."""
        if self._frame_cnt % 10 == 0:
            gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self._face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
            if len(faces) > 0:
                # pick largest face — store as plain Python tuple (avoids numpy bool ambiguity)
                faces = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)
                self._face_box = tuple(int(v) for v in faces[0])
        self._frame_cnt += 1
        return self._face_box

    def draw(self, frame, chidori_intensity, rasengan_intensity):
        overall = max(chidori_intensity, rasengan_intensity) / 100.0
        if overall < 0.05:
            return frame

        h, w = frame.shape[:2]
        self._pulse += 0.08
        pulse = abs(math.sin(self._pulse)) * 0.4 + 0.6

        face = self._detect_face(frame)

        # ── derive body anchor points ─────────────────────────────────────
        if face is not None:
            fx, fy, fw, fh = face
            face_cx  = fx + fw // 2
            face_cy  = fy + fh // 2
            head_top = fy - int(fh * 0.2)
            neck_y   = fy + fh + int(fh * 0.15)
            shoulder_y   = neck_y + int(fh * 0.6)
            shoulder_span = int(fw * 2.8)
            chest_y  = shoulder_y + int(fh * 0.9)
            chest_w  = int(fw * 1.8)
        else:
            # fallback: assume face is centre-top of frame
            face_cx   = w // 2
            face_cy   = h // 4
            head_top  = h // 8
            neck_y    = int(h * 0.35)
            shoulder_y   = int(h * 0.42)
            shoulder_span = int(w * 0.55)
            chest_y   = int(h * 0.62)
            chest_w   = int(w * 0.30)

        ls = (face_cx - shoulder_span // 2, shoulder_y)   # left shoulder
        rs = (face_cx + shoulder_span // 2, shoulder_y)   # right shoulder
        lc = (face_cx - chest_w // 2, chest_y)            # left chest
        rc = (face_cx + chest_w // 2, chest_y)            # right chest
        neck = (face_cx, neck_y)

        # colour blend: chidori=cyan-white, rasengan=blue-gold
        chi_a = chidori_intensity / 100.0
        ras_a = rasengan_intensity / 100.0

        chi_col = (int(220 * chi_a * pulse), int(255 * chi_a * pulse), int(255 * chi_a * pulse))
        ras_col = (int(60  * ras_a * pulse), int(180 * ras_a * pulse), int(255 * ras_a * pulse))
        mix_col = (
            int((chi_col[0] + ras_col[0]) * 0.5),
            int((chi_col[1] + ras_col[1]) * 0.5),
            int((chi_col[2] + ras_col[2]) * 0.5),
        )

        ov  = frame.copy()
        thi = max(1, int(2 + overall * 3))

        # ── collar / neck ring ────────────────────────────────────────────
        collar_rx = int(fw*0.6) if face is not None else 40
        collar_ry = int(fw*0.2) if face is not None else 14
        cv2.ellipse(ov, neck, (collar_rx, collar_ry),
                    0, 0, 360, mix_col, thi)

        # ── shoulder pauldrons (arcs) ─────────────────────────────────────
        pauldron_r = int(fw * 0.55) if face is not None else 38
        cv2.ellipse(ov, ls, (pauldron_r, pauldron_r//2), 0, 180, 360, chi_col, thi+1)
        cv2.ellipse(ov, rs, (pauldron_r, pauldron_r//2), 0, 180, 360, ras_col, thi+1)

        # ── chest plate lines ─────────────────────────────────────────────
        cv2.line(ov, neck, lc, mix_col, thi)
        cv2.line(ov, neck, rc, mix_col, thi)
        cv2.line(ov, ls,   lc, chi_col, thi)
        cv2.line(ov, rs,   rc, ras_col, thi)
        cv2.line(ov, lc,   rc, mix_col, thi)

        # ── vertical sternum line ─────────────────────────────────────────
        sternum_top = neck
        sternum_bot = (face_cx, chest_y)
        cv2.line(ov, sternum_top, sternum_bot, mix_col, thi - 1)

        # ── energy nodes (circles at joints) ──────────────────────────────
        node_r = max(3, int(5 * overall * pulse))
        for pt, col in [(ls, chi_col), (rs, ras_col), (neck, mix_col),
                        (lc, chi_col), (rc, ras_col)]:
            cv2.circle(ov, pt, node_r + 2, col, 1)
            cv2.circle(ov, pt, node_r,     col, -1)

        # ── forehead symbol (diamond) ─────────────────────────────────────
        if overall > 0.3:
            sym_cx = face_cx
            sym_cy = head_top + int((neck_y - head_top) * 0.18)
            sym_s  = max(4, int(8 * overall * pulse))
            pts    = np.array([
                [sym_cx,        sym_cy - sym_s],
                [sym_cx + sym_s, sym_cy],
                [sym_cx,        sym_cy + sym_s],
                [sym_cx - sym_s, sym_cy],
            ], np.int32)
            cv2.polylines(ov, [pts], True, mix_col, max(1, thi-1))
            if overall > 0.6:
                cv2.fillPoly(ov, [pts], mix_col)

        alpha = min(0.85, overall * pulse * 0.9)
        cv2.addWeighted(ov, alpha, frame, 1 - alpha, 0, frame)
        return frame


# ═══════════════════════════════════════════════════════════════════════════════
#  OBITO MASK EFFECT
# ═══════════════════════════════════════════════════════════════════════════════
# class ObitoMaskEffect:
#     """
#     Draws a procedural Obito/Tobi-style spiral mask over the detected face.
#     No image file needed — drawn entirely with OpenCV primitives.
#     Face detection runs every 10 frames to stay CPU-cheap.

#     Mask features:
#       • White base mask covering face (ellipse)
#       • Black/dark curved mask-split line (half-face style)
#       • Single Sharingan spiral on the right eye hole
#       • Triangular/angular nose indent
#       • Chakra energy glow around mask that pulses with jutsu intensity
#       • Eye hole glows with the active jutsu colour
#     """
#     def __init__(self):
#         self._face_cas  = cv2.CascadeClassifier(
#             cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#         self._face_box  = None
#         self._frame_cnt = 0
#         self._pulse     = 0.0
#         self._spiral_angle = 0.0   # animated spiral rotation

#     # ── face detection (every 10 frames) ─────────────────────────────────────
#     def _detect_face(self, frame):
#         if self._frame_cnt % 10 == 0:
#             gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             faces = self._face_cas.detectMultiScale(
#                 gray, 1.1, 4, minSize=(70, 70))
#             if len(faces) > 0:
#                 faces = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)
#                 self._face_box = tuple(int(v) for v in faces[0])
#             else:
#                 self._face_box = None
#         self._frame_cnt += 1

#     # ── draw the mask onto frame ──────────────────────────────────────────────
#     def _draw_mask(self, frame, fx, fy, fw, fh, intensity, pulse):
#         cx = fx + fw // 2
#         cy = fy + fh // 2
#         rx = int(fw * 0.54)
#         ry = int(fh * 0.60)

#         # ── 1. Create mask canvas (draw onto overlay, blend in) ───────────
#         ov = frame.copy()

#         # Orange base fill  (Tobi's iconic orange)
#         ORANGE     = (0, 120, 230)    # BGR
#         DARK_LINE  = (0,  60, 140)    # darker orange for spiral lines
#         BLACK      = (10,  10,  10)

#         cv2.ellipse(ov, (cx, cy), (rx, ry), 0, 0, 360, ORANGE, -1)

#         # ── 2. Concentric spiral lines (the defining Tobi feature) ────────
#         # The spiral emanates FROM the eye hole outward.
#         # We approximate with concentric ellipses offset toward the eye,
#         # getting larger, giving the spiral/vortex illusion.
#         eye_cx = cx + int(fw * 0.16)   # eye is right-of-centre
#         eye_cy = cy - int(fh * 0.06)

#         num_rings = 10
#         for i in range(1, num_rings + 1):
#             # Each ring grows and shifts slightly to simulate spiral
#             scale  = i / num_rings
#             shift  = int(fw * 0.04 * (1 - scale))   # inner rings shift more
#             r_x    = int(rx * scale * 0.95)
#             r_y    = int(ry * scale * 0.92)
#             ring_cx = eye_cx - shift
#             ring_cy = eye_cy - int(fh * 0.01 * (1 - scale))
#             thickness = 2 if i % 2 == 0 else 1
#             cv2.ellipse(ov, (ring_cx, ring_cy), (max(1,r_x), max(1,r_y)),
#                         0, 0, 360, DARK_LINE, thickness)

#         # ── 3. Radial crack lines from eye outward (depth detail) ─────────
#         num_cracks = 8
#         for i in range(num_cracks):
#             angle  = (i / num_cracks) * 2 * math.pi
#             x_end  = eye_cx + int(rx * 0.85 * math.cos(angle))
#             y_end  = eye_cy + int(ry * 0.85 * math.sin(angle))
#             # fade the line — draw short segments getting lighter
#             for seg in range(4):
#                 t1 = (seg    ) / 4.0
#                 t2 = (seg + 1) / 4.0
#                 x1 = eye_cx + int((x_end - eye_cx) * t1)
#                 y1 = eye_cy + int((y_end - eye_cy) * t1)
#                 x2 = eye_cx + int((x_end - eye_cx) * t2)
#                 y2 = eye_cy + int((y_end - eye_cy) * t2)
#                 alpha_seg = int(80 * (1 - t1))
#                 col = (max(0, DARK_LINE[0]-alpha_seg),
#                        max(0, DARK_LINE[1]-20),
#                        max(0, DARK_LINE[2]-alpha_seg))
#                 cv2.line(ov, (x1, y1), (x2, y2), DARK_LINE, 1)

#         # ── 4. Blend orange mask onto frame ──────────────────────────────
#         cv2.addWeighted(ov, 0.82, frame, 0.18, 0, frame)

#         # ── 5. Outer mask edge ────────────────────────────────────────────
#         cv2.ellipse(frame, (cx, cy), (rx, ry), 0, 0, 360, BLACK, 3)

#         # ── 6. Eye hole — right side ──────────────────────────────────────
#         eye_rx = int(fw * 0.12)
#         eye_ry = int(fh * 0.10)
#         # Dark hole
#         cv2.ellipse(frame, (eye_cx, eye_cy), (eye_rx, eye_ry),
#                     0, 0, 360, (8, 6, 5), -1)
#         cv2.ellipse(frame, (eye_cx, eye_cy), (eye_rx, eye_ry),
#                     0, 0, 360, BLACK, 2)

#         # ── 7. Sharingan inside eye hole ──────────────────────────────────
#         self._spiral_angle += 0.05

#         # Iris — red
#         cv2.circle(frame, (eye_cx, eye_cy), eye_rx - 3, (0, 0, 180), -1)
#         # Pupil — black
#         cv2.circle(frame, (eye_cx, eye_cy), max(2, eye_rx // 3), (5, 5, 5), -1)

#         # 3 tomoe orbiting pupil
#         tomoe_orbit = max(3, int(eye_rx * 0.55))
#         for i in range(3):
#             ang = self._spiral_angle + (i / 3.0) * 2 * math.pi
#             tx  = eye_cx + int(tomoe_orbit * math.cos(ang))
#             ty  = eye_cy + int(tomoe_orbit * 0.75 * math.sin(ang))
#             tr  = max(2, eye_rx // 7)
#             cv2.circle(frame, (tx, ty), tr, (5, 5, 5), -1)
#             # teardrop tail
#             tail_ang = ang + 0.7
#             tx2 = tx + int(tr * 1.4 * math.cos(tail_ang))
#             ty2 = ty + int(tr * 1.4 * math.sin(tail_ang))
#             cv2.line(frame, (tx, ty), (tx2, ty2), (5, 5, 5), max(1, tr-1))

#         # White ring around iris
#         cv2.circle(frame, (eye_cx, eye_cy), eye_rx - 3, (60, 60, 200), 1)

#         # ── 8. Sharingan glow (scales with jutsu charge) ──────────────────
#         if intensity > 0:
#             glow_a  = min(1.0, intensity / 80.0) * pulse
#             glow_ov = frame.copy()
#             cv2.circle(glow_ov, (eye_cx, eye_cy), eye_rx + 8,
#                        (0, int(40*glow_a), int(255*glow_a)), -1)
#             cv2.addWeighted(glow_ov, 0.4 * glow_a, frame,
#                             1 - 0.4 * glow_a, 0, frame)

#         # ── 9. Chakra energy ring around mask (intensity driven) ──────────
#         if intensity > 5:
#             energy_a = min(1.0, intensity / 100.0) * pulse
#             e_ov = frame.copy()
#             glow_col = (int(100*energy_a), int(180*energy_a), int(255*energy_a))
#             cv2.ellipse(e_ov, (cx, cy), (rx+12, ry+12),
#                         0, 0, 360, glow_col, 4)
#             cv2.ellipse(e_ov, (cx, cy), (rx+22, ry+22),
#                         0, 0, 360, glow_col, 2)
#             cv2.addWeighted(e_ov, energy_a * 0.75, frame,
#                             1 - energy_a * 0.75, 0, frame)

#     def draw(self, frame, intensity):
#         self._pulse = abs(math.sin(self._frame_cnt * 0.05)) * 0.35 + 0.65
#         self._detect_face(frame)
#         if self._face_box is not None:
#             fx, fy, fw, fh = self._face_box
#             self._draw_mask(frame, fx, fy, fw, fh, intensity, self._pulse)
#         return frame


# ═══════════════════════════════════════════════════════════════════════════════
#  AMBIENT CHAKRA AURA (full-screen edge glow)
# ═══════════════════════════════════════════════════════════════════════════════
class AmbientAura:
    def __init__(self):
        self._t = 0.0

    def draw(self, frame, chidori_intensity, rasengan_intensity, sukuna_intensity=0):
        chi = chidori_intensity / 100.0
        ras = rasengan_intensity / 100.0
        suk = sukuna_intensity  / 100.0
        if chi < 0.05 and ras < 0.05 and suk < 0.05:
            return frame
        self._t += 0.07
        pulse = abs(math.sin(self._t)) * 0.3 + 0.7
        h, w  = frame.shape[:2]
        ov    = frame.copy()

        # vignette-style edge glow
        # chidori=right cyan, rasengan=left blue, sukuna=bottom red
        thickness = max(8, int(30 * max(chi, ras, suk)))
        if chi > 0.05:
            col = (int(180*chi*pulse), int(220*chi*pulse), int(255*chi*pulse))
            cv2.rectangle(ov, (w//2, 0), (w-1, h-1), col, thickness)
        if ras > 0.05:
            col = (int(40*ras*pulse), int(160*ras*pulse), int(255*ras*pulse))
            cv2.rectangle(ov, (0, 0), (w//2, h-1), col, thickness)
        if suk > 0.05:
            # dark red glow on bottom edge
            col = (0, int(20*suk*pulse), int(200*suk*pulse))
            cv2.rectangle(ov, (0, h//2), (w-1, h-1), col, thickness)
            # also darken screen corners for cursed feel
            corner_ov = ov.copy()
            dark_alpha = suk * pulse * 0.35
            corner_ov[:h//4, :w//4]   = (corner_ov[:h//4, :w//4] * (1-dark_alpha)).astype("uint8")
            corner_ov[:h//4, 3*w//4:] = (corner_ov[:h//4, 3*w//4:] * (1-dark_alpha)).astype("uint8")
            ov = corner_ov

        cv2.addWeighted(ov, 0.45, frame, 0.55, 0, frame)

        # scanline flicker when very charged
        if max(chi, ras) > 0.7 and random.random() < 0.3:
            for y in range(0, h, 8):
                if random.random() < 0.06 * max(chi, ras):
                    cv2.line(frame, (0, y), (w, y), (200, 230, 255), 1)
        # cursed energy flicker (red-tinted scanlines)
        if suk > 0.6 and random.random() < 0.3:
            for y in range(0, h, 10):
                if random.random() < 0.05 * suk:
                    cv2.line(frame, (0, y), (w, y), (0, 0, 160), 1)
        return frame


# ═══════════════════════════════════════════════════════════════════════════════
#  HUD PANEL
# ═══════════════════════════════════════════════════════════════════════════════
def draw_hud(frame, chi_intensity, ras_intensity, suk_intensity,
             chi_hand, ras_hand,
             chi_lm_present, ras_lm_present, suk_lm_present=False):
    h, w = frame.shape[:2]
    bar_w = int(w * 0.22)
    bar_h = 14
    pad   = 10

    # ── Chidori bar (right side) ──────────────────────────────────────────
    chi_fill = int(bar_w * chi_intensity / 100)
    bx = w - bar_w - pad
    by = h - bar_h - pad
    cv2.rectangle(frame, (bx, by), (bx+bar_w, by+bar_h), (20, 20, 30), -1)
    cv2.rectangle(frame, (bx, by), (bx+bar_w, by+bar_h), (60, 80, 120), 1)
    if chi_fill > 0:
        blue  = int(200 + chi_intensity * 0.55)
        green = int(180 + chi_intensity * 0.5)
        cv2.rectangle(frame, (bx, by), (bx+chi_fill, by+bar_h),
                      (int(max(0,255-chi_intensity*2)), green, blue), -1)
    label = "⚡ CHIDORI" if not (chi_intensity >= 95) else "⚡ MAX — OPEN FIST!"
    col   = (100, 220, 255) if chi_lm_present else (60, 60, 80)
    cv2.putText(frame, label, (bx, by - 6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.42, col, 1)
    cv2.putText(frame, f"{int(chi_intensity)}%", (bx + bar_w + 4, by + bar_h - 2),
                cv2.FONT_HERSHEY_SIMPLEX, 0.38, col, 1)

    # ── Rasengan bar (left side) ──────────────────────────────────────────
    ras_fill = int(bar_w * ras_intensity / 100)
    bx2 = pad
    cv2.rectangle(frame, (bx2, by), (bx2+bar_w, by+bar_h), (10, 20, 40), -1)
    cv2.rectangle(frame, (bx2, by), (bx2+bar_w, by+bar_h), (40, 80, 160), 1)
    if ras_fill > 0:
        blue2 = int(200 + ras_intensity * 0.55)
        cv2.rectangle(frame, (bx2, by), (bx2+ras_fill, by+bar_h),
                      (20, int(120+ras_intensity*0.8), blue2), -1)
    label2 = "🌀 RASENGAN" if not (ras_intensity >= 95) else "🌀 MAX — OPEN HAND!"
    col2   = (255, 200, 80) if ras_lm_present else (60, 60, 80)
    cv2.putText(frame, label2, (bx2, by - 6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.42, col2, 1)
    cv2.putText(frame, f"{int(ras_intensity)}%",
                (bx2 + bar_w + 4, by + bar_h - 2),
                cv2.FONT_HERSHEY_SIMPLEX, 0.38, col2, 1)

    # ── gesture hint strip ────────────────────────────────────────────────
    hints = []
    if chi_lm_present and chi_intensity < 95:
        hints.append(("✊ FIST → charge Chidori", (100, 220, 255)))
    if ras_lm_present and ras_intensity < 95:
        hints.append(("🤚 CLAW → charge Rasengan", (255, 200, 80)))
    for i, (txt, col) in enumerate(hints):
        cv2.putText(frame, txt, (w//2 - 170, h - 34 + i*18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.40, col, 1)

    # ── Sukuna bar (centre-bottom) ────────────────────────────────────────
    suk_bar_w = int(w * 0.22)
    suk_fill  = int(suk_bar_w * suk_intensity / 100)
    suk_bx    = w // 2 - suk_bar_w // 2
    suk_by    = h - bar_h - pad
    cv2.rectangle(frame, (suk_bx, suk_by), (suk_bx+suk_bar_w, suk_by+bar_h), (10, 5, 20), -1)
    cv2.rectangle(frame, (suk_bx, suk_by), (suk_bx+suk_bar_w, suk_by+bar_h), (60, 0, 100), 1)
    if suk_fill > 0:
        red = int(100 + suk_intensity * 1.5)
        cv2.rectangle(frame, (suk_bx, suk_by), (suk_bx+suk_fill, suk_by+bar_h),
                      (0, 0, min(red, 255)), -1)
    suk_label = "DOMAIN EXPANSION!!" if suk_intensity >= 95 else "🔴 CURSED ENERGY"
    suk_col   = (0, 0, 200) if suk_lm_present else (40, 0, 60)
    cv2.putText(frame, suk_label, (suk_bx, suk_by - 6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.42, suk_col, 1)
    cv2.putText(frame, f"{int(suk_intensity)}%",
                (suk_bx + suk_bar_w + 4, suk_by + bar_h - 2),
                cv2.FONT_HERSHEY_SIMPLEX, 0.38, suk_col, 1)
    if suk_lm_present and suk_intensity < 95:
        cv2.putText(frame, "3-FINGER SALUTE → charge Sukuna",
                    (suk_bx - 40, suk_by - 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 0, 180), 1)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN LOOP
# ═══════════════════════════════════════════════════════════════════════════════
def _get_tip(lm):
    """Return index fingertip (landmark 8) as (x,y) or None."""
    if lm is None or len(lm) <= 8:
        return None
    pt = lm[8]
    try:
        return (int(pt[0]), int(pt[1]))
    except (IndexError, TypeError):
        return None


def _resolve_gestures(detector, hands):
    """
    Any hand can trigger any jutsu.
    Priority per hand (highest → lowest):
      1. FIST          → Chidori
      2. SUKUNA SALUTE → Sukuna   (3-finger; before claw to avoid overlap)
      3. CLAW          → Rasengan (only if NOT Sukuna)
      4. OPEN PALM     → Infinity (all 5 fingers out; only if NOT claw/fist/Sukuna)

    Each hand feeds into at most ONE effect.
    Same effect can only be active on ONE hand at a time.

    Returns dict with keys:
      fist_detected, fist_center,
      claw_detected, palm_center,
      sukuna_detected, sukuna_center,
      infinity_detected, infinity_center,
      left_tip, right_tip
    """
    result = dict(
        fist_detected=False,     fist_center=None,
        claw_detected=False,     palm_center=None,
        sukuna_detected=False,   sukuna_center=None,
        infinity_detected=False, infinity_center=None,
        left_tip=None,           right_tip=None,
    )

    left_lm  = hands.get("Left")
    right_lm = hands.get("Right")

    result["left_tip"]  = _get_tip(left_lm)
    result["right_tip"] = _get_tip(right_lm)

    for label, lm in [("Left", left_lm), ("Right", right_lm)]:
        if lm is None:
            continue

        # 1. Fist → Chidori
        if not result["fist_detected"] and detector.is_fist(lm):
            result["fist_detected"] = True
            result["fist_center"]   = detector.get_fist_center(lm)
            continue

        # 2. Sukuna salute → Sukuna  (BEFORE claw check)
        if not result["sukuna_detected"] and detector.is_sukuna_gesture(lm):
            result["sukuna_detected"] = True
            result["sukuna_center"]   = detector.get_sukuna_center(lm)
            continue

        # 3. Claw → Rasengan
        if not result["claw_detected"] and detector.is_claw(lm):
            result["claw_detected"] = True
            result["palm_center"]   = detector.get_palm_center(lm)
            continue

        # 4. Open palm → Infinity  (only reaches here if not fist/sukuna/claw)
        if not result["infinity_detected"] and detector.is_open_palm(lm):
            result["infinity_detected"] = True
            result["infinity_center"]   = detector.get_palm_center(lm)
            continue

    return result


def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    detector   = HandDetector()
    chidori    = ChidoriEffect()
    rasengan   = RasenganEffect()
    intro      = FireIntro()
    armour     = ArmourOverlay()
    aura       = AmbientAura()
    # obito_mask = ObitoMaskEffect()
    heart      = HeartEffect()
    sukuna     = SukunaEffect()
    infinity   = InfinityEffect()

    print("=" * 60)
    print("  DUAL JUTSU — Any Hand Edition")
    print("  ⚡ Chidori  → FIST (either hand)")
    print("  🌀 Rasengan → CLAW (either hand)")
    print("  🔴 Sukuna   → 3-FINGER SALUTE (either hand)")
    print("  💠 Infinity → OPEN PALM flat to camera (either hand)")
    print("  💖 Heart    → touch both INDEX fingertips together")
    print("  Note: each hand triggers ONE effect at a time.")
    print("  Press Q to quit.")
    print("=" * 60)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        # ── fire intro ────────────────────────────────────────────────────
        if intro.active:
            frame = intro.update(frame)
            cv2.imshow("DUAL JUTSU", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            continue

        # ── hand detection ────────────────────────────────────────────────
        frame, hands = detector.find_hands(frame, draw=False)

        # ── gesture resolution (any hand, no overlap) ─────────────────────
        g = _resolve_gestures(detector, hands)

        any_hand_present = any(h is not None for h in hands.values())
        left_lm  = hands.get("Left")
        right_lm = hands.get("Right")

        # ── ambient aura ──────────────────────────────────────────────────
        frame = aura.draw(frame, chidori.intensity, rasengan.intensity, sukuna.intensity)

        # ── armour overlay ────────────────────────────────────────────────
        if chidori.intensity > 15 or rasengan.intensity > 15:
            frame = armour.draw(frame, chidori.intensity, rasengan.intensity)

        # ── Obito mask ────────────────────────────────────────────────────
        # frame = obito_mask.draw(frame, max(chidori.intensity, rasengan.intensity))

        # ── jutsu effects ─────────────────────────────────────────────────
        frame = chidori.update(frame, g["fist_detected"],      g["fist_center"])
        frame = rasengan.update(frame, g["claw_detected"],     g["palm_center"])
        frame = sukuna.update(frame,   g["sukuna_detected"],   g["sukuna_center"])
        frame = infinity.update(frame, g["infinity_detected"], g["infinity_center"])

        # ── heart gesture ─────────────────────────────────────────────────
        frame = heart.update(frame, g["left_tip"], g["right_tip"])

        # ── HUD ───────────────────────────────────────────────────────────
        if (not chidori.blast.active and not rasengan.blast.active
                and not sukuna.blast.active and not infinity.blast.active
                and not heart.bloom.active):
            draw_hud(frame,
                     chidori.intensity, rasengan.intensity, sukuna.intensity,
                     "Any",             "Any",
                     any_hand_present,  any_hand_present,
                     any_hand_present)

        cv2.imshow("DUAL JUTSU", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    chidori.cleanup()
    rasengan.cleanup()
    sukuna.cleanup()
    infinity.cleanup()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()