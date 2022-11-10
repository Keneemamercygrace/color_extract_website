from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
from colorthief import ColorThief
from datetime import datetime
import os
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/images/"
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/show", methods=['GET', 'POST'])
def show():
    file = request.files['file']
    print(file.filename)
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    full_image_path = f"static/images/{file.filename}"
    color_thief = ColorThief(full_image_path)
    top_colors = color_thief.get_palette(color_count=11)
    return render_template('colors.html', image=full_image_path, top_colors=top_colors)


@app.route("/demo")
def demo():
    file_path = "static/images/mohamed-nohassi-odxB5oIG_iA-unsplash.jpg"
    color_thief = ColorThief(file_path)
    all_colors = color_thief.get_palette(color_count=11)
    return render_template("demo.html", image=file_path, all_colors=all_colors)


if __name__ == "__main__":
    app.run(debug=True)
