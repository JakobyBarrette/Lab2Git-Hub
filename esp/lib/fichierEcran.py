import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

class Ecran:

    def __init__(self):
        displayio.release_displays()
        self.i2c = board.I2C()
        self.display_bus = displayio.I2CDisplay(self.i2c, device_address=0x3C)
        self.display = adafruit_displayio_ssd1306.SSD1306(self.display_bus, width=128, height=64, rotation=180)
        self.splash = displayio.Group()
        self.display.root_group = self.splash

        self.text = ""
        self.text_area = label.Label(terminalio.FONT, text=self.text, color=0xFFFFFF, x=5, y=10)
        self.splash.append(self.text_area)

    def rafraichir_texte(self, texte):
        self.text_area.text = texte
        self.display.refresh()

    @property
    def texte(self):
        return self.text_area.text