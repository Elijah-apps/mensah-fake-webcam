import cv2
import pyvirtualcam
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel
from PySide6.QtCore import Qt, QThread, Signal

class VideoThread(QThread):
    frame_ready = Signal(object)

    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path
        self.running = True

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        with pyvirtualcam.Camera(width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                 height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                                 fps=int(cap.get(cv2.CAP_PROP_FPS))) as cam:
            while self.running:
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frame_ready.emit(frame)
                cam.send(frame)
                cam.sleep_until_next_frame()
        cap.release()

    def stop(self):
        self.running = False
        self.wait()


class VideoSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Virtual Webcam')
        self.setGeometry(100, 100, 300, 100)

        self.layout = QVBoxLayout()
        self.label = QLabel("Select a video file to use as webcam feed")
        self.label.setAlignment(Qt.AlignCenter)

        self.button = QPushButton('Select Video')
        self.button.clicked.connect(self.open_file_dialog)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.video_thread = None

    def open_file_dialog(self):
        video_path, _ = QFileDialog.getOpenFileName(self, "Select Video File", "", "Video Files (*.mp4 *.avi *.mov)")
        if video_path:
            self.start_video_feed(video_path)

    def start_video_feed(self, video_path):
        if self.video_thread is not None:
            self.video_thread.stop()
        self.video_thread = VideoThread(video_path)
        self.video_thread.frame_ready.connect(self.update_frame)
        self.video_thread.start()

    def update_frame(self, frame):
        # This function can be used to update a GUI element if necessary
        pass

    def closeEvent(self, event):
        if self.video_thread is not None:
            self.video_thread.stop()
        event.accept()
