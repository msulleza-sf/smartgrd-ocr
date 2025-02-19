import os
import PIL
from google import genai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from google.genai import types

# Load environment variables from .env file
from pathlib import Path

# Load environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Flask app
app = Flask(__name__)

# Load API key from .env file
api_key = os.getenv("GEMINI_API_KEY")

# Ensure API key is available
if not api_key:
    raise ValueError("Missing Gemini API Key. Set GEMINI_API_KEY in a .env file.")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

@app.route("/analyze-image", methods=["POST"])
def analyze_image():
    print("Request body:", request.json)
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files["image"]
    
    # Save the uploaded image file directly
    image_path = "./tmp/uploaded_image.jpeg"
    image_file.save(image_path)
    
    image = PIL.Image.open(image_path)

    # Call Gemini API
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=["Tell me the digits in this image", image],
    )

    # Extract response content
    print(response.text)
    return jsonify({
        "response": response.text,
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085, debug=True)