from machine import Pin, I2C
import ssd1306
import time

# Setup I2C
# Pin assignments may need to be adjusted depending on your specific wiring
i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)

# Initialize OLED Display
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Clear the display
oled.fill(0)

# Display "Hello World"
oled.text('Hello World', 12, 25)
oled.show()                                                                                                                    