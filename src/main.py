import RPi.GPIO as GPIO
import requests
import json
import time
import os


config_path = os.path.join(os.path.dirname(__file__),  "data", "config.json")


def get_token():
    config = json.load(open(config_path, "r", encoding="utf-8"))
    user_id = config["selected-user"]
    return config["users"][user_id]["token"]


BUTTON_PIN = 21  # Button is attached to PIN 21

GPIO.setmode(GPIO.BCM)  # BCM Mode - pins are treated by their GPIO numbers
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set pin to input


def ring_phone():
    data = {
        "type": "note",
        "title": "איתור הטלפון",
        "body": "כנראה שמישהו לחץ על הכפתור..."
    }

    response = requests.post(
        "https://api.pushbullet.com/v2/pushes",
        json=data,
        headers={"Access-Token": get_token()}
    )

    print(response.text)


def mainloop():
    previous_state = GPIO.HIGH
    try:
        while True:
            time.sleep(0.01)
            current_state = GPIO.input(BUTTON_PIN)
            if current_state != previous_state:
                # If the button was pressed
                if current_state == GPIO.LOW:
                    ring_phone()
                previous_state = current_state
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == '__main__':
    mainloop()
