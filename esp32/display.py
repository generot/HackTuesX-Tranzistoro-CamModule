from machine import SoftI2C, Pin
from ssd1306 import SSD1306_I2C

I2C_SCL = 14
I2C_SDA = 15

SIZE = (128, 64)

LN_COUNT = 0
SEPR_PX_Y = 15

def display_init():
    display_if = SoftI2C(scl=Pin(I2C_SCL), sda=Pin(I2C_SDA))
    display = SSD1306_I2C(*SIZE, display_if)
    
    return display

def flush():
    global LN_COUNT
    
    LN_COUNT = 0

def println(disp, s):
    global LN_COUNT
    
    disp.text(s, 0, LN_COUNT * SEPR_PX_Y)
    LN_COUNT += 1