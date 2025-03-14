import time
import cv2
from PySide6.QtCore import QObject, Property, Signal, QBuffer, QIODevice
from PySide6.QtGui import QImage
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "cardvault"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class CardVault(QObject):
    image_changed = Signal()

    def __init__(self):
        super().__init__()

        self._image_files = [
            {"text": "Cards 1", "value": "cards1.jpg"},
            {"text": "Cards 2", "value": "cards2.webp"},
            {"text": "Cards 3", "value": "cards3.jpg"},
        ]

        self._display_modes = [
            {"text": "Original", "value": "original"},
            {"text": "Threshold", "value": "threshold"},
        ]

        self._epsilon_factors = [
            {"text": "0.1", "value": 0.1},
            {"text": "0.01", "value": 0.01},
            {"text": "0.001", "value": 0.001}
        ]

        self._selected_image = "cards2.webp"
        self._contoured = False
        self._display_mode = "original"
        self._auto_threshold = False
        self._threshold = 127
        self._epsilon_factor = 0.01
        self._min_sides = 0
        self._max_sides = 10
        self._min_area = 100
        self._image = ""

        self._process_image()

    @staticmethod
    def _convert_cv_to_qimage(cv_image):
        height, width, _ = cv_image.shape
        bytes_per_line = 3 * width
        
        return QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

    @staticmethod
    def _qimage_to_base64(qimage):
        buffer = QBuffer()
        buffer.open(QIODevice.WriteOnly)

        qimage.save(buffer, "PNG")
        base64_data = bytes(buffer.data().toBase64()).decode()

        buffer.close()
        
        return f"data:image/png;base64,{base64_data}"

    def _process_image(self):
        if not self._selected_image:
            return

        img = cv2.imread(self._selected_image)

        frame_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        frame_blur = cv2.GaussianBlur(frame_gray, (5, 5), 0)

        _, threshold = cv2.threshold(frame_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) if self.auto_threshold else cv2.threshold(frame_blur, self._threshold, 255, cv2.THRESH_BINARY)

        output = cv2.cvtColor(threshold, cv2.COLOR_GRAY2BGR) if self._display_mode == "threshold" else img.copy()

        if self._contoured:
            contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            for contour in contours[1:]:
                approx = cv2.approxPolyDP(contour, self._epsilon_factor * cv2.arcLength(contour, True), True)
                if len(approx) < self._min_sides or len(approx) > self._max_sides or cv2.contourArea(approx) < self._min_area:
                    continue

                cv2.drawContours(output, [approx], 0, (0, 0, 255), 4)

        qimage = self._convert_cv_to_qimage(output)
        self._image = self._qimage_to_base64(qimage)

        self.image_changed.emit()

    @Property(list, constant=True)
    def image_files(self):
        return self._image_files
    
    @Property(list, constant=True)
    def display_modes(self):
        return self._display_modes
    
    @Property(list, constant=True)
    def epsilon_factors(self):
        return self._epsilon_factors
    
    @Property(str, notify=image_changed)
    def image(self):
        return self._image + "?" + str(int(time.time())) if self._image else ""
    
    @Property(str)
    def selected_image(self):
        return self._selected_image
    
    @selected_image.setter
    def selected_image(self, value):
        if self._selected_image == value:
            return
        
        self._selected_image = value
        self._process_image()
    
    @Property(str)
    def display_mode(self):
        return self._display_mode
    
    @display_mode.setter
    def display_mode(self, value):
        if self._display_mode == value:
            return
        
        self._display_mode = value
        self._process_image()

    @Property(bool)
    def contoured(self):
        return self._contoured
    
    @contoured.setter
    def contoured(self, value):
        self._contoured = value
        self._process_image()

    @Property(bool)
    def auto_threshold(self):
        return self._auto_threshold
    
    @auto_threshold.setter
    def auto_threshold(self, value):
        self._auto_threshold = value
        self._process_image()

    @Property(int)
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        if self._threshold == value:
            return
        
        self._threshold = value
        self._process_image()

    @Property(float)
    def epsilon_factor(self):
        return self._epsilon_factor
    
    @epsilon_factor.setter
    def epsilon_factor(self, value):
        if self._epsilon_factor == value:
            return
        
        self._epsilon_factor = value
        self._process_image()

    @Property(int)
    def min_sides(self):
        return self._min_sides
    
    @min_sides.setter
    def min_sides(self, value):
        if self._min_sides == value:
            return
        
        self._min_sides = value
        self._process_image()

    @Property(int)
    def max_sides(self):
        return self._max_sides
    
    @max_sides.setter
    def max_sides(self, value):
        if self._max_sides == value:
            return
        
        self._max_sides = value
        self._process_image()

    @Property(int)
    def min_area(self):
        return self._min_area
    
    @min_area.setter
    def min_area(self, value):
        if self._min_area == value:
            return
        
        self._min_area = value
        self._process_image()