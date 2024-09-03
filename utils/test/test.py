# Importing dataset from Roboflow
from roboflow import Roboflow

rf = Roboflow(api_key="h0LatO6wKxgJUq5K6HTI")
project = rf.workspace("tanay-bs8l1").project("adobe-gamesense")
version = project.version(1)
dataset = version.download("yolov8")

# Removing player data from the dataset
import os

for i in ["train","valid","test"]:
    # Define the paths to the directories
    labels_dir = f'Adobe-GameSense-1/{i}/labels'
    images_dir = f'Adobe-GameSense-1/{i}/images'

    # Debug path existence
    if not os.path.exists(labels_dir):
        print(f"The path {labels_dir} does not exist.")
    if not os.path.exists(images_dir):
        print(f"The path {images_dir} does not exist.")

    # Iterate over all the files in the labels directory
    for filename in os.listdir(labels_dir):
        # Only process .txt files
        if filename.endswith('.txt'):
            filepath = os.path.join(labels_dir, filename)
            image_filepath = os.path.join(images_dir, filename.replace('.txt', '.jpg'))  # Assuming .jpg extension for images

            # Read the annotation file
            with open(filepath, 'r') as file:
                lines = file.readlines()

            # Process the lines
            new_lines = []
            for line in lines:
                elements = line.strip().split()
                if len(elements) != 5:
                    print(f"Invalid number of coordinates: {len(elements)} in file {filepath}")
                    continue  # Skip this line

                label = int(elements[0])
                if label not in [0, 1]:
                    continue  # Skip if label is not 0 or 1

                # Replace label 1 with 0
                if label == 1:
                    new_lines.append(f"0 {' '.join(elements[1:])}\n")

            # Write the new content to the file if it's not empty
            if new_lines:
                with open(filepath, 'w') as file:
                    file.writelines(new_lines)
            else:
                # If file is empty after processing, delete the file and the corresponding image
                os.remove(filepath)
                print(f"Deleted file: {filepath}")
                if os.path.exists(image_filepath):
                    os.remove(image_filepath)
                    print(f"Deleted image: {image_filepath}")


    # Preprocessing the images cropping and intensity thresholding
    import cv2
    import numpy as np
    import os

    # Define the paths
    source_dir = f"Adobe-GameSense-1/{i}/images"
    dest_dir = f"Adobe-GameSense-1/{i}/preprocess_images"

    # Create destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Process each image in the source directory
    for filename in os.listdir(source_dir):
        image_path = os.path.join(source_dir, filename)

        if not os.path.isfile(image_path):
            continue

        # Read and process the image
        image = cv2.imread(image_path)

        if image is None:
            print(f"Error: Image {filename} not loaded properly.")
            continue

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)
        black_mask = cv2.bitwise_not(mask)
        black_image = np.zeros_like(image)
        colored_foreground = cv2.bitwise_and(image, image, mask=mask)
        black_background = cv2.bitwise_and(black_image, black_image, mask=black_mask)
        final_image = cv2.add(colored_foreground, black_background)

        crop_top = 100
        crop_bottom = 0
        crop_left = 200
        crop_right = 200

        h, w, _ = final_image.shape
        final_image_cropped = final_image[crop_top:h-crop_bottom, crop_left:w-crop_right]

        final_image_rgb = cv2.cvtColor(final_image_cropped, cv2.COLOR_BGR2RGB)

        # Save the processed image
        dest_path = os.path.join(dest_dir, filename)
        cv2.imwrite(dest_path, cv2.cvtColor(final_image_rgb, cv2.COLOR_RGB2BGR))

        print(f"Processed and saved: {filename}")

    print("All images processed and saved.")

'''
!pip install -q git+https://github.com/THU-MIG/yolov10.git

!mkdir -p {HOME}/weights
!wget -P {HOME}/weights -q https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10n.pt
# !wget -P {HOME}/weights -q https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10s.pt
# !wget -P {HOME}/weights -q https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10m.pt
# !wget -P {HOME}/weights -q https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10b.pt
# !wget -P {HOME}/weights -q https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10x.pt
# !wget -P {HOME}/weights -q https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10l.pt
!ls -lh {HOME}/weights


!yolo task=detect mode=train epochs=100 batch=1 plots=True model=weights/yolov10n.pt data=Adobe-GameSense-1/data.yaml
'''