import json
from adafruit_hid.keycode import Keycode

def load_key_config(file_path):
    with open(file_path, 'r') as file:
        key_config = json.load(file)
    for key in key_config['keys']:
        key['macro'] = [getattr(Keycode, code.split('.')[-1]) for code in key['macro']]
    return key_config
