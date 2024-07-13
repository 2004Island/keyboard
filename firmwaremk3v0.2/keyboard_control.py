from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

class KeyboardController:
    def __init__(self, key_config, switches, pixels, oled):
        self.kbd = Keyboard(usb_hid.devices)
        self.keycodes = {}
        self.up_colors = {}
        self.down_colors = {}
        self.oled_texts = {}
        self.key_states = {switch: False for switch in switches}
        self.previous_displayed_key = None

        for key in key_config['keys']:
            self.keycodes[switches[key['key_number']]] = key['macro']
            self.up_colors[switches[key['key_number']]] = tuple(key['up_color'])
            self.down_colors[switches[key['key_number']]] = tuple(key['down_color'])
            self.oled_texts[switches[key['key_number']]] = key.get('oled', '')

    def check_and_send_keys(self, switches, pixels, display_centered_text, oled):
        new_key_pressed = None
        for switch in self.keycodes.keys():
            if not switch.value:  # Switch is pressed when value is False
                if not self.key_states[switch]:  # Only press keys if they are not already pressed
                    macro = self.keycodes[switch]
                    if Keycode.SEMICOLON in macro:
                        for keycode in macro:
                            if keycode != Keycode.SEMICOLON:
                                self.kbd.press(keycode)
                        for keycode in macro:
                            if keycode != Keycode.SEMICOLON:
                                self.kbd.release(keycode)
                    elif macro[0] == Keycode.SHIFT:
                        self.kbd.press(macro[0])
                        for i in range(1, len(macro)):
                            self.kbd.press(macro[i])
                            self.kbd.release(macro[i])
                        self.kbd.release(macro[0])
                    else:
                        for keycode in macro:
                            self.kbd.press(keycode)
                            self.kbd.release(keycode)
                    pixels[switches.index(switch)] = self.down_colors[switch]
                    self.key_states[switch] = True
                    new_key_pressed = switch
            else:
                if self.key_states[switch]:  # Only release keys if they are currently pressed
                    pixels[switches.index(switch)] = self.up_colors[switch]
                    self.key_states[switch] = False

        if new_key_pressed and new_key_pressed != self.previous_displayed_key:
            display_centered_text(oled, self.oled_texts[new_key_pressed])
            self.previous_displayed_key = new_key_pressed
