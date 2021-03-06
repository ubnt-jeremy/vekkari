#!/usr/bin/env python

##
# epaper-clock.py
#
# Copyright (C) Jukka Aittola (jaittola(at)iki.fi)
#
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 ##

##
 #  @filename   :   main.cpp
 #  @brief      :   2.9inch e-paper display (B) demo
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     July 31 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 ##

import epd2in7b
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import RPi.GPIO as GPIO

from datetime import datetime
import time
import locale
import subprocess

COLORED = 1
UNCOLORED = 0

LOCALE="fi_FI"
DATEFORMAT = "%a %x"
TIMEFORMAT = "%H:%M"
FONT = '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf'

class Fonts:
    def __init__(self, timefont_size, datefont_size):
        self.timefont = ImageFont.truetype(FONT, timefont_size)
        self.datefont = ImageFont.truetype(FONT, datefont_size)

def main():
    locale.setlocale(locale.LC_ALL, LOCALE)

    epd = epd2in7b.EPD()
    epd.init()
    epd.set_rotate(epd2in7b.ROTATE_270)

    fonts = Fonts(timefont_size = 75, datefont_size = 30)

    read_button4_for_shutdown()
    clock_loop(epd, fonts)

def clock_loop(epd, fonts):
    while True:
        now = datetime.now()
        draw_clock_data(epd, fonts, now)
        now = datetime.now()
        seconds_until_next_minute = 60 - now.time().second
        time.sleep(seconds_until_next_minute)

def draw_clock_data(epd, fonts, datetime_now):
    datestring = datetime_now.strftime(DATEFORMAT).capitalize()
    timestring = datetime_now.strftime(TIMEFORMAT)

    # Create frame buffers
    frame_black = [0] * (epd.width * epd.height / 8)
    frame_red = [0] * (epd.width * epd.height / 8)

    epd.draw_string_at(frame_black, 20, 20, timestring, fonts.timefont, COLORED)
    epd.draw_string_at(frame_black, 20, 100, datestring, fonts.datefont, COLORED)
#    epd.draw_string_at(frame_red, 50, 120, "e-paper.", font, COLORED)
    epd.display_frame(frame_black, frame_red)

def read_button4_for_shutdown():
    GPIO.setmode(GPIO.BCM)
    pin = 19  # 4th button in the 2.7 inch hat this pin according to the schematics.
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=shutdown_button_pressed, bouncetime=200)

def shutdown_button_pressed(pin):
    print("Button %d was pressed. Shutting down" % pin)
    subprocess.call(["sudo", "poweroff"])

if __name__ == '__main__':
    main()
