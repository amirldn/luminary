# SPDX-FileCopyrightText: 2020 Jeff Epler for Adafruit Industries
# SPDX-License-Identifier: MIT

import random
import time

import board
import displayio
import framebufferio
import rgbmatrix

displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=32,
    height=32,
    bit_depth=3,
    rgb_pins=[board.R0, board.G0, board.B0, board.R1, board.G1, board.B1],
    addr_pins=[board.ROW_A, board.ROW_B, board.ROW_C, board.ROW_D],
    clock_pin=board.CLK,
    latch_pin=board.LAT,
    output_enable_pin=board.OE,
)

# Associate matrix with a Display to use displayio features
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False, rotation=0)


root = displayio.Group()
display.root_group = root

FILENAME = "bmp/1.bmp"


# Potentially a memory leak - should release these groups or reuse them
def group_with_bmp(filename):
    bmp = displayio.OnDiskBitmap(filename)
    tilegrid = displayio.TileGrid(
        bmp,
        pixel_shader=bmp.pixel_shader,
        tile_width=bmp.width,
        tile_height=bmp.height,
    )
    group = displayio.Group()
    group.append(tilegrid)
    return group


def display_bmp(filename):
    group = group_with_bmp(filename)
    # root.append(group)
    display.refresh(minimum_frames_per_second=0)
    display.root_group = group
    print("Displaying " + filename)


bmps = [0, 1, 2, 3, 4, 5, 6, 7]
count = 5

while True:
    print(count)
    if count == 7:
        count = 0

    display_bmp("bmp/" + str(count) + ".bmp")
    count += 1
    time.sleep(3)
