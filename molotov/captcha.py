# -*- coding: utf-8; -*-

from datetime import datetime
import os.path
import random
import sha
import sys
import time

from PIL import Image, ImageDraw, ImageFont

from molotov.model import Captcha


def generate_text(chars, textlen):
    real_text = ""
    text = ""
    for i in xrange(textlen):
        sp = random.randint(0, 2)
        for s in xrange(sp):
            text += " "
        text += chars[random.randint(0, len(chars) - 1)]
        real_text += text[len(text) - 1]
    return (text, real_text)

def generate_point(width, height):
    return (random.randint(0, width),
            random.randint(0, height))

def generate_color(red_min=0, red_max=0xff,
                   green_min=0, green_max=0xff,
                   blue_min=0, blue_max=0xff):
    red = random.randint(max(0, red_min), min(red_max, 0xff))
    green = random.randint(max(0, green_min), min(green_max, 0xff))
    blue = random.randint(max(0, blue_min), min(blue_max, 0xff))
    ans = "#%02x%02x%02x" % (red, green, blue)
    return ans

def generate_color_like(color, offset):
    red = int(color[1:3], 16)
    green = int(color[3:5], 16)
    blue = int(color[5:7], 16)
    col = generate_color(red - offset, red + offset,
                         green - offset, green + offset,
                         blue - offset, blue + offset)
    return col

def generate_captcha(chars, textlen, width, height, font, font_size):

    # Create an image background filled
    bgcolor = generate_color()
    im = Image.new("RGB", (width, height), bgcolor)
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(font, font_size)

    # Draw the text
    textcolor = generate_color()
    (text, realtext) = generate_text(chars, textlen)
    draw.text((10, 10), text, font=font, fill=textcolor)

    # Add some lines
    lines_count = random.randint(2, 5)
    for l in xrange(lines_count):
        (x1, y1) = generate_point(width, height)
        (x2, y2) = generate_point(width, height)
        lcolor = generate_color()
        draw.line((x1, y1, x2, y2), width=1, fill=lcolor)
    
    # Add some dot noise
    for i in xrange(width * height / 4, width * height / 3):
        (x, y) = generate_point(width, height)
        pcol = generate_color()
        draw.point((x, y), fill=pcol)
    
    del draw
    return (realtext, im)

def create_captcha():
    random.seed(time.time())
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789&#@%"
    font = "/usr/share/fonts/dejavu/DejaVuSansCondensed-Oblique.ttf"
    (text, im) = generate_captcha(chars, 7, 145, 40, font, 20)

    # Generate an id for the captcha
    h = sha.new()
    h.update(str(random.random()))
    h.update(text)
    captcha_id = h.hexdigest()
    del h

    # Create the captcha image and it's link
    src = "/ustatic/captchas/%s.png" % captcha_id
    im.save("."+ src, "PNG")
    
    del im
    c = Captcha(captcha_id=captcha_id, text=text, src=src,
                creation=datetime.now())
    return c
