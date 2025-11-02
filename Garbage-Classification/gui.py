import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import text_to_speech
from PIL import Image, ImageTk
import image

# Hướng dẫn (hiển thị bằng tiếng Anh)
userGuide = "Welcome to our waste classification system. Please leave trash in front of the screen."

# Màu nền mong muốn cho các khoảng trống
BG_COLOR = "#8bf7b6"

class GarbageGUI:
    """
    Giao diện chính cho ứng dụng phân loại rác thải.
    - Lớp này tạo cửa sổ chính, vùng xem trước ảnh, các nút hành động và thanh trạng thái.
    - Các nhãn/tiêu đề hiển thị bằng tiếng Anh (theo yêu cầu); các chú thích trong mã
      (docstrings/comments) viết bằng tiếng Việt để hỗ trợ người phát triển.
    """

    def __init__(self, root):
        #Khởi tạo cửa sổ chính.

        self.root = root
        self.root.title("Smart Garbage Classification")
        self.root.geometry("600x420")
        # Thiết lập màu nền chính cho cửa sổ
        self.root.configure(bg=BG_COLOR)

        self.create_widgets()

    def create_widgets(self):
        #Tạo và cấu hình các widget của GUI.

        # Cấu hình style cho ttk 
        style = ttk.Style()
        try:
            style.configure('Main.TFrame', background=BG_COLOR)
            style.configure('Main.TLabel', background=BG_COLOR)
        except Exception:
            pass

        # Tiêu đề
        title = ttk.Label(self.root, text="Garbage Recognition & Classification System", font=("Helvetica", 15, "bold"), style='Main.TLabel')
        title.pack(pady=(10, 6))

        # Khung chính chứa preview và nút
        content_frame = ttk.Frame(self.root, style='Main.TFrame')
        content_frame.pack(pady=(0, 6), fill=tk.BOTH, expand=True)

        # Vùng xem trước
        self.preview_frame = ttk.Frame(content_frame, style='Main.TFrame')
        self.preview_frame.pack(pady=(0, 6))

        # Ảnh mặc định 
        try:
            img = Image.open("bg.png")
            img = img.resize((400, 280), Image.Resampling.LANCZOS)
            self.preview_image = ImageTk.PhotoImage(img)
        except Exception:
            img = Image.new('RGB', (400, 280), color=BG_COLOR)
            self.preview_image = ImageTk.PhotoImage(img)

        # Dùng tk.Label cho ảnh để bg được áp dụng chính xác
        self.image_label = tk.Label(self.preview_frame, image=self.preview_image, bg=BG_COLOR)
        self.image_label.pack()

        # Khung chứa nút (giữ cố định vị trí)
        button_frame = ttk.Frame(content_frame, style='Main.TFrame')
        button_frame.pack(pady=(4, 6))

        self.image_btn = ttk.Button(button_frame, text="Select Image", command=self.process_image, width=14)
        self.image_btn.pack(side=tk.LEFT, padx=6)

        self.video_btn = ttk.Button(button_frame, text="Camera Detection", command=self.process_video, width=16)
        self.video_btn.pack(side=tk.LEFT, padx=6)

        self.guide_btn = ttk.Button(button_frame, text="User Guide", command=self.show_guide, width=12)
        self.guide_btn.pack(side=tk.LEFT, padx=6)

        # Thanh tiến trình (hiển thị khi xử lý ảnh)
        self.progress = ttk.Progressbar(self.root, mode='indeterminate', length=220)

        # Thanh trạng thái (hiển thị dòng trạng thái ngắn)
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self.root, textvariable=self.status_var, style='Main.TLabel', anchor='w')
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def process_image(self):
        """Mở hộp thoại chọn ảnh và gọi hàm detect.
        - Hàm này mở hộp thoại, cập nhật preview, chạy `image.detect(file_path)` và dừng progress.
        - `image.detect` tự lo phần hiển thị/âm thanh, nên GUI không cố gắng parse kết quả để show.
        """
        file_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if not file_path:
            return
        try:
            self.progress.pack(fill=tk.X, pady=5)
            self.progress.start()
            self.status_var.set("Processing image...")

            img = Image.open(file_path)
            img = img.resize((400, 300), Image.Resampling.LANCZOS)
            self.preview_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.preview_image)

            # Gọi hàm detect (image.detect tự xử lý hiển thị/âm thanh)
            image.detect(file_path)

            self.status_var.set("Ready")
        except Exception as e:
            messagebox.showerror("Error", f"Unable to process image: {e}")
        finally:
            try:
                self.progress.stop()
                self.progress.pack_forget()
            except Exception:
                pass

    def process_video(self):
        """Khởi chạy nhận diện từ camera trong luồng nền.
        - Để tránh khóa GUI, hàm này tạo một luồng nền và gọi `video.run_webcam()`.
        - `video.run_webcam()` gọi nội bộ `yolov5.detect.run` nên OpenCV sẽ mở cửa sổ
          riêng để hiển thị kết quả.
        """
        try:
            import video as video_module
            from threading import Thread

            def _run():
                try:
                    self.status_var.set("Camera detection running...")
                    video_module.run_webcam()
                    self.status_var.set("Ready")
                except Exception as e:
                    self.status_var.set("Camera error")
                    messagebox.showerror("Video Error", f"Unable to run camera: {e}")

            Thread(target=_run, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Import Error", f"Unable to import video module: {e}")

    def show_guide(self):
        # Phát hướng dẫn bằng giọng nói và hiển thị hộp thoại thông tin.
        text_to_speech.speak(userGuide)
        messagebox.showinfo("User Guide", userGuide)

def main():
    root = tk.Tk()
    app = GarbageGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
    