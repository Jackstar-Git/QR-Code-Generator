import qrcode
import colorama
from PIL import Image
import os
import platform
from subprocess import Popen

colorama.init(autoreset=True)
color = colorama.Fore

code = qrcode.QRCode()
img = None

data = ""

while not data:
    data = input("Please paste your data here (Press \"q\" to quit): ")
    if data == "q":
        exit(0)
    if not data:
        print("-" * 50)
        print(color.RED + "Error: You data cannot be empty, please try again or press \"q\" to quit!")
        print("-" * 50)
        continue

    code.add_data(data)
    break

error_level = ""
while not error_level:
    error_level = input(
        "Please enter the level of error correction you want! Levels are: L-Low, M-Medium (default), and H-High! (Press \"q\" to quit´or \"Enter\" to continue with default settings): ")
    if error_level == "q":
        exit(0)
    if error_level.lower() not in ["l", "m", "h", ""]:
        print("-" * 50)
        print(
            color.RED + "Error: You error level must be one of these options: L, M or H! Press \"Enter\" to continue with default settings. Please try again or press \"q\" to quit!")
        print("-" * 50)
        error_level = False
        continue

    match error_level.lower():
        case "l":
            code.error_correction = qrcode.ERROR_CORRECT_L
        case "m":
            code.error_correction = qrcode.ERROR_CORRECT_M
        case "h":
            code.error_correction = qrcode.ERROR_CORRECT_H
        case _:
            code.error_correction = qrcode.ERROR_CORRECT_M
    code.make(fit=True)

    img = code.make_image(fill_color="black", back_color="white")

    print("-" * 50)
    print(color.LIGHTGREEN_EX + f"Successfully created your QR-Code!")
    print("-" * 50)
    break

save = ""
while not save:
    save = input("Do you want to save the image (\"y\" for yes, \"n\" for no): ")
    if save.lower() not in ["y", "n"]:
        print("-" * 50)
        print(color.RED + f"Error: Your answer must be \"y\" for yes or \"n\" for no, not {save}! Please try again")
        print("-" * 50)

match save.lower():
    case "n":
        img.save("qr-code.png")
        Image.open("qr-code.png").show()
        os.remove("qr-code.png")
    case "y":
        path = ""
        while not path:
            path = input(
                "Please enter the path where your image should be stored! (Hit \"Enter\" to quit without saving!): ")
            if not path:
                exit(0)

            if not os.path.exists(path):
                print("-" * 50)
                print(color.RED + f"Error: The following path doesn't exist: {path}! Please try again")
                print("-" * 50)
                continue
            else:
                img.save(os.path.join(path, "qr-code.png"))
                if platform.system() == "Windows":
                    os.startfile(path)
                elif platform.system() == "Darwin":
                    Popen(["open", path])
                else:
                    Popen(["xdg-open", path])
