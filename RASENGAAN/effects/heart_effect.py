import cv2
import numpy as np
import math
import random


# ─────────────────────────────────────────────────────────────────────────────
#  Flower particle
# ─────────────────────────────────────────────────────────────────────────────

class Flower:
    """A small animated flower that blooms then fades out."""

    PETAL_COLORS = [
        (80,  80,  255),   # red-ish (BGR)
        (100, 60,  255),   # rose
        (140, 80,  255),   # pink-red
        (60,  120, 255),   # orange-red
        (180, 100, 255),   # pink
    ]

    def __init__(self, x, y):
        self.x      = x
        self.y      = y
        self.life   = 0
        self.max_life = random.randint(38, 55)
        self.size   = random.uniform(6, 13)
        self.angle  = random.uniform(0, 2 * math.pi)
        self.petals = random.randint(5, 7)
        self.color  = random.choice(self.PETAL_COLORS)
        # drift
        self.vx = random.uniform(-0.8, 0.8)
        self.vy = random.uniform(-1.5, -0.3)

    @property
    def alive(self):
        return self.life < self.max_life

    def update(self):
        self.life += 1
        self.x    += self.vx
        self.y    += self.vy
        self.vy   += 0.04          # gentle gravity
        self.angle += 0.05

    def draw(self, frame):
        progress = self.life / self.max_life
        # bloom-in then fade-out
        if progress < 0.25:
            scale = progress / 0.25
        elif progress < 0.65:
            scale = 1.0
        else:
            scale = 1.0 - (progress - 0.65) / 0.35

        alpha = max(0.0, scale)
        if alpha < 0.05:
            return

        sz = self.size * scale
        cx, cy = int(self.x), int(self.y)

        overlay = frame.copy()

        # petals
        for i in range(self.petals):
            a = self.angle + i * (2 * math.pi / self.petals)
            px = int(cx + math.cos(a) * sz)
            py = int(cy + math.sin(a) * sz)
            cv2.circle(overlay, (px, py), max(1, int(sz * 0.55)), self.color, -1)

        # centre
        centre_color = (200, 220, 255)  # soft white-yellow
        cv2.circle(overlay, (cx, cy), max(1, int(sz * 0.38)), centre_color, -1)

        cv2.addWeighted(overlay, alpha * 0.85, frame, 1 - alpha * 0.85, 0, frame)


# ─────────────────────────────────────────────────────────────────────────────
#  Heart bloom — the full-screen celebration
# ─────────────────────────────────────────────────────────────────────────────

class HeartBloom:
    """Draws a filled red heart + spawns flowers, then fades everything out."""

    TOTAL_FRAMES = 90

    def __init__(self):
        self.active      = False
        self.frame_count = 0
        self.origin      = (320, 240)
        self.flowers: list = []

    def trigger(self, origin):
        self.active      = True
        self.frame_count = 0
        self.origin      = origin
        self.flowers     = []
        # pre-spawn flowers in small centre cluster
        cx, cy = origin
        for _ in range(18):
            spread = random.randint(8, 30)
            angle  = random.uniform(0, 2 * math.pi)
            fx = cx + math.cos(angle) * spread
            fy = cy + math.sin(angle) * spread
            self.flowers.append(Flower(fx, fy))

    # ── helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _heart_point(t, cx, cy, size):
        x = cx + size * 16 * math.sin(t) ** 3 / 16
        y = cy - size * (13 * math.cos(t) - 5 * math.cos(2*t)
                         - 2 * math.cos(3*t) - math.cos(4*t)) / 16
        return int(x), int(y)

    @staticmethod
    def _draw_filled_heart(img, cx, cy, size, color, alpha=1.0):
        pts = []
        for i in range(200):
            t = -math.pi + 2 * math.pi * i / 200
            pts.append(HeartBloom._heart_point(t, cx, cy, size))
        poly = np.array(pts, dtype=np.int32).reshape(-1, 1, 2)
        overlay = img.copy()
        cv2.fillPoly(overlay, [poly], color)
        cv2.polylines(overlay, [poly], True, (60, 60, 220), 2)
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

    # ── main update ───────────────────────────────────────────────────────────

    def update(self, frame):
        if not self.active:
            return frame

        progress = self.frame_count / self.TOTAL_FRAMES
        cx, cy   = self.origin

        # heart alpha
        if progress < 0.18:
            heart_alpha = progress / 0.18
        elif progress < 0.65:
            heart_alpha = 1.0
        else:
            heart_alpha = 1.0 - (progress - 0.65) / 0.35
        heart_alpha = max(0.0, heart_alpha)

        pulse = 1.0 + 0.07 * math.sin(self.frame_count * 0.35)
        size  = int(72 * pulse * min(progress / 0.18, 1.0))

        # 1) flowers
        if progress < 0.55 and self.frame_count % 4 == 0:
            spread = random.randint(8, 30)
            angle  = random.uniform(0, 2 * math.pi)
            fx = cx + math.cos(angle) * spread
            fy = cy + math.sin(angle) * spread
            self.flowers.append(Flower(fx, fy))

        for f in self.flowers:
            f.update()
            f.draw(frame)
        self.flowers = [f for f in self.flowers if f.alive]

        # 2) heart on top
        if size > 1 and heart_alpha > 0.05:
            self._draw_filled_heart(frame, cx, cy, size, (50, 50, 220), heart_alpha)

        # 3) LOVE!! text
        if 0.2 < progress < 0.75:
            txt_a = 1.0 - abs(progress - 0.47) / 0.28
            txt_a = max(0.0, min(1.0, txt_a))
            if txt_a > 0.05:
                txt_overlay = frame.copy()
                font        = cv2.FONT_HERSHEY_DUPLEX
                font_scale  = 1.6
                thickness   = 3
                text        = "LOVE!!"
                (tw, th), _ = cv2.getTextSize(text, font, font_scale, thickness)
                tx = cx - tw // 2
                ty = cy + th // 2
                cv2.putText(txt_overlay, text, (tx, ty),
                            font, font_scale, (255, 255, 255), thickness)
                cv2.addWeighted(txt_overlay, txt_a * 0.95, frame,
                                1 - txt_a * 0.95, 0, frame)

        self.frame_count += 1
        if self.frame_count >= self.TOTAL_FRAMES and not self.flowers:
            self.active = False

        return frame


