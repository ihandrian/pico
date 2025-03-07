import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
from machine import Pin, PWM, I2C
import machine
import ssd1306

# Initialize OLED Display
led1 = PWM(Pin(1))
led2 = PWM(Pin(5))
led3 = PWM(Pin(9))
led1.freq(1000)
led2.freq(1000)
led3.freq(1000)
# Setup I2C
# Pin assignments may need to be adjusted depending on your specific wiring
i2c = I2C(1, scl=Pin(27), sda=Pin(26), freq=400000)

ssid = 'your_ssid'
password = 'your_password'

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        # Clear the display
        oled.fill(0)
        # Display IP address
        oled.text('Try connection...', 12, 25)
        oled.show()    
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    # Display IP address
    oled.fill(0)
    oled.text('Connected:', 12, 25)
    oled.text(f'{ssid}', 12, 35)
    oled.text(f'{ip}', 12, 45)
    oled.show()  
    oled.fill(0)
    return ip

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(temperature, state):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <link rel="stylesheet" type="text/css" href="/style.css">
            </head>
            <body>
            <h1>Select LED</h1>
            <table>
                <tr>
                    <th>Red</th>
                    <th>Yellow</th>
                    <th>Green</th>
                </tr>
                <tr>
                    <td>
                        <form action="./red_on">
                            <input type="submit" value="On" />
                        </form>
                    </td>
                    <td>
                        <form action="./ylw_on">
                            <input type="submit" value="On" />
                        </form>
                    </td>
                    <td>
                        <form action="./grn_on">
                            <input type="submit" value="On" />
                        </form>
                    </td>
                </tr>
                <tr>
                    <td>
                        <form action="./red_off">
                            <input type="submit" value="Off" />
                        </form>
                    </td>
                    <td>
                        <form action="./ylw_off">
                            <input type="submit" value="Off" />
                        </form>
                    </td>
                    <td>
                        <form action="./grn_off">
                            <input type="submit" value="Off" />
                        </form>
                    </td>
                </tr>
            </table>
            <p>Temperature : {temperature}°C<br>
            Status : {state}</p><br>
            <p>Irfan Handrian/V.1/2024<br>MYTVPT23MAK</p>
            </body>
            </html>

            """
    return str(html)

def serve(connection):
    #Start a web server
    state = 'active'
    pico_led.on()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/red_on?':
            for duty_cycle in range(0, 65535, 10):
                led1.duty_u16(duty_cycle)
        elif request =='/red_off?':
            for duty_cycle in range(65535, 0, -10):
                led1.duty_u16(duty_cycle)
        if request == '/ylw_on?':
            for duty_cycle in range(0, 65535, 10):
                led2.duty_u16(duty_cycle)
        elif request =='/ylw_off?':
            for duty_cycle in range(65535, 0, -10):
                led2.duty_u16(duty_cycle)
        if request == '/grn_on?':
            for duty_cycle in range(0, 65535, 10):
                led3.duty_u16(duty_cycle)
        elif request =='/grn_off?':
            for duty_cycle in range(65535, 0, -10):
                led3.duty_u16(duty_cycle)

        temperature = round((pico_temp_sensor.temp), 2) # type: ignore
        html = webpage(temperature, state)
        client.send(html)
        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
    # Clear the display
    oled.fill(0)

    # Display IP address
    oled.text('Hello', ip, 12, 25)
    oled.show()                                                               
except KeyboardInterrupt:
    machine.reset()
    
    