import requests

invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
stream = True

headers = {
    "Authorization": "Bearer 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",
    "Accept": "text/event-stream" if stream else "application/json"
}

image_url = "https://media.istockphoto.com/id/476116580/photo/sycamore-tree-in-summer-field-at-sunset-england-uk.jpg?s=612x612&w=0&k=20&c=KNQmjVuAJy8aCYC0RIZyR3GfD3w92giM_UVdWP5jcIk="  # 👈 your URL here


payload = {
    "model": "meta/llama-3.2-11b-vision-instruct",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What genre does this image belong to? Give a short answer in 5 words."
                },
                {
                    "type": "image_url",
                    "image_url": {"url": image_url}
                }
            ]
        }
    ],
    "max_tokens": 5,
    "temperature": 1.00,
    "top_p": 1.00,
    "stream": stream
}

response = requests.post(invoke_url, headers=headers, json=payload)

# ✅ Clean output — extract only the text
import json

output = ""
for line in response.iter_lines():
    if line:
        decoded = line.decode("utf-8")
        if decoded.startswith("data: ") and decoded != "data: [DONE]":
            try:
                chunk = json.loads(decoded[6:])  # remove "data: " prefix
                content = chunk["choices"][0]["delta"].get("content", "")
                if content:
                    print(content, end="", flush=True)
                    output += content
            except:
                pass

print()  # clean newline
print(f"\nFull reply: {output}")  # ✅ clean final answer
# ```

# ---

# ### What changed:

# | | Before | After |
# |---|---|---|
# | Output | Raw JSON chunks 🤮 | Clean text only ✅ |
# | Parsing | `line.decode("utf-8")` | `json.loads()` to extract content ✅ |
# | Variable | No output variable | `output` stores full reply ✅ |

# Now instead of seeing all that `{"id":"chatcmpl...` mess, you'll just see:
# ```
# landscape photography genre.

# Full reply: landscape photography genre.