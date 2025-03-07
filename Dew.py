import machine
from machine import Pin, I2C
import ssd1306
import dht
import time

# OLED display
I2C_PORT = 1
I2C_SCL = Pin(7)
I2C_SDA = Pin(6)
OLED_WIDTH = 128 
OLED_HEIGHT = 64
oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, I2C(I2C_PORT, scl=I2C_SCL,
sda=I2C_SDA))

# Temperatur and Humidity Sensor
DHT_SENSOR_PIN = Pin(16)
dht_sensor = dht.DHT22(DHT_SENSOR_PIN)

# Buttons
BUTTON_1_PIN = Pin(20)
BUTTON_2_PIN = Pin(18)
button_1 = machine.Pin(BUTTON_1_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_2 = machine.Pin(BUTTON_2_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN) 

# Measure and read values from the sensor
dht_sensor.measure()
temperature = dht_sensor.temperature()
humidity = dht_sensor.humidity()

# Calculate the dew point
dew_point = temperature - (100 - humidity) / 5

def button1(Pin):
    oled.fill(0)
    oled.text(f'Temp: {temperature}C', 12, 15)
    oled.show()
    time.sleep(1)
    
def button2(Pin) :
    oled.fill(0)
    oled.text(f'Hum_: {humidity}%', 12, 25)
    oled.show()
    time.sleep(1)
    
def dew() :
    oled.fill(0)
    oled.text(f'Temp: {temperature}C', 12, 15)
    oled.text(f'Hum_: {humidity}%', 12, 25)
    oled.text(f'Dew : {dew_point}C', 12, 35)
    oled.show()
    time.sleep(5)

# Print the results
print("Temperature (°C):", temperature)
print("Relative Humidity (%):", humidity) 
print("Dew Point (°C):", dew_point)

button_1.irq(trigger=machine.Pin.IRQ_FALLING, handler=button1)
button_2.irq(trigger=machine.Pin.IRQ_FALLING, handler=button2)

while True:
    dew()
    if KeyboardInterrupt : 
        machine.reset()
