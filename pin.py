from machine import Pin
import utime
import urequests
import time
from servo import Servo

# Create our Servo object, assigning the
# GPIO pin connected the PWM wire of the servo
my_servo = Servo(pin_id=17)

delay_ms = 25

matrix_keys = [['1', '2', '3'],
              ['4', '5', '6'],
              ['7', '8', '9'],
              ['*', '0', '#']]
secret_pin = ['7', '7', '7', '7']
guess = []
buzzer = Pin(18, Pin.OUT, Pin.PULL_UP)
led = Pin(17, Pin.OUT, Pin.PULL_UP)
red = Pin(21, Pin.OUT, Pin.PULL_UP)
keypad_rows = [9, 10, 11, 12]
keypad_columns = [13, 14, 15]
col_pins = []
row_pins = []

for x in range(0, 4):
    row_pins.append(Pin(keypad_rows[x], Pin.OUT))
    row_pins[x].value(1)
for x in range(0, 3):
