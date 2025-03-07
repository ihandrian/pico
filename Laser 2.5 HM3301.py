# Import necessary libraries
from machine import Pin, I2C
import ssd1306
import time

# I2C address for the HM3301 sensor
HM3301_I2C_ADDR = 0x40

# Initialize I2C communication
i2c0 = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)
#i2c1 = I2C(1, scl=Pin(7), sda=Pin(6), freq=100000)
"""
x = 128
y = 64
oled = ssd1306.SSD1306_I2C(x, y, i2c1)
"""
# Read PM2.5 and PM10.0 values from the sensor
def read_pm_values():
    i2c0.writeto(HM3301_I2C_ADDR, bytes([0x88]))  # Request data
    time.sleep_ms(100)  # Wait for data to be ready
    data = i2c0.readfrom(HM3301_I2C_ADDR, 29)  # Read 29 bytes of data
    pm2_5 = (data[3] << 8) | data[2]
    pm10_0 = (data[5] << 8) | data[4]
    return pm2_5, pm10_0

while True:
    pm2_5_value, pm10_0_value = read_pm_values()
    print(f"PM2.5: {pm2_5_value} µg/m³, PM10.0: {pm10_0_value} µg/m³")
    #oled.fill(0)
    #oled.text('PM2.5: {pm2_5_value} µg/m³, PM10.0: {pm10_0_value} µg/m³', 12, 45)
    #oled.show() 
    time.sleep(1)  # Read data every second
