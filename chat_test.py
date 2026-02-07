import requests

url = "http://127.0.0.1:8000/v1/completions"

# Replace this with your actual model
model_name = "huggingface/starcoder"  # ya "local/D:/phase/models/ggml-model.bin"

while True:
    prompt = input("You: ")
    if prompt.lower() in ["quit", "exit"]:
        break

    data = {
        "model": model_name,
        "prompt": prompt,
        "max_tokens": 150
    }

    response = requests.post(url, json=data)
    if response.ok:
        result = response.json()
        print("Bot:", result['choices'][0]['text'])
    else:
        print("Error:", response.text)
