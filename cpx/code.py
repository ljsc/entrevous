import board
import digitalio
import time
import supervisor
import neopixel

from adafruit_debouncer import Debouncer

def hsv(hue, saturation, value):
    """Convert hsv to rgb colorscale.

    See https://en.wikipedia.org/wiki/HSL_and_HSV#HSV_to_RGB
    
    hue - [0, 360]
    saturation - [0.0, 1.0]
    value - [0.0, 0.1]

    Returns tuple of r, g, and b components - [0, 255]
    """

    value *= 255
    chroma = value * saturation
    sector = hue / 60.

    x = chroma * (1 - abs(sector % 2 - 1))

    if 0 <= sector <= 1:  r,g,b = chroma, x, 0
    elif 1 < sector <= 2: r,g,b = x, chroma, 0
    elif 2 < sector <= 3: r,g,b = 0, chroma, x
    elif 3 < sector <= 4: r,g,b = 0, x, chroma
    elif 4 < sector <= 5: r,g,b = x, 0, chroma
    else: r,g,b = chroma, 0, x

    m = value - chroma

    return int(r+m), int(g+m), int(b+m)


def color(pixel, seq):
    """Compute pixel value for a pixel index given the current sequence number."""
    return hsv(pixel*12+60*seq, 0.95, 0.25)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=False)

ba = digitalio.DigitalInOut(board.BUTTON_A)
ba.switch_to_input(pull=digitalio.Pull.DOWN)
ba = Debouncer(ba)

CLEAR = (0, 0, 0)
CYCLE = len(pixels)

def reset():
    """Reset global sketch state."""
    global seq, frame, step
    seq = -1
    frame = 0
    step = -1


reset()
 
## Main loop

active = True

while True:
    ba.update()

    if ba.rose:
        if active:
            active = False
            reset()
            pixels.fill((0, 0, 0))
            pixels.show()
        else:
            active = True

    if active:
        if frame == 0 or frame == 2 * CYCLE:
            step *= -1

        if frame == 0: seq = (seq + 1) % 6

        frame += step

        for x in range(CYCLE):
            c = color(x, seq) if x < frame <= x + CYCLE else CLEAR
            pixels[x] = c
        pixels.show()

    time.sleep(0.01)
