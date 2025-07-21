import qrcode

image = qrcode.make("http://127.0.0.1:8000")
image.save("qrcode.png")