import board
import busio
import digitalio
import usb_hid
import adafruit_ssd1306
from time import sleep

from config import load_key_config
from display import display_centered_text
from keyboard_control import KeyboardController
from led_control import setup_leds, light_up_leds

# Load key configuration
key_config = load_key_config('key_config.json')

# Setup Neopixel LED
pixelpin = board.GP14
num_pixels = 16
pixels = setup_leds(pixelpin, num_pixels)

# Setup OLED
i2c = busio.I2C(board.GP1, board.GP0)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Initialize digital inputs for switches (right to left, top to bottom)
pins = [
    board.GP8, board.GP9, board.GP10, board.GP11,
    board.GP4, board.GP5, board.GP6, board.GP7,
    board.GP0, board.GP1, board.GP2, board.GP3,
    board.GP12, board.GP13, board.GP14, board.GP15
]

switches = [digitalio.DigitalInOut(pin) for pin in pins]
for switch in switches:
    switch.direction = digitalio.Direction.INPUT
    switch.pull = digitalio.Pull.UP

# Setup keyboard controller
kbd_controller = KeyboardController(key_config, switches, pixels, oled)

# Light up LEDs initially
light_up_leds(pixels, switches, kbd_controller.up_colors)

# Main loop
while True:
    kbd_controller.check_and_send_keys(switches, pixels, display_centered_text, oled)
    sleep(0.01)  # Reduce delay to make key press detection more responsive