# ─────────────────────────────────────────────────────────────────────────────
#  Main HeartEffect class
# ─────────────────────────────────────────────────────────────────────────────

class HeartEffect:
    """
    Touch both index fingertips together to trigger a heart bloom + LOVE!!

    Usage in main.py:
        heart = HeartEffect()
        frame = heart.update(frame, left_index_tip, right_index_tip)

    left_index_tip / right_index_tip : (x, y) tuples or None
    """

    TOUCH_THRESHOLD  = 38   # px distance to count as touching
    TOUCH_HOLD_FRAMES = 10  # frames held before triggering
    TRAIL_MAX        = 60

    def __init__(self):
        self.trail_points   = []
        self.bloom          = HeartBloom()
        self._touch_counter = 0
        self._triggered     = False

    def update(self, frame, left_tip, right_tip):
        both_visible = left_tip is not None and right_tip is not None

        # ── trail update ──────────────────────────────────────────────────
        if both_visible:
            mx = (left_tip[0] + right_tip[0]) // 2
            my = (left_tip[1] + right_tip[1]) // 2
            self.trail_points.append((mx, my))
            if len(self.trail_points) > self.TRAIL_MAX:
                self.trail_points.pop(0)
        else:
            if self.trail_points:
                self.trail_points.pop(0)

        # ── proximity detection ───────────────────────────────────────────
        if both_visible:
            dist = math.hypot(left_tip[0] - right_tip[0],
                              left_tip[1] - right_tip[1])
            if dist < self.TOUCH_THRESHOLD:
                self._touch_counter += 1
            else:
                self._touch_counter = 0
                self._triggered     = False
        else:
            self._touch_counter = 0
            self._triggered     = False

        # ── trigger bloom ─────────────────────────────────────────────────
        if (self._touch_counter >= self.TOUCH_HOLD_FRAMES
                and not self._triggered
                and not self.bloom.active):
            self.bloom.trigger(left_tip)
            self._triggered   = True
            self.trail_points = []

        # ── draw trail (only when bloom not active) ───────────────────────
        if not self.bloom.active:
            self._draw_trail(frame)

        # ── draw bloom ────────────────────────────────────────────────────
        frame = self.bloom.update(frame)

        # ── fingertip dots ────────────────────────────────────────────────
        if both_visible and not self.bloom.active:
            for tip in (left_tip, right_tip):
                cv2.circle(frame, tip, 8,  (50,  50,  230), -1)
                cv2.circle(frame, tip, 10, (120, 120, 255),  2)

        return frame

    def _draw_trail(self, frame):
        if len(self.trail_points) < 2:
            return
        overlay = frame.copy()
        n = len(self.trail_points)
        for i in range(1, n):
            alpha     = i / n
            thickness = max(1, int(alpha * 5))
            color = (int(30 * alpha), int(30 * alpha), int(220 + 35 * alpha))
            cv2.line(overlay,
                     self.trail_points[i - 1],
                     self.trail_points[i],
                     color, thickness)
        cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)