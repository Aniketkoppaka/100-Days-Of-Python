from flask import Flask, render_template, request
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import io

app = Flask(__name__)

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No file part in the request.")

        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', error="No file selected.")

        if file:
            try:
                image_stream = file.read()
                image = Image.open(io.BytesIO(image_stream)).convert('RGB')

                image.thumbnail((100, 100))

                np_image = np.array(image)

                pixels = np_image.reshape(-1, 3)

                kmeans = KMeans(n_clusters=10, n_init='auto', random_state=42)
                kmeans.fit(pixels)

                dominant_colors_rgb = kmeans.cluster_centers_

                dominant_colors_hex = [rgb_to_hex(color) for color in dominant_colors_rgb]

                return render_template('index.html', colors=dominant_colors_hex)

            except Exception as e:
                print(f"Error processing image: {e}")
                return render_template('index.html', error="Invalid image file or processing error.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)