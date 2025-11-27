import nuke
import json
import urllib.request
from PySide6 import QtWidgets, QtGui, QtCore
import cv2
from functools import partial

API_URL = "https://backend.actionvfx.com/api/v1/collections/18367/products"


class VideoThumbnailViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(VideoThumbnailViewer, self).__init__(parent)
        self.setWindowTitle("ActionVFX Viewer (Demo Público)")
        self.setMinimumSize(640, 480)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.image_label = QtWidgets.QLabel("Cargando…")
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.thumbnail_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.thumbnail_layout)

        # Controles de reproducción
        controls = QtWidgets.QHBoxLayout()
        self.play_btn = QtWidgets.QPushButton("Play")
        self.pause_btn = QtWidgets.QPushButton("Pause")
        self.stop_btn = QtWidgets.QPushButton("Stop")
        self.play_btn.clicked.connect(self.play_video)
        self.pause_btn.clicked.connect(self.pause_video)
        self.stop_btn.clicked.connect(self.stop_video)
        controls.addWidget(self.play_btn)
        controls.addWidget(self.pause_btn)
        controls.addWidget(self.stop_btn)
        self.layout.addLayout(controls)

        self.current_video_url = None
        self.cap = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.play_video_frame)

        self.load_data()

    def load_data(self):
        try:
            request = urllib.request.Request(
                API_URL,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            with urllib.request.urlopen(request) as response:
                raw = response.read().decode()
                self.data = json.loads(raw)
                self.build_ui()

        except Exception as e:
            self.image_label.setText(f"Error al cargar datos:\n{e}")

    def build_ui(self):
        for item in self.data[:9]:
            poster_url = item["poster"]
            video_poster = item["video"]["poster"]
            video_url = next(
                (s["src"] for s in item["video"]["sources"]
                 if s["type"] == "video/mp4" and s["size"] == "medium"),
                None
            )

            btn = QtWidgets.QPushButton()
            btn.setFixedSize(100, 60)
            btn.setIconSize(QtCore.QSize(100, 60))
            btn.setToolTip(item["name"])
            btn.clicked.connect(partial(self.load_image, video_poster, video_url))

            try:
                thumb_request = urllib.request.Request(
                    poster_url,
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                with urllib.request.urlopen(thumb_request) as thumb_resp:
                    thumb_data = thumb_resp.read()
                    image = QtGui.QImage()
                    image.loadFromData(thumb_data)
                    btn.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(image)))
            except Exception as e:
                print(f"Error cargando thumbnail: {e}")

            self.thumbnail_layout.addWidget(btn)

        # Mostrar primer elemento
        if self.data:
            first_poster = self.data[0]["video"]["poster"]
            first_video = next(
                (s["src"] for s in self.data[0]["video"]["sources"]
                 if s["type"] == "video/mp4" and s["size"] == "medium"),
                None
            )
            self.load_image(first_poster, first_video)

    def load_image(self, poster_url, video_url):
        self.current_video_url = video_url
        try:
            request = urllib.request.Request(
                poster_url,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(request) as response:
                data = response.read()
                image = QtGui.QImage()
                image.loadFromData(data)
                pixmap = QtGui.QPixmap.fromImage(image)
                self.image_label.setPixmap(
                    pixmap.scaled(
                        self.image_label.size(),
                        QtCore.Qt.KeepAspectRatio,
                        QtCore.Qt.SmoothTransformation
                    )
                )
        except Exception as e:
            self.image_label.setText(f"Error al cargar imagen:\n{e}")

    def play_video(self):
        if self.current_video_url:
            self.stop_video()
            self.cap = cv2.VideoCapture(self.current_video_url)
            self.timer.start(24)

    def pause_video(self):
        self.timer.stop()

    def stop_video(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None

    def play_video_frame(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                image = QtGui.QImage(frame.data, w, h, bytes_per_line,
                                     QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(image)
                self.image_label.setPixmap(
                    pixmap.scaled(
                        self.image_label.size(),
                        QtCore.Qt.KeepAspectRatio,
                        QtCore.Qt.SmoothTransformation
                    )
                )
            else:
                self.stop_video()


# Mostrar ventana
viewer = VideoThumbnailViewer()
viewer.show()
