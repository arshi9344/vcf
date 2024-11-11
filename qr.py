import qrcode
from PIL import Image, ImageDraw, ImageFont

def generate_vcard_qr(name, phone, email=None, organization=None, title=None, address=None, website=None, image_path=None, filename="contact_qr.png"):
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
TEL:{phone}
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
    qr_img.save(filename)
    print(f"QR code saved as {filename}")

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
    draw.text((20, 100), f"Phone: {phone}", fill="black", font=small_font)
    if email:
        draw.text((20, 130), f"Email: {email}", fill="black", font=small_font)
    if organization:
        draw.text((20, 160), f"Organization: {organization}", fill="black", font=small_font)
    if title:
        draw.text((20, 190), f"Title: {title}", fill="black", font=small_font)
    if address:
        draw.text((20, 220), f"Address: {address}", fill="black", font=small_font)
    if website:
        draw.text((20, 250), f"Website: {website}", fill="black", font=small_font)
    
    # Paste the contact image onto the card if available
    if image_path:
        try:
            contact_img = Image.open(image_path)
            contact_img = contact_img.resize((150, 150))
            card_img.paste(contact_img, (430, 90))
        except IOError:
            print(f"Could not open image at {image_path}")

    # Paste the QR code onto the card at the bottom
    qr_img = qr_img.resize((150, 150))
    card_img.paste(qr_img, (430, 250))

    # Save the contact card
    card_filename = "contact_card.png"
    card_img.save(card_filename)
    print(f"Contact card saved as {card_filename}")

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
