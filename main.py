import pyautogui
import pyperclip
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def check_text_with_groq(text):
    client = Groq(api_key="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")

    # Instruction for analysis
    prompt = (
        f"Analyze the following text:\n{text}\n\n"
        "If the text contains criminal activities, fraud, drug trafficking, or brainwashing, respond with:\n"
        "'DANGEROUS' followed by a 50-character explanation.\n\n"
        "If the text is safe, respond with:\n"
        "'SAFE' followed by a response of 10-15 characters."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,  # Consistency
        max_tokens=100,  # Ensure enough space for response
        top_p=1,
        stream=False,
    )

    result_text = response.choices[0].message.content.strip()  # Extract response
    return result_text

@app.route('/analyze', methods=['GET'])
def analyze_text():
    try:
        pyautogui.click(1127, 1049)
        time.sleep(1)

        pyautogui.moveTo(602, 221)
        pyautogui.dragTo(1869, 934, duration=1, button='left')
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(1)

        copied_text = pyperclip.paste()

        groq_response = check_text_with_groq(copied_text)

        if groq_response.startswith("DANGEROUS"):
            response = {
                "status": "🚨 Response is DANGEROUS! 🚨",
                "reason": groq_response[10:].strip()
            }
        else:
            response = {
                "status": "✅ Response is SAFE. ✅",
                "reason": groq_response[5:].strip()
            }
        pyautogui.click(1127, 1049)

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
