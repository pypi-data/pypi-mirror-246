import gradio as gr
from Anime.Anime import apply_style_transfer
from PIL import Image
import numpy as np


def style_transfer_interface(input_image, model_id, use_gpu):
    try:
        # Convert Gradio input image to a NumPy array
        input_array = np.array(input_image)

        # Save the input image to a temporary file using Pillow
        temp_input_path = "temp_input_image.jpg"
        Image.fromarray(input_array).save(temp_input_path)

        # Specify the output image path
        output_image_path = "output_image.jpg"

        # Apply style transfer using the temporary input file
        apply_style_transfer(temp_input_path, output_image_path, model_id=model_id, use_gpu=use_gpu)

        # Return the path to the stylized image
        return output_image_path
    except Exception as e:
        print(f"Error during style transfer: {e}")
        raise


iface = gr.Interface(
    fn=style_transfer_interface,
    inputs=[
        gr.Image(type="pil", label="输入图像"),
        gr.Dropdown(choices=["1", "2", "3"], label="选择模型"),
        gr.Dropdown(choices=['True','False'], label="是否使用GPU"),
    ],
    outputs=gr.Image(type="pil", label="风格化图像"),
    live=False,
)

iface.launch()
