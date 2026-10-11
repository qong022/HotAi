from PIL import Image

try:
    img = Image.open("logo.png.png")
    img.save("icon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("SUCCESS! 'icon.ico' generated successfully.")
except Exception as e:
    print("ERROR! Image failed to load. Ensure 'logo.png' is at C:\\Users\\ASP-AJFM-PDP-EG\\HotAi. Details:", e)