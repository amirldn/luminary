# SPDX-FileCopyrightText: 2020 Jeff Epler for Adafruit Industries
# SPDX-License-Identifier: MIT

# IDEA: Have a text file on the board that gets written to with bmp id

import board
import displayio
import framebufferio
import rgbmatrix
import os
import usb_cdc
import time

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

bmp_path = "/bmp/"


# Potentially a memory leak - should release these groups or reuse them
def group_with_bmp(filepath):
    bmp = displayio.OnDiskBitmap(filepath)
    tilegrid = displayio.TileGrid(
        bmp,
        pixel_shader=bmp.pixel_shader,
        tile_width=bmp.width,
        tile_height=bmp.height,
    )
    group = displayio.Group()
    group.append(tilegrid)
    return group


def display_bmp(bmp_id):
    filepath = bmp_path + bmp_id + ".bmp"
    group = group_with_bmp(filepath)
    display.show(group)
    display.refresh(target_frames_per_second=60)
    print("Displaying " + filepath)


# Iterate through all bmp files in the bmp_path directory and display them
print("Starting...")
while True:
    print("Fetching files...")
    bmp_files = [f for f in os.listdir(bmp_path) if f.endswith(".bmp")]
    print("Found bmps: {}".format(bmp_files))
    for bmp_file in bmp_files:
        bmp_id = bmp_file.replace(".bmp", "")
        try:
            display_bmp(bmp_id)
        except Exception as e:
            print("Error displaying " + bmp_file + ": " + str(e))
    # display_bmp("2nkto6YNI4rUYTLqEwWJ3o")
