from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired, Email, URL, Optional, Regexp
from qr import generate_vcard_qr
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[Optional(), Regexp(r'^\+[1-9]\d{1,14}$', message="Enter a valid phone number with country code.")])
    email = StringField('Email', validators=[Optional(), Email(message="Enter a valid email address.")])
    organization = StringField('Organization', validators=[Optional()])
    title = StringField('Title', validators=[Optional()])
    address = StringField('Address', validators=[Optional()])
    website = StringField('Website', validators=[Optional(), Regexp(r'^(http://|https://|www\.)[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(\S*)?$', message="Enter a valid website URL starting with http://, https://, or www.")])
    image = FileField('Profile Image', validators=[Optional()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        email = form.email.data
        organization = form.organization.data
        title = form.title.data
        address = form.address.data
        website = form.website.data
        image = form.image.data

        # Ensure website URLs are properly formatted
        if website and not website.startswith(('http://', 'https://', 'www.')):
            website = 'http://' + website

        image_path = None
        if image:
            image_path = os.path.join('images', image.filename)
            image.save(image_path)

        # Extract the first word of the name to use as a prefix for filenames
        name_prefix = name.split()[0]

        qr_filename = f"{name_prefix}_contact_qr.png"
        card_filename = f"{name_prefix}_contact_card.png"
        qr_filepath = os.path.join('output', qr_filename)
        card_filepath = os.path.join('output', card_filename)

        generate_vcard_qr(name, phone, email, organization, title, address, website, image_path, qr_filepath, card_filepath)
        
        return render_template('index.html', form=form, qr_image=qr_filename, card_image=card_filename)

    return render_template('index.html', form=form)

@app.route('/output/<filename>')
def output_file(filename):
    return send_from_directory('output', filename)

if __name__ == '__main__':
    app.run(debug=True)