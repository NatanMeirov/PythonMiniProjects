# Imports
import sys
import os
try:
    from PIL import Image
except ImportError:
    print("Please make sure to install Pillow library first: use 'pip install Pillow' command")
    sys.exit()


# Validations
try:
    if len(sys.argv) < 3:
        raise IOError(f"Arguments Error - not enough arguments or too much arguments:\n{sys.argv[0]} [dir path to process] [dir path to store the output (new or exist dir)]")
    if len(sys.argv) > 3:
        raise IOError(f"Arguments Error - too much arguments:\n{sys.argv[0]} [dir path to process] [dir path to store the output (new or exist dir)]")

    images_folder = sys.argv[1]
    new_or_exist_folder = sys.argv[2]

    if not os.path.isdir(images_folder):
        raise NotADirectoryError(f"Argument Type Error: {images_folder} is not a directory")

    if not os.path.exists(new_or_exist_folder):
        os.mkdir(new_or_exist_folder)
    elif not os.path.isdir(new_or_exist_folder):
        raise NotADirectoryError(f"Argument Type Error: {new_or_exist_folder} is not a directory")

    if not images_folder.endswith("\\"):
        images_folder = images_folder + "\\"

    if not new_or_exist_folder.endswith("\\"):
        new_or_exist_folder = new_or_exist_folder + "\\"

except NotADirectoryError as e:
    print(e)
    sys.exit()
except IOError as e:
    print(e)
    sys.exit()


# Processing
print("Converting...")

for filename in os.listdir(images_folder):
    if filename.split(".")[1] != "jpg":
        continue

    complete_input_path = images_folder + filename

    new_formatted_filename = filename.split(".")[0] + ".png" # Grabs the image name without the .jpg suffix and added .png
    complete_output_path = new_or_exist_folder + new_formatted_filename

    image = Image.open(complete_input_path)
    image.save(complete_output_path, "png")

print("Images Converted Successfully")