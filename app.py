from flask import Flask, render_template, request, send_from_directory
from qr import generate_vcard_qr
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        organization = request.form.get('organization')
        title = request.form.get('title')
        address = request.form.get('address')
        website = request.form.get('website')
        image = request.files.get('image')

        image_path = None
        if image:
            image_path = os.path.join('static/images', image.filename)
            image.save(image_path)

        qr_filename = "static/images/contact_qr.png"
        card_filename = "static/images/contact_card.png"
        generate_vcard_qr(name, phone, email, organization, title, address, website, image_path, qr_filename, card_filename)
        
        return render_template('index.html', qr_image=qr_filename, card_image=card_filename)

    return render_template('index.html')

@app.route('/static/images/<filename>')
def download_file(filename):
    return send_from_directory('static/images', filename)

if __name__ == '__main__':
    app.run(debug=True)