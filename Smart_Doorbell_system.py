import RPi.GPIO as GPIO
import subprocess
import time
import RPi.GPIO as GPIO  # For GPIO pin control
from picamera2 import Picamera2
import time  # For delays and timestamps
import requests  # For sending notifications via IFTTT
from twilio.rest import Client  # For sending SMS via Twilio

# Define GPIO pins for the button and buzzer
BUTTON_PIN = 21  # Example GPIO pin for button
BUZZER_PIN = 18  # Example GPIO pin for buzzer

# Set up GPIO
GPIO.setmode(GPIO.BCM)
# Set button as input with pull-down resistor
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)  # Set buzzer as output

# Initialize the Pi Camera
camera = Picamera2()
camera.configure(camera.create_still_configuration())
camera.start()

# Set up notification URLs and tokens (IFTTT is still there for image upload)
# Replace with your IFTTT key
IFTTT_WEBHOOK_URL = "https://maker.ifttt.com/trigger/doorbell_pressed/with/key/YOUR_IFTTT_KEY"

# Twilio credentials (replace with your Twilio account SID, auth token, and phone number)
# Replace with your Twilio Account SID
TWILIO_ACCOUNT_SID = 'Your Twilio Account SID'
# Replace with your Twilio Auth Token
TWILIO_AUTH_TOKEN = 'Your Auth Token'
# Your Twilio phone number (e.g., +1234567890)
TWILIO_PHONE_NUMBER = 'Your Twilio Phone number'
# The recipient's phone number (e.g., +11234567890)
USER_PHONE_NUMBER = 'Enter users Phone Number'

# Twilio Client Setup
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_sms(message):
    # Send an SMS to the user via Twilio
    message = client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,  # Twilio phone number
        to=USER_PHONE_NUMBER  # Recipient phone number
    )
    print(f"Message sent: {message.sid}")


def send_notification(image_path):
    # Send the captured image via IFTTT (optional)
    with open(image_path, 'rb') as file:
        requests.post(IFTTT_WEBHOOK_URL, files={'photo': file})

    # Send SMS via Twilio
    send_sms(f"Doorbell Pressed! Image captured: {image_path}")


def capture_image():
    # Generate a timestamped filename
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    image_path = f'/home/pi/doorbell_{timestamp}.jpg'
    camera.capture(image_path)  # Capture the image
    return image_path


try:
    while True:
        # Check if the button is pressed
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:  # Button pressed
            print("Button Pressed! Capturing image...")

            # Sound the buzzer briefly
            GPIO.output(BUZZER_PIN, GPIO.HIGH)  # Turn on the buzzer
            time.sleep(0.5)  # Buzzer sounds for half a second
            GPIO.output(BUZZER_PIN, GPIO.LOW)  # Turn off the buzzer

            # Capture the image
            image_path = capture_image()
            print("Image captured:", image_path)

            # Send the notification (SMS and IFTTT)
            send_notification(image_path)
            print("Notification sent!")

            # Debounce delay to prevent multiple triggers
            time.sleep(5)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()  # Clean up GPIO on exit


# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
button_pin = 21          # GPIO pin where button is connected
buzzer_pin = 18          # GPIO pin where buzzer is connected

# Set up the button pin as an input, and the buzzer pin as an output
# Button is pulled up to 3.3V
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buzzer_pin, GPIO.OUT)

# Function to ring the buzzer


def ring_buzzer():
    GPIO.output(buzzer_pin, GPIO.HIGH)  # Turn on buzzer
    time.sleep(0.5)  # Buzzer rings for 0.5 seconds
    GPIO.output(buzzer_pin, GPIO.LOW)   # Turn off buzzer


try:
    # Print the first message
    print("Program Activated")

    # Add a 3-second delay
    time.sleep(3)

    # Check for button press
    while True:
        button_state = GPIO.input(button_pin)

        if button_state == GPIO.LOW:  # Button pressed (assuming active low)
            print("Button Pressed! Ringing the buzzer...")
            ring_buzzer()  # Ring the buzzer when button is pressed

            # Run the libcamera-hello command
            subprocess.run(['libcamera-hello'])

            # Print the second message
            print("Object Detected and Image Captured")

            # Add another 3-second delay
            time.sleep(3)

            # Print the third message
            print("Program Terminated")

            break  # Exit the loop after the program runs

except KeyboardInterrupt:
    print("Program interrupted by user.")
finally:
    GPIO.cleanup()  # Clean up GPIO settings on exit

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
button_pin = 21          # GPIO pin where button is connected
buzzer_pin = 18          # GPIO pin where buzzer is connected

# Set up the button pin as an input, and the buzzer pin as an output
# Button is pulled up to 3.3V
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buzzer_pin, GPIO.OUT)

# Function to ring the buzzer


def ring_buzzer():
    GPIO.output(buzzer_pin, GPIO.HIGH)  # Turn on buzzer
    time.sleep(0.5)  # Buzzer rings for 0.5 seconds
    GPIO.output(buzzer_pin, GPIO.LOW)   # Turn off buzzer


try:
    # Print the first message
    print("Program Activated")

    # Add a 3-second delay
    time.sleep(3)

    # Check for button press
    while True:
        button_state = GPIO.input(button_pin)

        if button_state == GPIO.LOW:  # Button pressed (assuming active low)
            print("Button Pressed! Ringing the buzzer...")
            ring_buzzer()  # Ring the buzzer when button is pressed

            # Run the libcamera-hello command
            subprocess.run(['libcamera-hello'])

            # Print the second message
            print("Object Detected and Image Captured")

            # Add another 3-second delay
            time.sleep(3)

            # Print the third message
            print("Program Terminated")

            break  # Exit the loop after the program runs

except KeyboardInterrupt:
    print("Program interrupted by user.")
finally:
    GPIO.cleanup()  # Clean up GPIO settings on exit
