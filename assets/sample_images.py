"""
Sample Image Generator for Food Verse AI
Generates high-fidelity visual representations of meals, fresh produce,
and kitchen stations for instant testing and demonstration mode.
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np


def get_sample_dish_image(dish_key: str = "paneer_tikka") -> Image.Image:
    """Generates an illustrative meal image for Food Recognition testing."""
    img = Image.new("RGB", (640, 480), color=(250, 248, 245))
    draw = ImageDraw.Draw(img)

    # Ceramic Serving Bowl
    draw.ellipse([80, 60, 560, 420], fill=(240, 238, 233), outline=(190, 180, 170), width=4)
    draw.ellipse([110, 90, 530, 390], fill=(225, 95, 45))  # Rich spiced curry base

    if dish_key == "paneer_tikka":
        # Brown rice bed on the right half
        draw.chord([260, 90, 530, 390], -80, 80, fill=(215, 195, 160))
        # Brown rice texture dots
        for rx, ry in [(350, 180), (390, 220), (430, 260), (370, 300), (450, 190), (410, 320)]:
            draw.ellipse([rx, ry, rx + 14, ry + 6], fill=(175, 150, 115))

        # Charred Paneer Cubes
        paneer_positions = [(180, 180), (240, 230), (170, 280), (250, 150)]
        for px, py in paneer_positions:
            draw.rectangle([px, py, px + 50, py + 45], fill=(255, 250, 235), outline=(160, 80, 20), width=2)
            # Char marks
            draw.line([px + 8, py + 12, px + 42, py + 15], fill=(90, 40, 10), width=3)
            draw.line([px + 10, py + 28, px + 38, py + 32], fill=(90, 40, 10), width=3)

        # Green Bell Pepper Slices
        draw.arc([160, 140, 210, 180], 40, 180, fill=(46, 125, 50), width=6)
        draw.arc([220, 300, 280, 340], 20, 190, fill=(46, 125, 50), width=6)

        # Fresh Cilantro garnish
        for cx, cy in [(280, 210), (290, 205), (310, 220), (275, 230)]:
            draw.ellipse([cx, cy, cx + 10, cy + 10], fill=(46, 125, 50))

        # Title banner on image
        draw.rectangle([0, 0, 640, 44], fill=(30, 41, 59))
        draw.text((20, 12), "Food Verse AI Sample Dish: Paneer Tikka Masala & Brown Rice", fill=(255, 255, 255))

    elif dish_key == "mediterranean_chicken":
        # Quinoa base
        draw.ellipse([110, 90, 530, 390], fill=(210, 190, 155))
        # Grilled chicken strips
        for gx, gy in [(160, 160), (210, 210), (180, 270)]:
            draw.rectangle([gx, gy, gx + 90, gy + 35], fill=(220, 180, 140), outline=(130, 90, 50), width=2)
            draw.line([gx + 15, gy + 5, gx + 25, gy + 30], fill=(80, 40, 20), width=3)
            draw.line([gx + 45, gy + 5, gx + 55, gy + 30], fill=(80, 40, 20), width=3)
            draw.line([gx + 75, gy + 5, gx + 85, gy + 30], fill=(80, 40, 20), width=3)

        # Cherry tomatoes
        for tx, ty in [(360, 160), (410, 190), (370, 230)]:
            draw.ellipse([tx, ty, tx + 35, ty + 35], fill=(220, 40, 40))

        # Cucumber slices
        for kx, ky in [(350, 280), (410, 290), (380, 340)]:
            draw.ellipse([kx, ky, kx + 40, ky + 40], fill=(120, 200, 120), outline=(40, 120, 40), width=3)

        # Feta crumble
        for fx, fy in [(280, 240), (295, 230), (320, 260), (270, 270)]:
            draw.rectangle([fx, fy, fx + 15, fy + 12], fill=(255, 255, 255))

        draw.rectangle([0, 0, 640, 44], fill=(30, 41, 59))
        draw.text((20, 12), "Food Verse AI Sample Dish: Mediterranean Chicken Quinoa Bowl", fill=(255, 255, 255))

    return img


def get_sample_freshness_image(item_key: str = "banana_speckled") -> Image.Image:
    """Generates an illustrative perishable item image for Freshness & Spoilage testing."""
    img = Image.new("RGB", (640, 480), color=(248, 250, 252))
    draw = ImageDraw.Draw(img)

    if item_key == "banana_speckled":
        # Banana yellow curve
        draw.rectangle([0, 0, 640, 44], fill=(30, 41, 59))
        draw.text((20, 12), "Food Verse AI Sample Item: Ripe Cavendish Bananas (Sugar Spots)", fill=(255, 255, 255))

        # Banana arc
        draw.arc([100, 100, 520, 380], 30, 160, fill=(245, 200, 30), width=75)
        # Green tip
        draw.arc([460, 180, 530, 250], 30, 90, fill=(120, 175, 50), width=50)
        # Brown stem
        draw.rectangle([110, 230, 135, 265], fill=(100, 70, 30))

        # Senescent sugar spots (browning dots)
        np.random.seed(42)
        for _ in range(85):
            angle = np.random.uniform(0.6, 2.5)
            r = np.random.uniform(160, 200)
            cx = int(310 + r * np.cos(angle))
            cy = int(240 + r * np.sin(angle) * 0.7)
            spot_r = np.random.randint(2, 6)
            draw.ellipse([cx - spot_r, cy - spot_r, cx + spot_r, cy + spot_r], fill=(95, 55, 25))

        draw.text((160, 420), "Visible Characteristics: Prominent melanin sugar freckles (~35% peel coverage)", fill=(80, 80, 80))

    elif item_key == "fresh_strawberries":
        draw.rectangle([0, 0, 640, 44], fill=(30, 41, 59))
        draw.text((20, 12), "Food Verse AI Sample Item: Fresh Ripe Strawberries", fill=(255, 255, 255))

        # Strawberry body
        draw.polygon([(320, 380), (220, 190), (420, 190)], fill=(225, 25, 35))
        draw.ellipse([210, 160, 330, 220], fill=(225, 25, 35))
        draw.ellipse([310, 160, 430, 220], fill=(225, 25, 35))

        # Green Calyx (Leaves)
        draw.polygon([(320, 150), (280, 120), (310, 165)], fill=(34, 139, 34))
        draw.polygon([(320, 150), (360, 120), (330, 165)], fill=(34, 139, 34))
        draw.polygon([(320, 150), (320, 110), (320, 165)], fill=(34, 139, 34))

        # Golden Achenes (Seeds)
        for sx in range(250, 400, 24):
            for sy in range(190, 350, 22):
                if 220 < sx < 420 and sy > 170:
                    draw.ellipse([sx, sy, sx + 4, sy + 6], fill=(250, 230, 140))

        draw.text((180, 420), "Visible Characteristics: Firm turgid skin, vibrant scarlet red, crisp calyx", fill=(80, 80, 80))

    elif item_key == "spoiled_poultry":
        draw.rectangle([0, 0, 640, 44], fill=(30, 41, 59))
        draw.text((20, 12), "Food Verse AI Sample Item: Spoiled Raw Poultry (Slime & Discoloration)", fill=(255, 255, 255))

        # Grayish-green fillet
        draw.ellipse([140, 140, 500, 360], fill=(175, 170, 155), outline=(120, 130, 110), width=3)
        # Slimy exudate patches
        draw.ellipse([220, 180, 380, 290], fill=(160, 175, 145))
        draw.ellipse([340, 240, 440, 320], fill=(145, 160, 135))
        draw.text((150, 420), "Visible Characteristics: Biofilm slime sheen, grayish-green metmyoglobin discoloration", fill=(180, 40, 40))

    return img


def get_sample_kitchen_image() -> Image.Image:
    """Generates an illustrative commercial kitchen station image."""
    img = Image.new("RGB", (640, 480), color=(235, 240, 245))
    draw = ImageDraw.Draw(img)

    # Stainless Steel Prep Counter
    draw.rectangle([30, 180, 610, 420], fill=(205, 215, 222), outline=(140, 150, 160), width=3)
    # Counter reflection highlight
    draw.line([32, 190, 608, 190], fill=(245, 250, 255), width=2)

    # Station 1: Raw Poultry Cutting Board (YELLOW / DANGER ZONE)
    draw.rectangle([60, 220, 260, 370], fill=(255, 230, 120), outline=(200, 160, 40), width=2)
    # Raw poultry pieces
    draw.ellipse([80, 250, 160, 310], fill=(240, 180, 175), outline=(210, 140, 135), width=2)
    draw.ellipse([150, 280, 230, 340], fill=(240, 180, 175), outline=(210, 140, 135), width=2)
    draw.text((70, 225), "Board 1: Raw Poultry", fill=(120, 60, 0))

    # HAZARD WARNING ARROW / CALLOUT
    draw.rectangle([250, 265, 330, 295], fill=(239, 68, 68))
    draw.text((258, 272), "15cm GAP!", fill=(255, 255, 255))

    # Station 2: Ready-to-Eat Produce Board (GREEN / SALAD)
    draw.rectangle([320, 220, 580, 370], fill=(210, 245, 210), outline=(60, 150, 60), width=2)
    # Chopped romaine lettuce & cucumber
    draw.ellipse([340, 250, 430, 330], fill=(46, 125, 50))
    draw.ellipse([450, 260, 520, 330], fill=(139, 195, 74))
    draw.ellipse([480, 300, 540, 350], fill=(220, 50, 40)) # Cherry tomatoes
    draw.text((330, 225), "Board 2: Fresh Salad Produce", fill=(20, 90, 20))

    # Header Bar
    draw.rectangle([0, 0, 640, 50], fill=(30, 41, 59))
    draw.text((20, 15), "Commercial Kitchen Hygiene Audit: Cross-Contamination Risk Scene", fill=(255, 255, 255))
    draw.text((30, 435), "Observable Issue: Yellow poultry board placed adjacent to green produce board (<1 meter)", fill=(200, 50, 50))

    return img
