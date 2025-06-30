from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont
from transformers import pipeline
import tempfile
import os

app = Flask(__name__)

# Translation model
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-hi")

@app.route("/overlay", methods=["POST"])
def translate_and_overlay():
    if "image" not in request.files or "text" not in request.form:
        return jsonify({"error": "Please provide an image and text to translate"}), 400

    img_file = request.files["image"]
    text_to_translate = request.form["text"]
    target_lang = request.form.get("lang", "hi")  # default to Hindi

    # Translate
    translated = translator(text_to_translate, src="en", tgt=target_lang)[0]["translation_text"]

    # Load image
    image = Image.open(img_file.stream).convert("RGB")

    # Draw text
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((10, 10), translated, fill=(255, 0, 0), font=font)

    # Save to temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    image.save(temp_file.name)
    return send_file(temp_file.name, mimetype="image/jpeg")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))  # required for Render
    app.run(debug=False, host="0.0.0.0", port=port)

