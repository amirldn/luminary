# SPDX-FileCopyrightText: 2020 Jeff Epler for Adafruit Industries
# SPDX-License-Identifier: MIT

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
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True, rotation=0)
root = displayio.Group()
display.root_group = root

bmp_path = "/bmp/"


def display_bmp():
    # Setup the file as the bitmap data source
    bitmap = displayio.OnDiskBitmap("/bmp/cover.bmp")
    # Create a TileGrid to hold the bitmap
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
    # Create a Group to hold the TileGrid
    group = displayio.Group()
    # Add the TileGrid to the Group
    group.append(tile_grid)
    # Add the Group to the Display
    display.root_group = group
    display.refresh(target_frames_per_second=1)


print("Starting...")
while True:
    try:
        display_bmp()
    except Exception as e:
        print("Error displaying: " + str(e))
