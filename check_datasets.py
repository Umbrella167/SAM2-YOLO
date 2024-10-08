import os
import cv2

def draw_bounding_boxes(image_dir, label_dir, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through all label files
    for label_file in os.listdir(label_dir):
        # Construct the full path to the label file
        label_path = os.path.join(label_dir, label_file)
        
        # Construct the corresponding image file path
        image_file = label_file.replace('.txt', '.jpg')
        image_path = os.path.join(image_dir, image_file)
        
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Warning: Image {image_file} not found.")
            continue
        
        # Read the labels
        with open(label_path, 'r') as file:
            labels = file.readlines()
        
        # Draw each bounding box on the image
        for label in labels:
            data = label.strip().split()
            obj_id = int(data[0])
            x, y, w, h = map(float, data[1:])

            # Convert YOLO format (x_center, y_center, width, height) to bounding box (x1, y1, x2, y2)
            img_h, img_w, _ = image.shape
            x1 = int((x - w / 2) * img_w)
            y1 = int((y - h / 2) * img_h)
            x2 = int((x + w / 2) * img_w)
            y2 = int((y + h / 2) * img_h)

            # Draw the rectangle
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Optionally, put the object ID on the bounding box
            cv2.putText(image, str(obj_id), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Save the image with bounding boxes
        output_path = os.path.join(output_dir, image_file)
        cv2.imwrite(output_path, image)

# Example usage
image_directory = 'datasets/images/train'  # Path to the directory containing train images
label_directory = 'datasets/labels/train'  # Path to the directory containing train labels
output_directory = 'datasets/visualized/train'  # Path to save the visualized images

draw_bounding_boxes(image_directory, label_directory, output_directory)