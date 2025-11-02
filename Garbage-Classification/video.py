import sys
from pathlib import Path

# Đường dẫn đến model và weights đã được training (mặc định)
DEFAULT_WEIGHTS = 'yolov5/runs/train/exp40epoch/weights/best_fix.pt'

def run_webcam(weights: str = None, source: str = '0', view_img: bool = True):
    """
    Chạy phát hiện từ webcam sử dụng yolov5/detect.py

    Tham số:
        weights: đường dẫn tới file weights (nếu None sẽ dùng DEFAULT_WEIGHTS)
        source: nguồn đầu vào ('0' cho webcam mặc định)
        view_img: True để hiển thị cửa sổ kết quả

    Lưu ý: Nhấn 'q' để dừng camera và đóng cửa sổ
    """
    try:
        # Thêm thư mục gốc vào sys.path để import yolov5
        project_root = Path(__file__).resolve().parents[0]
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        # Import và sử dụng yolov5.detect
        from yolov5.detect import run

        # Sử dụng weights được chỉ định hoặc mặc định
        weights_path = weights if weights is not None else DEFAULT_WEIGHTS

        # Gọi hàm run từ detect.py với các tham số phù hợp
        run(weights=weights_path, 
            source=source,
            conf_thres=0.45,
            view_img=view_img,
            nosave=True)  # Không lưu kết quả

    except Exception as e:
        print(f"Lỗi khi chạy camera: {e}")
        raise

if __name__ == '__main__':
    # Khi chạy trực tiếp file này, khởi chạy webcam
    run_webcam()