from colorthief import ColorThief
import matplotlib.pyplot as plt
from flask_uploads import configure_uploads, IMAGES, UploadSet
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import FileField
from PIL import Image
import base64
import io

photos = UploadSet("photos", IMAGES)


class InsertPic(FlaskForm):
    image = FileField('Select Your Picture')


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
configure_uploads(app, photos)
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = InsertPic()

    if form.validate_on_submit():
        filename = photos.save(form.image.data)
        file_url = f'static/img/{filename}'
        im = Image.open(f"{file_url}")
        data = io.BytesIO()
        im.save(data, "JPEG")
        image = base64.b64encode(data.getvalue())

        ct = ColorThief(f"{file_url}")
        colors = ct.get_palette(color_count=11)
        plt.imshow([[colors[a] for a in range(10)]])
        plt.axis('off')
        plt.savefig("output.jpg", bbox_inches='tight', pad_inches=0)
        im = Image.open("output.jpg")
        data = io.BytesIO()
        im.save(data, "JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())
        # Convet to HEX Values

        separate_colors = []

        for color in colors:
            a = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            separate_colors.append(a)
        return render_template('colors.html', colors=separate_colors, img_data=encoded_img_data.decode('utf-8'),
                               image=image.decode('utf-8'))

    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
