#!/usr/bin/env python3
"""
Create a symbolic logo for CCDebugger
Design: Magnifying glass with bug/error symbol inside
Simple, high contrast, works in black and white
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

def create_logo(size, bg_color="#FFFFFF", fg_color="#000000", style="filled"):
    """
    Create CCDebugger logo at specified size
    
    Args:
        size: Square dimensions (e.g., 512 for 512x512)
        bg_color: Background color
        fg_color: Foreground color
        style: "filled" or "outline"
    """
    # Create image
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Fill background
    draw.rectangle([0, 0, size, size], fill=bg_color)
    
    # Calculate dimensions
    padding = size // 8
    canvas_size = size - (padding * 2)
    center_x = size // 2
    center_y = size // 2
    
    # Line width based on size
    line_width = max(2, size // 32)
    thick_line = line_width * 2
    
    # Magnifying glass parameters
    glass_radius = canvas_size // 3
    handle_length = canvas_size // 4
    handle_width = glass_radius // 3
    
    # Draw magnifying glass handle
    handle_start_x = center_x + glass_radius * 0.7
    handle_start_y = center_y + glass_radius * 0.7
    handle_end_x = center_x + glass_radius + handle_length
    handle_end_y = center_y + glass_radius + handle_length
    
    # Handle (thick line)
    draw.line(
        [handle_start_x, handle_start_y, handle_end_x, handle_end_y],
        fill=fg_color,
        width=handle_width
    )
    
    # Glass rim
    if style == "filled":
        # Outer circle (filled)
        draw.ellipse(
            [center_x - glass_radius, center_y - glass_radius,
             center_x + glass_radius, center_y + glass_radius],
            fill=fg_color
        )
        # Inner circle (to create rim)
        inner_radius = glass_radius - thick_line
        draw.ellipse(
            [center_x - inner_radius, center_y - inner_radius,
             center_x + inner_radius, center_y + inner_radius],
            fill=bg_color
        )
    else:
        # Outline only
        for i in range(thick_line):
            draw.ellipse(
                [center_x - glass_radius + i, center_y - glass_radius + i,
                 center_x + glass_radius - i, center_y + glass_radius - i],
                outline=fg_color,
                width=1
            )
    
    # Draw bug/error symbol inside glass
    bug_size = glass_radius // 2
    
    # Create a stylized bug that looks like brackets with an X
    # This represents both a bug and code error
    
    # Left bracket <
    bracket_height = bug_size
    bracket_width = bug_size // 3
    left_x = center_x - bug_size // 2
    
    points_left = [
        (left_x, center_y),
        (left_x - bracket_width, center_y - bracket_height // 2),
        (left_x - bracket_width + line_width, center_y - bracket_height // 2 + line_width),
        (left_x + line_width, center_y),
        (left_x - bracket_width + line_width, center_y + bracket_height // 2 - line_width),
        (left_x - bracket_width, center_y + bracket_height // 2),
    ]
    draw.polygon(points_left, fill=fg_color)
    
    # Right bracket >
    right_x = center_x + bug_size // 2
    points_right = [
        (right_x, center_y),
        (right_x + bracket_width, center_y - bracket_height // 2),
        (right_x + bracket_width - line_width, center_y - bracket_height // 2 + line_width),
        (right_x - line_width, center_y),
        (right_x + bracket_width - line_width, center_y + bracket_height // 2 - line_width),
        (right_x + bracket_width, center_y + bracket_height // 2),
    ]
    draw.polygon(points_right, fill=fg_color)
    
    # X in the middle
    x_size = bug_size // 3
    x_offset = x_size // 2
    
    # First line of X
    draw.line(
        [center_x - x_offset, center_y - x_offset,
         center_x + x_offset, center_y + x_offset],
        fill=fg_color,
        width=line_width
    )
    
    # Second line of X
    draw.line(
        [center_x - x_offset, center_y + x_offset,
         center_x + x_offset, center_y - x_offset],
        fill=fg_color,
        width=line_width
    )
    
    return img

def create_all_icons():
    """Create all required icon sizes and variations"""
    
    # Icon sizes for Chrome Extension
    sizes = [16, 32, 48, 128, 512]
    
    # Create directories
    os.makedirs("assets/icons", exist_ok=True)
    os.makedirs("dist/assets/icons", exist_ok=True)
    os.makedirs("logo_variants", exist_ok=True)
    
    # Create main icons (black on white)
    for size in sizes:
        img = create_logo(size, bg_color="#FFFFFF", fg_color="#000000")
        if size <= 128:
            img.save(f"assets/icons/icon-{size}.png")
            img.save(f"dist/assets/icons/icon-{size}.png")
        img.save(f"logo_variants/logo-{size}.png")
    
    # Create dark mode variants (white on black)
    for size in sizes:
        img = create_logo(size, bg_color="#000000", fg_color="#FFFFFF")
        img.save(f"logo_variants/logo-dark-{size}.png")
    
    # Create transparent background variants
    for size in sizes:
        img = create_logo(size, bg_color=(0, 0, 0, 0), fg_color="#000000")
        img.save(f"logo_variants/logo-transparent-{size}.png")
    
    # Create colored variants
    colors = {
        "blue": ("#1E3A8A", "#FFFFFF"),  # Dark blue with white
        "red": ("#DC2626", "#FFFFFF"),   # Red with white
        "green": ("#059669", "#FFFFFF"), # Green with white
        "purple": ("#7C3AED", "#FFFFFF"), # Purple with white
    }
    
    for color_name, (bg, fg) in colors.items():
        for size in [128, 512]:
            img = create_logo(size, bg_color=bg, fg_color=fg)
            img.save(f"logo_variants/logo-{color_name}-{size}.png")
    
    # Create outline variants
    for size in [128, 512]:
        img = create_logo(size, bg_color="#FFFFFF", fg_color="#000000", style="outline")
        img.save(f"logo_variants/logo-outline-{size}.png")
    
    # Create store assets with the logo
    print("Creating store assets with logo...")
    
    store_sizes = {
        "small_promo": (440, 280),
        "large_promo": (920, 680),
        "marquee_promo": (1400, 560),
        "screenshot": (1280, 800)
    }
    
    for name, (width, height) in store_sizes.items():
        # Create promotional image
        img = Image.new('RGBA', (width, height), "#F8F9FA")
        draw = ImageDraw.Draw(img)
        
        # Add logo
        logo_size = min(width, height) // 3
        logo = create_logo(logo_size, bg_color=(0, 0, 0, 0), fg_color="#000000")
        
        # Position logo
        logo_x = (width - logo_size) // 2
        logo_y = (height - logo_size) // 2 - 50
        
        # Paste logo
        img.paste(logo, (logo_x, logo_y), logo)
        
        # Add text
        try:
            # Try to use a clean system font
            font_size = min(width, height) // 15
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
            font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(font_size * 0.6))
        except:
            font = ImageFont.load_default()
            font_small = font
        
        # Main text
        text = "CCDebugger"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (width - text_width) // 2
        text_y = logo_y + logo_size + 30
        draw.text((text_x, text_y), text, fill="#000000", font=font)
        
        # Tagline
        tagline = "AI-Powered Error Debugging Assistant"
        bbox = draw.textbbox((0, 0), tagline, font=font_small)
        tagline_width = bbox[2] - bbox[0]
        tagline_x = (width - tagline_width) // 2
        tagline_y = text_y + font_size + 10
        draw.text((tagline_x, tagline_y), tagline, fill="#666666", font=font_small)
        
        # Save
        os.makedirs("store_assets", exist_ok=True)
        img.save(f"store_assets/{name}.png")
    
    print("Logo creation complete!")
    print("\nCreated files:")
    print("- Extension icons: assets/icons/icon-*.png")
    print("- Logo variants: logo_variants/")
    print("- Store assets: store_assets/")
    
    # Create a logo showcase
    showcase = Image.new('RGBA', (1200, 800), "#F0F0F0")
    draw = ImageDraw.Draw(showcase)
    
    # Add title
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
    except:
        title_font = ImageFont.load_default()
    
    draw.text((50, 30), "CCDebugger Logo Variants", fill="#000000", font=title_font)
    
    # Arrange logos
    positions = [
        (50, 100, "Original"),
        (300, 100, "Dark Mode"),
        (550, 100, "Transparent"),
        (800, 100, "Outline"),
        (50, 350, "Blue"),
        (300, 350, "Red"),
        (550, 350, "Green"),
        (800, 350, "Purple"),
    ]
    
    logo_display_size = 200
    
    for x, y, label in positions:
        # Add label
        draw.text((x, y - 30), label, fill="#333333", font=title_font)
        
        # Determine which logo to load
        if label == "Original":
            logo = create_logo(logo_display_size, bg_color="#FFFFFF", fg_color="#000000")
        elif label == "Dark Mode":
            logo = create_logo(logo_display_size, bg_color="#000000", fg_color="#FFFFFF")
        elif label == "Transparent":
            logo = create_logo(logo_display_size, bg_color=(0, 0, 0, 0), fg_color="#000000")
            # Add checkered background
            for i in range(0, logo_display_size, 20):
                for j in range(0, logo_display_size, 20):
                    if (i // 20 + j // 20) % 2 == 0:
                        draw.rectangle([x + i, y + j, x + i + 20, y + j + 20], fill="#E0E0E0")
        elif label == "Outline":
            logo = create_logo(logo_display_size, bg_color="#FFFFFF", fg_color="#000000", style="outline")
        else:
            # Color variants
            color_map = {
                "Blue": ("#1E3A8A", "#FFFFFF"),
                "Red": ("#DC2626", "#FFFFFF"),
                "Green": ("#059669", "#FFFFFF"),
                "Purple": ("#7C3AED", "#FFFFFF"),
            }
            bg, fg = color_map.get(label, ("#000000", "#FFFFFF"))
            logo = create_logo(logo_display_size, bg_color=bg, fg_color=fg)
        
        showcase.paste(logo, (x, y), logo if logo.mode == 'RGBA' else None)
    
    showcase.save("logo_variants/logo_showcase.png")
    print("\nLogo showcase saved as: logo_variants/logo_showcase.png")

if __name__ == "__main__":
    create_all_icons()