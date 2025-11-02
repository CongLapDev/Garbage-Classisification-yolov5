import cv2
import torch
import gui
import text_to_speech

# Đường dẫn đến model YOLOv5 và file weights đã được training
path_to_model = './yolov5'
path_to_train = 'yolov5/runs/train/exp40epoch/weights/best_fix.pt'

# Tải model YOLOv5 đã được training với weights tùy chỉnh
model = torch.hub.load(path_to_model, 'custom', path = path_to_train, source='local', force_reload=True)

def detect(file_path):
    # Hàm phát hiện và phân loại rác từ ảnh
    # Đọc ảnh và chuyển đổi màu
    img = cv2.imread(file_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Thực hiện phát hiện đối tượng
    result = model(img)

    # Hiển thị kết quả
    result.show()
    ids = str(result)

    # Phân loại và thông báo bằng giọng nói
    if 'metal' in ids:
        text = 'This is metal, please throw it into trash can with label metal'
        text_to_speech.speak(text)
    elif 'glass' in ids:
        text = 'This is glass, please throw it into trash can with label glass'
        text_to_speech.speak(text)
    elif 'cardboard' in ids:
        text = 'This is cardboard, please throw it into trash can with label cardboard'
        text_to_speech.speak(text)
    elif 'paper' in ids:
        text = 'This is paper, please throw it into trash can with label paper'
        text_to_speech.speak(text)
    elif 'trash' in ids:
        text = "This is can not recycle, please throw it into the red trash can"
        text_to_speech.speak(text)
    elif 'plastic' in ids:
        text = "This is plastic, please throw it into trash can with label plastic"
        text_to_speech.speak(text)
        





