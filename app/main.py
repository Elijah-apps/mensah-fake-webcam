import cv2
import pyvirtualcam
from PySide6.QtWidgets import QApplication
from .gui import VideoSelector

def start_virtual_cam():
    app = QApplication([])
    video_selector = VideoSelector()
    video_selector.show()
    app.exec()

if __name__ == "__main__":
    start_virtual_cam()