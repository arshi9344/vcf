import qrcode
from PIL import Image, ImageDraw, ImageFont

def generate_vcard_qr(name, phone=None, email=None, organization=None, title=None, address=None, website=None, image_path=None, qr_filename="contact_qr.png", card_filename="contact_card.png"):
    # Split the name into first and last name
    name_parts = name.split()
    first_name = name_parts[0]
    last_name = name_parts[-1] if len(name_parts) > 1 else ""

    # Define vCard format for contact details
    vcard_data = f"""
BEGIN:VCARD
VERSION:3.0
FN:{name}
N:{last_name};{first_name};;;
ORG:{organization or ""}
TITLE:{title or ""}
TEL:{phone or ""}
EMAIL:{email or ""}
ADR:;;{address or ""};;;
URL:{website or ""}
END:VCARD
    """.strip()
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(vcard_data)
    qr.make(fit=True)

    # Generate QR code image
    qr_img = qr.make_image(fill='black', back_color='white')
    qr_img.save(qr_filename)
    print(f"QR code saved as {qr_filename}")

    # Generate contact card
    card_img = Image.new('RGB', (600, 400), color='#f0f0f0')
    draw = ImageDraw.Draw(card_img)
    
    # Load a font
    try:
        font = ImageFont.truetype("arial.ttf", 30)
        small_font = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Draw a colored rectangle for the header
    draw.rectangle([(0, 0), (600, 80)], fill="#4CAF50")

    # Draw text on the card
    draw.text((20, 20), f"{name}", fill="white", font=font)
    
    y_position = 100
    if phone:
        draw.text((20, y_position), f"Phone: {phone}", fill="black", font=small_font)
        y_position += 30
    if email:
        draw.text((20, y_position), f"Email: {email}", fill="black", font=small_font)
        y_position += 30
    if organization:
        draw.text((20, y_position), f"Organization: {organization}", fill="black", font=small_font)
        y_position += 30
    if title:
        draw.text((20, y_position), f"Title: {title}", fill="black", font=small_font)
        y_position += 30
    if address:
        draw.text((20, y_position), f"Address: {address}", fill="black", font=small_font)
        y_position += 30
    if website:
        draw.text((20, y_position), f"Website: {website}", fill="black", font=small_font)
        y_position += 30
    
    # Paste the contact image onto the card if available
    if image_path:
        try:
            contact_img = Image.open(image_path)
            contact_img = contact_img.resize((150, 150))
            card_img.paste(contact_img, (430, 100))
        except IOError:
            print(f"Could not open image at {image_path}")

    # Paste the QR code onto the card aligned with the contact image
    qr_img = qr_img.resize((150, 150))
    card_img.paste(qr_img, (430, 260))

    # Save the contact card
    card_img.save(card_filename)
    print(f"Contact card saved as {card_filename}")

if __name__ == "__main__":
    # Example usage
    generate_vcard_qr(
        name="John Doe",
        phone="+123456789",
        email="johndoe@example.com",
        organization="Example Inc.",
        title="Software Engineer",
        address="123 Example St, Example City",
        website="https://example.com",
        image_path="pfp.jpg"
    )