#!/usr/bin/env python3
"""
Generate icon files for Chrome Extension
Creates placeholder icons in required sizes: 16, 32, 48, 128 pixels
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Icon sizes required by Chrome
SIZES = [16, 32, 48, 128]

# Create directories
os.makedirs("assets/icons", exist_ok=True)
os.makedirs("dist/assets/icons", exist_ok=True)

# Base colors
BG_COLOR = "#1a1a2e"  # Dark blue
FG_COLOR = "#0f4c81"  # Blue
TEXT_COLOR = "#ffffff"  # White

for size in SIZES:
    # Create image with background
    img = Image.new('RGBA', (size, size), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Draw a bug icon (simplified)
    padding = size // 8
    bug_size = size - (padding * 2)
    
    # Bug body (circle)
    body_radius = bug_size // 3
    center_x = size // 2
    center_y = size // 2
    
    draw.ellipse(
        [center_x - body_radius, center_y - body_radius,
         center_x + body_radius, center_y + body_radius],
        fill=FG_COLOR
    )
    
    # Bug antennae (lines)
    if size >= 32:  # Only draw antennae for larger icons
        antenna_length = body_radius // 2
        draw.line(
            [center_x - body_radius//2, center_y - body_radius,
             center_x - body_radius, center_y - body_radius - antenna_length],
            fill=FG_COLOR, width=max(1, size//32)
        )
        draw.line(
            [center_x + body_radius//2, center_y - body_radius,
             center_x + body_radius, center_y - body_radius - antenna_length],
            fill=FG_COLOR, width=max(1, size//32)
        )
    
    # Add "CC" text for larger icons
    if size >= 48:
        try:
            # Try to use a system font
            font_size = size // 4
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
        
        text = "CC"
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = center_x - text_width // 2
        text_y = center_y - text_height // 2
        draw.text((text_x, text_y), text, fill=TEXT_COLOR, font=font)
    
    # Save icons
    img.save(f"assets/icons/icon-{size}.png")
    img.save(f"dist/assets/icons/icon-{size}.png")

print("Icons created successfully!")
print("Created icons in sizes:", SIZES)

# Also create store assets
store_sizes = {
    "small_promo": (440, 280),
    "large_promo": (920, 680),
    "marquee_promo": (1400, 560),
    "screenshot": (1280, 800)
}

for name, (width, height) in store_sizes.items():
    img = Image.new('RGBA', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Draw centered logo
    logo_size = min(width, height) // 3
    center_x = width // 2
    center_y = height // 2
    
    # Bug body
    body_radius = logo_size // 3
    draw.ellipse(
        [center_x - body_radius, center_y - body_radius,
         center_x + body_radius, center_y + body_radius],
        fill=FG_COLOR
    )
    
    # Add text
    try:
        font_size = logo_size // 4
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        font = ImageFont.load_default()
    
    text = "CCDebugger"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = center_x - text_width // 2
    text_y = center_y + body_radius + 20
    draw.text((text_x, text_y), text, fill=TEXT_COLOR, font=font)
    
    # Add tagline for larger images
    if height >= 560:
        try:
            tagline_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size // 2)
        except:
            tagline_font = font
        
        tagline = "AI-Powered Error Debugging Assistant"
        bbox = draw.textbbox((0, 0), tagline, font=tagline_font)
        tagline_width = bbox[2] - bbox[0]
        tagline_x = center_x - tagline_width // 2
        tagline_y = text_y + text_height + 10
        draw.text((tagline_x, tagline_y), tagline, fill="#cccccc", font=tagline_font)
    
    # Save store assets
    os.makedirs("store_assets", exist_ok=True)
    img.save(f"store_assets/{name}.png")

print("\nStore assets created in store_assets/ directory")