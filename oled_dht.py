from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
import time
import dht

# Initialize OLED Display
oled_x = 128
oled_y = 64
button = Pin(16, Pin.IN, Pin.PULL_DOWN)

# Setup I2C
disp = I2C(1, scl=Pin(27), sda=Pin(26), freq=200000)
oled = SSD1306_I2C(oled_x, oled_y, disp)

# Initialize DHT22
dht_sensor = dht.DHT22(Pin(16))  # GPIO 14 for DHT22


# Function to read from DHT22
def read_dht22():
    dht_sensor.measure()  # Trigger a measurement
    temp = dht_sensor.temperature()  # Get temperature
    hum = dht_sensor.humidity()  # Get humidity
    return temp, hum

print('Code by: Irfan Handrian')
while True:
    temp, hum = read_dht22()  # Read temperature and humidity

    if button.value() == 1:
        # Display "Hei Maailma" with temperature and humidity
        oled.fill(0)
        oled.text('Hei Maailma', 0, 0)
        oled.text('Temp: {}C'.format(temp), 0, 10)
        oled.text('Hum: {}%'.format(hum), 0, 20)
        oled.text('-Irfan H-'.format(hum), 0, 30)
    else:
        # Display "Hello World" with temperature and humidity
        oled.fill(0)
        oled.text('Hei Maailma', 0, 0)
        oled.text('Temp: {}C'.format(temp), 0, 10)
        oled.text('Hum: {}%'.format(hum), 0, 20)
        oled.text('-Irfan H-'.format(hum), 0, 40)

    oled.show()
    time.sleep(0.1)  # a small delay for loop

