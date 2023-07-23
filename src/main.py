#!/usr/bin/env python
"""
This demo can be ran from the project root directory via:
```sh
python src/main.py
```
It can also be ran via p4a/buildozer.
"""
from kivy.app import App
from pyzbar.pyzbar import ZBarSymbol
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from src.kivy_garden.zbarcam.zbarcam import ZBarCam


DEMO_APP_KV_LANG = """
#:import ZBarCam kivy_garden.zbarcam.ZBarCam
#:import ZBarSymbol pyzbar.pyzbar.ZBarSymbol
BoxLayout:
    orientation: 'vertical'
    ZBarCam:
        id: zbarcam
        # optional, by default checks all types
        code_types: ZBarSymbol.QRCODE, ZBarSymbol.EAN13
    Label:
        size_hint: None, None
        size: self.texture_size[0], 50
        text: ', '.join([str(symbol.data) for symbol in zbarcam.symbols])
"""


class DemoApp(App):

    def build(self):

        # layout = BoxLayout(orientation="vertical")
        cam = ZBarCam(code_types=(ZBarSymbol.QRCODE, ZBarSymbol.EAN13))
        # layout.add_widget(cam)
        #
        # label = Label()
        # label.size = 5, 5
        #  label.text = 'hey' + ', '.join([str(symbol.data) for symbol in cam.symbols])
        #
        # layout.add_widget(label)
        #
        return cam

        # print(', '.join([str(symbol.data) for symbol in cam.symbols]))
        # return Builder.load_string(DEMO_APP_KV_LANG)


if __name__ == '__main__':
    DemoApp().run()
