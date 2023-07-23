import os
import winsound

from collections import namedtuple
from PIL import ImageOps
from PIL import Image
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.utils import platform
from kivy.uix.anchorlayout import AnchorLayout
from pyzbar import pyzbar
from pyzbar.pyzbar import ZBarSymbol

MODULE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


class ZBarCam(AnchorLayout, App):

    """the resolution of the camera"""
    resolution = ListProperty([640, 480])

    symbols = ListProperty([])
    symbol = namedtuple("symbol", ["type", "data"])

    """the qr or barcode types. Default is all types"""
    code_types = ListProperty(set(pyzbar.ZBarSymbol))

    @property
    def xcamera(self):
        return self.ids["xcamera"]

    def __init__(self, **kwargs):

        Builder.load_file(os.path.join(MODULE_DIRECTORY, "zbarcam.kv"))
        # self.xcamera = xcamera

        super().__init__(**kwargs)

        Clock.schedule_once(lambda dt: self._setup())

    def _setup(self):
        """remove the shoot button"""
        self._remove_shoot_button()

        """bind camera to event"""
        self.xcamera.bind(on_camera_ready=self._on_camera_ready)

        """camera may be ready before bind"""
        if self.xcamera._camera is not None:
            self._on_camera_ready(self.xcamera)

    def _on_camera_ready(self, xcamera):
        """binds when xcamera._camera instance is ready"""
        xcamera._camera.bind(on_texture=self._on_texture)

    def _on_texture(self, instance):
        """store symbols in symbols property"""
        self.symbols = self._detect_qrcode_frame(texture=instance.texture, code_types=self.code_types)

    @classmethod
    def _detect_qrcode_frame(cls, texture, code_types):

        image_data = texture.pixels
        size = texture.size

        pil_image = Image.frombytes(
            mode="RGBA",
            size=size,
            data=image_data
        )

        pil_image = cls._fix_android_image(cls, pil_image)
        symbols = []
        codes = pyzbar.decode(pil_image, symbols=code_types)

        for code in codes:
            symbol = ZBarCam.symbol(type=code.type, data=code.data)
            symbols.append(symbol)

        if len(symbols) != 0:
            winsound.Beep(2500, 500)
            print(symbols)
            return symbols

        return symbols

    def _remove_shoot_button(self):
        """removes the shoot button"""
        xcamera = self.xcamera
        shoot_button = xcamera.children[0]
        xcamera.remove_widget(shoot_button)

    @staticmethod
    def _is_android():
        return platform == "android"

    @staticmethod
    def _is_ios():
        return platform == "ios"

    def _fix_android_image(self, pil_image):
        """fix mirrored android image"""
        if not self._is_android():
            return pil_image

        """rotate 90"""
        pil_image = pil_image.rotate(90)
        pil_image = ImageOps.mirror(pil_image)
        return pil_image

    def start(self):
        self.xcamera.play = True

    def stop(self):
        self.xcamera.play = False

    # def build(self):
    #
    #     """construct a layout and return the layout"""
    #     layout = CameraScanner(code_types=(ZBarSymbol.QRCODE, ZBarSymbol.EAN13))
    #     return layout


if __name__ == "__main__":
    app = ZBarCam()
    app.run()
