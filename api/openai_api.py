import requests  # Assuming you use requests to call the GPT-4 API

def call_gpt4_api(api_key, api_url, transcription):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": transcription}]
    }
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def correct_transcription(api_key, api_url, transcription):
    if len(transcription.split()) < 5:
        # Provide suggestions for short phrases instead of correcting
        suggestions = [
            f"There was an error while {transcription}.",
            f"{transcription} occurred during processing.",
            f"System encountered {transcription}. Please retry."
        ]
        return f"The original transcription is brief. Here are some ways to enhance it:\n{', '.join(suggestions)}"
    else:
        # Proceed with normal GPT-4 correction
        response = call_gpt4_api(api_key, api_url, transcription)
        return response['choices'][0]['message']['content']
