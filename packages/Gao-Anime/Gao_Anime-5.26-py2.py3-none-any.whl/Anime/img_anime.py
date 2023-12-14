import cv2
import paddlehub as hub

def img2img(input_image_path, output_image_path, model):
    # Read the input image
    input_image = cv2.imread(input_image_path)

    # Apply style transfer
    stylized_image = model.style_transfer(images=[input_image])[0]

    # Save the stylized image
    cv2.imwrite(output_image_path, stylized_image)

# Example usage:
# Specify the input and output paths
input_image_path = 'hyc.jpg'
output_image_path = 'hyc_trans_gong.jpg'

# Specify the PaddleHub model
model_name = 'animegan_v2_hayao_99'
model = hub.Module(name=model_name, use_gpu=False)

# Apply style transfer to a single image
img2img(input_image_path, output_image_path, model)
