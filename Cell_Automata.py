from PIL import Image
import PIL
import itertools

size = 1000
rule = 90

# Initialization of items
size = (2*size+2, size+1)
rule_bin = list(format(rule, '#010b')[2:])[::1]
keys = list(map(''.join, itertools.product('01', repeat=3)))
rule_rules = dict(zip(keys, rule_bin))

width, height = size
cells = [['0' for _ in range(width)] for _ in range(height)]
origin = int(width/2)+1
cells[0][origin] = '1'

# For a `0`, black is returned. For a `1`, white is returned
colors = [(0, 0, 0), (255, 255, 255)]

def decide_rule(row, cell):
    rule_input = ''.join(cells[row-1][cell-1:cell+2])
    val = rule_rules[rule_input]
    return val

# Construct table with rules
for r in range(height-1):
    for c in range(width-2):
        cell = decide_rule(r+1, c+1)
        cells[r+1][c+1] = cell

# Create Image
im = Image.new("RGB", size, "#000000")
pixels = im.load()
for r in range(height-1):
    for c in range(width-2):
        pixels[c, r] = colors[int(cells[r+1][c+1])]
im.show()
