import neopixel

def setup_leds(pixelpin, num_pixels):
    pixels = neopixel.NeoPixel(pixelpin, num_pixels)
    return pixels

def light_up_leds(pixels, switches, up_colors):
    for i in range(16):
        pixels[i] = up_colors[switches[i]]
        sleep(0.1)
