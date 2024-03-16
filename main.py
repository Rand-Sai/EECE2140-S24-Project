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
        
#main function
def main():
    #Greet user
    print('Hello!')

#----------------------------------------------
main()