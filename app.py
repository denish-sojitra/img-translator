from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap

app = Flask(__name__)

@app.route('/overlay', methods=['POST'])
def overlay_text():
    image_file = request.files['image']
    text = request.form.get('text', '')

    image = Image.open(image_file)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 24)
    except:
        font = ImageFont.load_default()

    wrapped_text = textwrap.wrap(text, width=50)
    y = 30
    for line in wrapped_text:
        draw.text((30, y), line, font=font, fill="black")
        y += 30

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)
    return send_file(buffer, mimetype='image/jpeg')
