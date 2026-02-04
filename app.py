from flask import Flask, render_template, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_image')
def generate_image():
    # Create a blank white image
    width, height = 800, 600
    color = (255, 255, 255)
    img = Image.new('RGB', (width, height), color)
    draw = ImageDraw.Draw(img)

    # Draw some festive background elements (confetti)
    for _ in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(5, 15)
        confetti_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.ellipse([x, y, x+size, y+size], fill=confetti_color)

    # Draw a representational cake
    cake_x, cake_y = 300, 400
    cake_width, cake_height = 200, 100
    draw.rectangle([cake_x, cake_y, cake_x + cake_width, cake_y + cake_height], fill=(255, 192, 203), outline="black") # Pink cake
    
    # Candles
    for i in range(3):
        candle_x = cake_x + 50 + (i * 50)
        draw.rectangle([candle_x, cake_y - 30, candle_x + 10, cake_y], fill="yellow", outline="black")
        draw.ellipse([candle_x, cake_y - 45, candle_x + 10, cake_y - 30], fill="orange") # Flame

    # Draw Text
    text_color = (0, 0, 128)
    try:
        # Try to load a nicer font, fallback to default
        font = ImageFont.truetype("arial.ttf", 40)
        font_small = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()

    text = "Happy Birthday Dad!!"
    text2 = "Love, your Daughter"
    
    # Calculate text size using textbbox (newer Pillow versions) or textsize (older)
    # Using a safe approach for recent Pillow versions:
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
    except AttributeError:
        # Fallback for older Pillow
        text_width, _ = draw.textsize(text, font=font)

    draw.text(((width - text_width) / 2, 100), text, fill=text_color, font=font)
    
    # Draw simple stick figures to represent Father and Daughter
    # Father
    draw.ellipse([200, 300, 260, 360], fill="peachpuff", outline="black") # Head
    draw.line([230, 360, 230, 480], fill="blue", width=5) # Body
    draw.line([230, 400, 180, 450], fill="blue", width=5) # Arm L
    draw.line([230, 400, 280, 450], fill="blue", width=5) # Arm R
    draw.line([230, 480, 200, 550], fill="black", width=5) # Leg L
    draw.line([230, 480, 260, 550], fill="black", width=5) # Leg R
    
    # Daughter (smaller, dress)
    draw.ellipse([540, 320, 590, 370], fill="peachpuff", outline="black") # Head
    draw.polygon([565, 370, 520, 500, 610, 500], fill="purple", outline="black") # Dress
    draw.line([565, 390, 530, 440], fill="purple", width=4) # Arm L
    draw.line([565, 390, 600, 440], fill="purple", width=4) # Arm R
    draw.line([550, 500, 550, 550], fill="black", width=4) # Leg L
    draw.line([580, 500, 580, 550], fill="black", width=4) # Leg R

    draw.text(((width - 200) / 2, 530), text2, fill="purple", font=font_small)

    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
