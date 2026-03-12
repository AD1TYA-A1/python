import pyautogui
import pyperclip
import time


# Safety pause between actions
pyautogui.PAUSE = 0.3

# ── Step 1: Move to taskbar area to prevent it from hiding ──────────────────
print("Moving mouse to taskbar to keep it visible...")
pyautogui.moveTo(707, 0, duration=0.3)
time.sleep(0.3)

# ── Step 2: Click the Chrome icon in the taskbar (717, 28) ──────────────────
print("Clicking Chrome icon at (717, 28)...")
pyautogui.click(717, 28)
time.sleep(1.5)

# ── Step 3: Move mouse to keep taskbar visible before drag ──────────────────
pyautogui.moveTo(717, 28, duration=0.2)
time.sleep(0.3)

# ── Step 4: Drag from (473, 196) to (1300, 693) ─────────────────────────────
print("Dragging from (518, 168) to (1292, 673)...")
pyautogui.moveTo(518, 168, duration=0.4)
time.sleep(0.2)
pyautogui.dragTo(1292, 673, duration=0.8, button='left')
time.sleep(0.5)

# ── Step 5: Copy selected text to clipboard ─────────────────────────────────
print("Copying selected text to clipboard...")
pyautogui.hotkey('ctrl', 'c')
time.sleep(0.5)  # Give clipboard time to update

# ── Step 6: Save the copied chat text into a variable BEFORE overwriting ────
copied_chat = pyperclip.paste()
print(f"Chat text captured: '{copied_chat}'")


# ── Step 7: Move mouse back to taskbar to keep it visible ───────────────────
pyautogui.moveTo(717, 28, duration=0.3)


print("Done!")