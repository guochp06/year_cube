#!/usr/bin/env python3
"""Generate Android launcher icons for YearCube app."""

from PIL import Image, ImageDraw
import os
import shutil

# Android icon sizes
SIZES = {
    'mdpi': 48,
    'hdpi': 72,
    'xhdpi': 96,
    'xxhdpi': 144,
    'xxxhdpi': 192,
}

# Colors
BG_COLOR = (76, 175, 80)       # #4caf50 - primary green
GRID_COLOR = (255, 255, 255)   # white grid lines/cells

def draw_icon(size, round_mask=False):
    """Draw a launcher icon with a grid motif."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background circle or rounded rect
    radius = size // 6
    if round_mask:
        # For round icon: full circle
        draw.ellipse([0, 0, size, size], fill=BG_COLOR)
    else:
        # For square icon: rounded rectangle
        draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=BG_COLOR)

    # Draw a small 3x3 grid in the center
    grid_cells = 3
    padding = size // 5
    cell_gap = max(1, size // 24)
    cell_size = (size - 2 * padding - (grid_cells - 1) * cell_gap) // grid_cells
    grid_total = grid_cells * cell_size + (grid_cells - 1) * cell_gap
    start_x = (size - grid_total) // 2
    start_y = (size - grid_total) // 2

    for row in range(grid_cells):
        for col in range(grid_cells):
            x1 = start_x + col * (cell_size + cell_gap)
            y1 = start_y + row * (cell_size + cell_gap)
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            cell_radius = max(1, cell_size // 4)
            # Fill top-left 4 cells (representing passed time), outline others
            if row * grid_cells + col < 4:
                draw.rounded_rectangle([x1, y1, x2, y2], radius=cell_radius, fill=GRID_COLOR)
            else:
                draw.rounded_rectangle([x1, y1, x2, y2], radius=cell_radius, outline=GRID_COLOR, width=max(1, size // 32))

    return img

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    res_dir = os.path.join(base_dir, 'android', 'app', 'src', 'main', 'res')

    for dpi, size in SIZES.items():
        # Square icons
        mipmap_dir = os.path.join(res_dir, f'mipmap-{dpi}')
        os.makedirs(mipmap_dir, exist_ok=True)
        icon = draw_icon(size, round_mask=False)
        icon.save(os.path.join(mipmap_dir, 'ic_launcher.png'), 'PNG')

        # Round icons (Android 8.0+ fallback and legacy round)
        mipmap_round_dir = os.path.join(res_dir, f'mipmap-{dpi}-v26')
        os.makedirs(mipmap_round_dir, exist_ok=True)
        round_icon = draw_icon(size, round_mask=True)
        round_icon.save(os.path.join(mipmap_round_dir, 'ic_launcher_round.png'), 'PNG')

        # Also save round to default mipmap dir for legacy support
        round_icon.save(os.path.join(mipmap_dir, 'ic_launcher_round.png'), 'PNG')

        # Remove old foreground files if they exist
        fg_path = os.path.join(mipmap_dir, 'ic_launcher_foreground.png')
        if os.path.exists(fg_path):
            os.remove(fg_path)

    # Play store icon 512x512
    store_dir = os.path.join(base_dir, 'assets')
    os.makedirs(store_dir, exist_ok=True)
    store_icon = draw_icon(512, round_mask=False)
    store_icon.save(os.path.join(store_dir, 'icon-512.png'), 'PNG')

    print("Icons generated successfully!")

if __name__ == '__main__':
    main()
