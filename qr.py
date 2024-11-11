import qrcode

def generate_vcard_qr(name, phone, email, organization, title, filename="contact_qr.png"):
    # Define vCard format for contact details
    vcard_data = f"""
BEGIN:VCARD
VERSION:3.0
FN:{name}
ORG:{organization}
TITLE:{title}
TEL:{phone}
EMAIL:{email}
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

    # Generate image and save as PNG
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)
    print(f"QR code saved as {filename}")

# Example usage
generate_vcard_qr(
    name="John Doe",
    phone="+123456789",
    email="johndoe@example.com",
    organization="Example Inc.",
    title="Software Engineer"
)
