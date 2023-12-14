import cv2
import paddlehub as hub
import os

# 根据自己喜好选择风格：
## 今敏:'animegan_v2_paprika_98'
## 新海诚:'animegan_v2_shinkai_53'
## 宫崎骏:'animegan_v2_hayao_99'

def apply_style_transfer(input_image_path, output_image_path="", model_id="1", use_gpu=False):
    if model_id=='1':
        print(f'正在进行宫崎骏风格的转化,   是否正在使用GPU：{use_gpu}')
        model_name ='animegan_v2_hayao_99'
    if model_id=='2':
        print(f'正在进行新海诚风格的转化,   是否正在使用GPU：{use_gpu}')
        model_name ='animegan_v2_shinkai_53'
    if model_id=='3':
        print(f'正在进行今敏风格的转化,     是否正在使用GPU：{use_gpu}')
        model_name ='animegan_v2_paprika_98'

        # 加载 PaddleHub 模型
    model = hub.Module(name=model_name, use_gpu=use_gpu)

    # 读取输入图像
    input_image = cv2.imread(input_image_path)

    # 应用图像样式迁移
    stylized_image = model.style_transfer(images=[input_image])[0]

    # 生成保存路径：
    if output_image_path=="":
        file_name_without_extension = os.path.splitext(os.path.basename(input_image_path))[0]
        output_image_path = file_name_without_extension + "_transfer.jpg"

    # 保存样式化图像
    cv2.imwrite(output_image_path, stylized_image)
    print(f'转换完成！！！！路径：{output_image_path}')