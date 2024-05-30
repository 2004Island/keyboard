import json
import board
import busio
import neopixel
import digitalio
import usb_hid
import adafruit_ssd1306
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from time import sleep

# Load key configuration from JSON file
with open('key_config.json', 'r') as file:
    key_config = json.load(file)

# Convert string representations of Keycode to actual Keycode objects
for key in key_config['keys']:
    key['macro'] = [getattr(Keycode, code.split('.')[-1]) for code in key['macro']]

# Setup Neopixel LED
pixelpin = board.GP14
num_pixels = 16
pixels = neopixel.NeoPixel(pixelpin, num_pixels)

# Setup OLED
i2c = busio.I2C(board.GP1, board.GP0)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Test the display
oled.fill(0)
oled.text("Hello World", 0, 0, 1)
oled.show()

# Initialize digital inputs for switches
pins = [
    board.GP5, board.GP4, board.GP3, board.GP2,
    board.GP9, board.GP8, board.GP7, board.GP6,
    board.GP13, board.GP12, board.GP11, board.GP10,
    board.GP16, board.GP17, board.GP18, board.GP19
]
switches = [digitalio.DigitalInOut(pin) for pin in pins]
for switch in switches:
    switch.direction = digitalio.Direction.INPUT
    switch.pull = digitalio.Pull.UP

# Setup keyboard
kbd = Keyboard(usb_hid.devices)

# Create dictionaries for macros, colors, and OLED texts
keycodes = {}
up_colors = {}
down_colors = {}
oled_texts = {}
for key in key_config['keys']:
    keycodes[switches[key['key_number']]] = key['macro']
    up_colors[switches[key['key_number']]] = tuple(key['up_color'])
    down_colors[switches[key['key_number']]] = tuple(key['down_color'])
    oled_texts[switches[key['key_number']]] = key.get('oled', '')

# Dictionary to keep track of key states
key_states = {switch: False for switch in switches}

# Function to center text on the OLED display
def display_centered_text(oled, text):
    oled.fill(0)
    text_width = len(text) * 6  # Each character is approximately 6 pixels wide
    x = (oled.width - text_width) // 2
    y = (oled.height - 8) // 2  # Each character is approximately 8 pixels tall
    oled.text(text, x, y, 1)
    oled.show()

# Function to check and send keycodes
def check_and_send_keys():
    for switch in keycodes.keys():
        if not switch.value:  # Switch is pressed when value is False
            if not key_states[switch]:  # Only press keys if they are not already pressed
                macro = keycodes[switch]
                oled_text = oled_texts[switch]
                if macro[0] == Keycode.SHIFT:
                    kbd.press(Keycode.SHIFT)
                if len(macro) > 1 and Keycode.SEMICOLON in macro:
                    for keycode in macro:
                        if keycode != Keycode.SEMICOLON:
                            kbd.press(keycode)
                    # Release the COMMAND key at the end
                    for keycode in macro:
                        if keycode != Keycode.SEMICOLON:
                            kbd.release(keycode)
                elif macro[0] == Keycode.SHIFT:
                    kbd.press(macro[0])
                    for i in range(1, len(macro)):
                        kbd.press(macro[i])
                        kbd.release(macro[i])
                    kbd.release(macro[0])
                else:
                    # Press and release each key for non-COMMAND macros
                    for keycode in macro:
                        kbd.press(keycode)
                        kbd.release(keycode)
                pixels[switches.index(switch)] = down_colors[switch]
                display_centered_text(oled, oled_text)
                key_states[switch] = True
        else:
            if key_states[switch]:  # Only release keys if they are currently pressed
                pixels[switches.index(switch)] = up_colors[switch]
                key_states[switch] = False

# Main loop
while True:
    check_and_send_keys()
    sleep(0.05)  # Reduce delay to make key press detection more responsive

