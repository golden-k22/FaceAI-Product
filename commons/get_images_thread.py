import pathlib

from PyQt5.QtCore import QThread, pyqtSignal

from commons.common import Common


class GetImagesThread(QThread):
    finished_get_images_signal = pyqtSignal(object)

    def __init__(self, faceai, urls, parent=None):
        super().__init__(parent=parent)
        self.urls = urls
        self.image_urls = []
        self.faceai = faceai
        self.direct = ""
        self.is_direct = False
        self.is_urls = False

    def run(self):
        if self.is_urls:
            self.get_images_from_urls()
        if self.is_direct:
            self.get_images_from_folder_path()
        self.finished_get_images_signal.emit(self.image_urls)

    def get_images_from_urls(self):
        for url in self.urls:
            if self.faceai.is_face(url):
                url = Common.resize_image(url, 500)
                self.image_urls.append(url)

    def get_images_from_folder_path(self):
        desktop = pathlib.Path(self.direct)
        for url in desktop.glob(r'**/*'):
            if Common.EXTENSIONS.count(url.suffix):
                if self.faceai.is_face(url):
                    url = Common.resize_image(url.__str__(), 500)
                    self.image_urls.append(url)
