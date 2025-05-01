from PIL import Image, ImageDraw
import random
import math

# Generate a random DNA sequence
def generate_dna(length=30):
    return ''.join(random.choice('ATCG') for _ in range(length))

# Convert DNA bases to angles and branching behavior
def dna_to_angles(dna):
    angle_map = {'A': 20, 'T': -20, 'C': 30, 'G': -30}
    return [angle_map[base] for base in dna]

# Leaf colors by base
leaf_colors = {
    'A': 'lightgreen',
    'T': 'lightblue',
    'C': 'pink',
    'G': 'orange'
}

# Draw a leaf
def draw_leaf(draw, x, y, angle, base, size=10):
    angle_rad = math.radians(angle)
    dx = size * math.cos(angle_rad)
    dy = size * math.sin(angle_rad)
    x1, y1 = x - dx, y - dy
    x2, y2 = x + dx, y + dy
    left = min(x1, x2)
    right = max(x1, x2)
    top = min(y1, y2)
    bottom = max(y1, y2)
    draw.ellipse([left, top, right, bottom], fill=leaf_colors.get(base, 'gray'), outline='darkgreen')

# Recursive branching
def draw_branch(draw, x, y, angle, depth, dna, index):
    if depth == 0 or index >= len(dna):
        return

    base = dna[index]
    angle_change = dna_to_angles(dna)[index]
    angle += angle_change

    length = 30 - depth * 2
    x2 = x + length * math.cos(math.radians(angle))
    y2 = y + length * math.sin(math.radians(angle))

    # Draw main stem
    draw.line((x, y, x2, y2), fill='green', width=2)
    draw_leaf(draw, x2, y2, angle + 90, base)

    # Branches
    draw_branch(draw, x2, y2, angle + 30, depth - 1, dna, index + 1)
    draw_branch(draw, x2, y2, angle - 30, depth - 1, dna, index + 1)

# Create the image with background
img = Image.new('RGB', (800, 800), 'lightyellow')
draw = ImageDraw.Draw(img)

# Draw background ground
draw.rectangle([0, 700, 800, 800], fill='saddlebrown')  # Soil
draw.rectangle([0, 0, 800, 700], fill='lightcyan')      # Sky

# Starting point
x, y = 400, 700
angle = -90

dna = generate_dna(20)
draw_branch(draw, x, y, angle, depth=5, dna=dna, index=0)

# Save the image
img.save("dna_plant_with_branches.png")
print("Branched DNA plant created with colored leaves and themed background!")
