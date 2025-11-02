import pyttsx3
from threading import Thread

def _speak_worker(text):
    """Worker chạy trong thread: tạo engine riêng, đọc, rồi stop."""
    engine = pyttsx3.init()
    try:
        voices = engine.getProperty('voices')
        # Chọn voice[1] nếu có, ngược lại voice[0]
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
        else:
            engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 160)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        # tránh crash nếu engine gặp lỗi
        print("TTS error:", e)
    finally:
        try:
            engine.stop()
        except Exception:
            pass

def speak(text): 
    """Gọi hàm này ở bất kỳ chỗ nào trong GUI. Nó sẽ chạy non-blocking."""
    Thread(target=_speak_worker, args=(text,), daemon=True).start()
