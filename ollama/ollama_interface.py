# ollama/ollama_interface.py
import requests

def query_ollama(prompt: str, model: str = "llama3", stream: bool = True) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": stream},
            stream=True,
            timeout=30  # optional: prevent hanging requests
        )

        response.raise_for_status()  # Raise HTTPError for bad status codes

        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = line.decode("utf-8")
                    if '"response":"' in data:
                        chunk = data.split('"response":"')[1].split('"')[0]
                        full_response += chunk
                except Exception as e:
                    full_response += f"\n[Decoding error: {str(e)}]"

        return full_response.strip() or "[No response from Ollama]"

    except requests.exceptions.RequestException as e:
        return f"[Ollama connection error: {str(e)}]"
