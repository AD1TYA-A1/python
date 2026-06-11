# from openai import OpenAI
import pyautogui
import pyperclip
import time
from openai import OpenAI


response = ""


client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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",
)

Niceee

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
print("Dragging from (518, 168) to (1319, 664)...")
pyautogui.moveTo(511, 168, duration=0.4)
time.sleep(0.5)
# pyautogui.click(clicks=2, interval=0.05)  # double click first
# time.sleep(0.1)
pyautogui.dragTo(1316, 690, duration=2.0, button="left")
time.sleep(0.5)

# pyautogui.moveTo(500, 300, duration=0.3)  # move to start position
# time.sleep(0.2)


# pyautogui.mouseDown(button="left")  # hold mouse down
# time.sleep(0.15)
# pyautogui.moveTo(1200, 600, duration=0.8)  # drag to end
# pyautogui.mouseUp(button="left")  # release


# pyautogui.moveTo(518, 168, duration=0.3)
# pyautogui.mouseDown(button='left')
# time.sleep(0.15)
# pyautogui.moveTo(1316, 673, duration=0.8)
# pyautogui.mouseUp(button='left')
# ── Step 5: Copy selected text to clipboard
# ─────────────────────────────────
print("Copying selected text to clipboard...")
pyautogui.hotkey("ctrl", "c")
time.sleep(0.5)  # Give clipboard time to update

# ── Step 6: Save the copied chat text into a variable BEFORE overwriting ────
copied_chat = pyperclip.paste()
print(f"Chat text captured: '{copied_chat}'")
pyautogui.click(927, 510)


# ── Step 7: Move mouse back to taskbar to keep it visible ───────────────────
pyautogui.click(738, 729, duration=0.3)


print("Done!")


completion = client.chat.completions.create(
    model="nvidia/llama-3.3-nemotron-super-49b-v1.5",
    messages=[
        {
            "role": "system",
            "content": """You are Aditya, a 20-something self-taught coder from India.

You will be given a chat conversation. Read it and reply AS Aditya to the LAST message.

PERSONALITY:
- Casual, chill, confident
- Text like a friend, not an essay
- Use "bro", "yaar", "fr", "ngl" occasionally
- Light Hindi words like "yaar", "arre", "bas"

REPLY RULES:
- Reply to the LAST message in the chat only
- MAX 3-4 lines
- NO bullet points
- NO *action emotes* like *snorts* *laughs* *removes mask* NEVER
- No formal language
- You are a real person texting, NOT roleplay acting""",
        },
        {"role": "user", "content": f"Here is the chat, reply based on the conversation: \n\n {copied_chat}"},
    ],
    temperature=0.6,
    top_p=0.95,
    max_tokens=65536,
    frequency_penalty=0,
    presence_penalty=0,
    stream=True,
)


# completion = client.chat.completions.create(
#     model="deepseek-ai/deepseek-v3.2",
#     messages=[
#         {
#             "role": "system",
#             "content": """""",
#         },
#         {
#             "role": "user",
#             "content": f"Here is the chat, reply to the last message:\n\n{command}",  # 👈 your clipboard variable
#         },
#     ],
#     temperature=1,
#     top_p=1,
#     max_tokens=100,
#     stream=True,
# )

# # ✅ Safe streaming loop
# for chunk in completion:
#     if not getattr(chunk, "choices", None):
#         continue
#     delta = chunk.choices[0].delta
#     if getattr(delta, "content", None) is not None:
#         print(delta.content, end="", flush=True)


for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    response += chunk.choices[0].delta.content
    print(chunk.choices[0].delta.content, end="")



# for chunk in completion:
#     if not getattr(chunk, "choices", None):
#         continue
#     reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
#     #   if reasoning:
#     #     print(reasoning, end="")
#     if chunk.choices and chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content, end="")


print()
print()
final = response.split('</think>')[1]
print()
print(f"response is : {final}")
pyperclip.copy(final)
pyautogui.hotkey("ctrl", "v")
time.sleep(0.5)  # Give clipboard time to update
print("Done!!")
print()  # clean newlin

pyautogui.click(1326, 729, duration=0.3)
