from google import genai

client = genai.Client(api_key="Your API key")

command = """

[12:28, 12/3/2026] Aditya: Aagya bhai
[12:28, 12/3/2026] Aditya: Paper dekek
[19:26, 12/3/2026] Aditi: Paper dekek
Achaa
[19:53, 12/3/2026] Aditya: Guuu
[19:53, 12/3/2026] Aditya: Me nahane jaara
[19:56, 12/3/2026] Aditi: Acha
"""

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=(
        "You are a person named Harry who speaks Hindi and English. "
        "He is from India and is a coder. Respond like Harry.\n\n"
        f"Chat: {command}"
    ),
)

print(response.text)
