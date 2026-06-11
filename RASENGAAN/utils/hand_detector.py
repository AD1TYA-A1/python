import cv2
import mediapipe as mp

_hands_module   = mp.solutions.hands
_drawing_module = mp.solutions.drawing_utils

class HandDetector:
    def __init__(self):
        self.mp_hands = _hands_module
        self.hands    = _hands_module.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.6,
            model_complexity=0
        )
        self.mp_draw = _drawing_module
        self.results = None

    def find_hands(self, frame, draw=False):
        """
        Returns (frame, hands_dict) where hands_dict is:
          { "Left":  [21 (x,y) landmarks] or None,
            "Right": [21 (x,y) landmarks] or None }
        Frame must already be flipped before calling so that
        "Left"/"Right" match the player's actual hands.
        """
        rgb          = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)
        h, w, _      = frame.shape

        hands = {"Left": None, "Right": None}

        if self.results.multi_hand_landmarks and self.results.multi_handedness:
            for hand_lms, handedness in zip(
                    self.results.multi_hand_landmarks,
                    self.results.multi_handedness):

                label = handedness.classification[0].label   # "Left" or "Right"

                if draw:
                    self.mp_draw.draw_landmarks(
                        frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)

                hands[label] = [(int(lm.x * w), int(lm.y * h))
                                for lm in hand_lms.landmark]

        return frame, hands

    # ── Chidori: closed fist ──────────────────────────────────────────────────

    def is_fist(self, landmarks):
        """All 4 fingers curled fully — closed fist."""
        if len(landmarks) < 21:
            return False
        finger_tips  = [8, 12, 16, 20]
        finger_bases = [5,  9, 13, 17]
        curled = sum(
            1 for tip, base in zip(finger_tips, finger_bases)
            if landmarks[tip][1] > landmarks[base][1]
        )
        return curled == 4

    def get_fist_center(self, landmarks):
        if len(landmarks) < 18:
            return None
        palm_points = [0, 5, 9, 17]
        cx = sum(landmarks[i][0] for i in palm_points) // 4
        cy = sum(landmarks[i][1] for i in palm_points) // 4
        return (cx, cy)

    # ── Rasengan: claw hand ───────────────────────────────────────────────────

    def is_claw(self, landmarks):
        """
        Claw / bowl gesture — fingers bent but NOT fully closed.
        Each fingertip is BELOW its PIP joint (mid-knuckle) but
        ABOVE its MCP base knuckle.

        Landmark pairs:
          index:  tip=8,  pip=7,  mcp=5
          middle: tip=12, pip=11, mcp=9
          ring:   tip=16, pip=15, mcp=13
          pinky:  tip=20, pip=19, mcp=17
        """
        if len(landmarks) < 21:
            return False

        tips  = [8,  12, 16, 20]
        pips  = [7,  11, 15, 19]
        mcps  = [5,   9, 13, 17]

        claw_count = 0
        for tip, pip, mcp in zip(tips, pips, mcps):
            tip_y = landmarks[tip][1]
            pip_y = landmarks[pip][1]
            mcp_y = landmarks[mcp][1]
            # tip below pip (bent) but above mcp (not fully closed)
            if tip_y > pip_y and tip_y < mcp_y + 15:
                claw_count += 1

        return claw_count >= 3    # at least 3 fingers in claw shape

    def get_palm_center(self, landmarks):
        """Center of palm — average of wrist + 4 MCP knuckles."""
        if len(landmarks) < 18:
            return None
        points = [0, 5, 9, 13, 17]
        cx = sum(landmarks[i][0] for i in points) // len(points)
        cy = sum(landmarks[i][1] for i in points) // len(points)
        return (cx, cy)

    # ── Sukuna: 3-finger salute (thumb + index + middle up) ──────────────────

    def is_sukuna_gesture(self, landmarks):
        """
        Sukuna cursed energy gesture:
          • Thumb, index (8) and middle (12) fingers are EXTENDED (tips above MCP)
          • Ring (16) and pinky (20) fingers are CURLED (tips below their base)
        This mirrors the iconic 3-finger-raised pose.
        """
        if len(landmarks) < 21:
            return False

        # Thumb: tip (4) above IP joint (3) in y — extended upward
        thumb_up = landmarks[4][1] < landmarks[3][1]

        # Index and middle extended: tip above MCP base knuckle
        index_up  = landmarks[8][1]  < landmarks[5][1]
        middle_up = landmarks[12][1] < landmarks[9][1]

        # Ring and pinky curled: tip below their PIP joint
        ring_curl  = landmarks[16][1] > landmarks[14][1]
        pinky_curl = landmarks[20][1] > landmarks[18][1]

        return thumb_up and index_up and middle_up and ring_curl and pinky_curl

    def get_sukuna_center(self, landmarks):
        """Palm center for Sukuna orb — same as palm center."""
        return self.get_palm_center(landmarks)

    # ── Infinity: open palm facing camera ────────────────────────────────────

    def is_open_palm(self, landmarks):
        """
        Open palm facing camera — ALL 5 fingers fully extended upward.
        All fingertips are ABOVE their MCP base knuckles (in y).
        Distinguishes from Sukuna (which curls ring+pinky).
        """
        if landmarks is None or len(landmarks) < 21:
            return False

        # All 4 fingers: tip above MCP
        tips = [8,  12, 16, 20]
        mcps = [5,   9, 13, 17]
        fingers_up = sum(
            1 for tip, mcp in zip(tips, mcps)
            if landmarks[tip][1] < landmarks[mcp][1]
        )

        # Thumb extended sideways: tip x is far from base
        thumb_extended = abs(landmarks[4][0] - landmarks[2][0]) > 20

        return fingers_up == 4 and thumb_extended