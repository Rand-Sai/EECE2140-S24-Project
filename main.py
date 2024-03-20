#Semester Project - QR Code generator
import qrcode

class QRCodeGenerator:
    def __init__(self):
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
    def generate_qr_code(self, url):
        self.qr.clear()
        self.qr.add_data(url)
        self.qr.make(fit=True)

        
        # Create an image from the QR Code instance
        img = self.qr.make_image(fill_color="black", back_color="white")

        # Save the image with a name based on the URL
        img_name = url.replace("://", "_").replace("/", "_") + ".png"
        img.save(img_name)
        print(f"QR code generated successfully as {img_name}")
        
#main function
def main():
    #Greet user
    print('Hello!')

#----------------------------------------------
main()