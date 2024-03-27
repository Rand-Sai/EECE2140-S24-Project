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
    def generate_qr_code(self, url, name1=None):
        self.qr.clear()
        self.qr.add_data(url)
        self.qr.make(fit=True)

        
        # Create an image from the QR Code instance
        img = self.qr.make_image(fill_color="black", back_color="white")

        # Save the image with a name based on the URL
        if name1 == None:
            img_name = url.replace("://", "_").replace("/", "_") + ".png"
        else:
            img_name = str(name1) + ".png"
        img.save(img_name)
        print(f"QR code generated successfully as {img_name}")
        
#main function
def main():
    #Greet user
    print('Hello!\n')
    url1 = input("Enter the url of the website or any text: \n")
    name1 = input("Enter the name of this QRcode image or leave blank: \n")
    QRG = QRCodeGenerator()
    QRG.generate_qr_code(url1, name1)
#----------------------------------------------
main()