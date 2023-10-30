from machine import Pin
from mfrc522 import MFRC522
import urequests

reader = MFRC522(spi_id=0, sck=6, miso=4, mosi=7, cs=5, rst=22)

red = Pin(17, Pin.OUT)
green = Pin(1, Pin.OUT)
blue = Pin(2, Pin.OUT)
buzzer = Pin(16, Pin.OUT)  # Initialize the buzzer pin

print("Bring RFID TAG Closer...")
print("")

# Replace 'YOUR_ZAPIER_WEBHOOK_URL' with the actual Zapier webhook URL
ZAPIER_WEBHOOK_URL = 'https://hooks.zapier.com/hooks/catch/16892604/38gxyfm/'

incorrect_attempts = 0  # Track the number of incorrect attempts
MAX_INCORRECT_ATTEMPTS = 3  # Define the maximum allowed incorrect attempts

while True:
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid), "little", False)

            if card == 691173844:
                print("Card ID: " + str(card) + " PASS: Green Light Activated")
                red.value(1)
                green.value(0)
                blue.value(0)
                incorrect_attempts = 0  # Reset incorrect attempts on successful card read
            else:
                print("Card ID: " + str(card) + " UNKNOWN CARD! Red Light Activated")
                red.value(0)
                green.value(0)
                blue.value(0)
                incorrect_attempts += 1  # Increment incorrect attempts

                if incorrect_attempts >= MAX_INCORRECT_ATTEMPTS:
                    # Activate the buzzer after 3 wrong attempts
                    buzzer.value(1)
                else:
                    buzzer.value(0)

                # Send an HTTP POST request to trigger the Zap in Zapier
                data = {"card_id": card}
                response = urequests.post(ZAPIER_WEBHOOK_URL, json=data)

                if response.status_code == 200:
                    print("Zapier Webhook Triggered Successfully")
                else:
                    print("Error Triggering Zapier Webhook")

                response.close()