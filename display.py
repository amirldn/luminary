# SPDX-FileCopyrightText: 2020 Jeff Epler for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import displayio
import framebufferio
import rgbmatrix
import os

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
    display.show(group)
    display.refresh(target_frames_per_second=1)
    print("Displaying " + filename)


bmp_path = "/bmp/"


while True:
    bmp_files = [f for f in os.listdir(bmp_path) if f.endswith(".bmp")]
    print(bmp_files)
    for bmp_file in bmp_files:
        try:
            display_bmp(bmp_path + bmp_file)
        except Exception as e:
            print("Error displaying " + bmp_file + ": " + str(e))
    # display_bmp(bmp_path + "2nkto6YNI4rUYTLqEwWJ3o.bmp")
