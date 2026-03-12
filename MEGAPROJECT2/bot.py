import google.generativeai as genai

genai.configure(
    api_key="AIzaSyAoBAMkfo22L8tvtkj-LDMdDqUN9wJJA5Y"
)  # Free from aistudio.google.com

model = genai.GenerativeModel("gemini-1.5-flash")

command = """
[12:28, 12/3/2026] Aditya: Aagya bhai
[12:28, 12/3/2026] Aditya: Paper dekek
[19:26, 12/3/2026] Aditi: Paper dekek
Achaa
[19:53, 12/3/2026] Aditya: Guuu
[19:53, 12/3/2026] Aditya: Me nahane jaara
[19:56, 12/3/2026] Aditi: Acha
"""

response = model.generate_content(
    "You are a person named Harry who speaks Hindi and English. "
    "He is from India and is a coder. Respond like Harry.\n\n"
    f"Chat: {command}"
)

print(response.text)
