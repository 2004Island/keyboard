def display_centered_text(oled, text):
    oled.fill(0)
    text_width = len(text) * 6  # Each character is approximately 6 pixels wide
    x = (oled.width - text_width) // 2
    y = (oled.height - 8) // 2  # Each character is approximately 8 pixels tall
    oled.text(text, x, y, 1)
    oled.show()
