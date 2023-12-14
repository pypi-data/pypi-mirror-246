import cv2
import paddlehub as hub

# 根据自己喜好选择风格：
## 今敏:'animegan_v2_paprika_98'
## 新海诚:'animegan_v2_shinkai_53'
## 宫崎骏:'animegan_v2_hayao_99'

def apply_style_transfer(input_image_path, output_image_path, model_name="animegan_v2_hayao_99", use_gpu=False):
    # 加载 PaddleHub 模型
    model = hub.Module(name=model_name, use_gpu=use_gpu)

    # 读取输入图像
    input_image = cv2.imread(input_image_path)

    # 应用图像样式迁移
    stylized_image = model.style_transfer(images=[input_image])[0]

    # 保存样式化图像
    cv2.imwrite(output_image_path, stylized_image)