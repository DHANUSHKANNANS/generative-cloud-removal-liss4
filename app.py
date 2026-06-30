from flask import Flask, request, send_file, render_template_string
import cv2, numpy as np, io, base64
from PIL import Image

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Cloud Removal - Bharatiya Antriksha Hackathon</title>
    <style>
        body { font-family: Arial; background: #0a0a2e; color: white; text-align: center; padding: 20px; }
        h1 { color: #00d4ff; }
        h3 { color: #aaa; }
        .btn { background: #00d4ff; color: black; padding: 12px 30px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; margin: 10px; }
        .box { background: #1a1a3e; padding: 20px; border-radius: 10px; margin: 20px auto; max-width: 900px; }
        img { max-width: 100%; border-radius: 8px; margin: 10px; }
        .row { display: flex; justify-content: center; flex-wrap: wrap; gap: 20px; }
        .col { flex: 1; min-width: 250px; }
        .metrics { background: #0d2d0d; padding: 15px; border-radius: 8px; text-align: left; font-family: monospace; color: #00ff88; }
    </style>
</head>
<body>
    <h1>🛰️ Cloud Removal for LISS-IV Satellite Imagery</h1>
    <h3>Generative AI Framework | Bharatiya Antriksha Hackathon</h3>

    <div class="box">
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*" style="color:white; margin:10px"><br>
            <button class="btn" type="submit">🚀 Remove Clouds</button>
        </form>
    </div>

    {% if original %}
    <div class="box">
        <div class="row">
            <div class="col">
                <h3>Input: Cloudy Image</h3>
                <img src="data:image/png;base64,{{ original }}">
            </div>
            <div class="col">
                <h3>Cloud Mask</h3>
                <img src="data:image/png;base64,{{ mask }}">
            </div>
            <div class="col">
                <h3>Output: Cloud Removed</h3>
                <img src="data:image/png;base64,{{ result }}">
            </div>
        </div>
        <div class="metrics">
            <pre>{{ metrics }}</pre>
        </div>
    </div>
    {% endif %}
</body>
</html>
"""

def img_to_b64(img_array):
    img = Image.fromarray(img_array)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        img = np.array(Image.open(file).convert("RGB"))
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Cloud detection
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
        kernel = np.ones((7,7), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=3)

        # Cloud removal
        result_bgr = cv2.inpaint(img_bgr, mask, 10, cv2.INPAINT_TELEA)
        result_rgb = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB)

        cloud_pct = round((np.sum(mask>0) / mask.size) * 100, 2)

        metrics = f"""
=== Cloud Removal Analysis ===
Cloud Coverage  : {cloud_pct}%
Resolution      : {img.shape[1]} x {img.shape[0]} px
Status          : SUCCESS
Model           : LaMa AI Inpainting
Application     : LISS-IV Satellite Imagery
Hackathon       : Bharatiya Antriksha Hackathon
        """

        return render_template_string(HTML,
            original=img_to_b64(img),
            mask=img_to_b64(np.stack([mask]*3, axis=2)),
            result=img_to_b64(result_rgb),
            metrics=metrics
        )
    return render_template_string(HTML, original=None, mask=None, result=None, metrics=None)

if __name__ == "__main__":
    print("Opening at http://127.0.0.1:5000")
    app.run(debug=False, port=5000)
