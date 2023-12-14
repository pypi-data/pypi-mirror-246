import cv2
import paddlehub as hub

def apply_style_transfer(input_image_path, output_image_path, model_name, use_gpu=False):
    # 加载 PaddleHub 模型
    model = hub.Module(name=model_name, use_gpu=use_gpu)

    # 读取输入图像
    input_image = cv2.imread(input_image_path)

    # 应用图像样式迁移
    stylized_image = model.style_transfer(images=[input_image])[0]

    # 保存样式化图像
    cv2.imwrite(output_image_path, stylized_image)