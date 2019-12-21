from PIL import Image
import PIL
import itertools
import random

size = 500

rule = 110
# please only input odds. I don't know if/how evens work.
input_size = 3

# turns the rules
size = (2*size+2, size+1)
rule_bin = list(format(rule, f'#0{2**input_size+2}b')[2:])
rule_bin = rule_bin[::-1]
# Produces all binary digits that are `input_size` in length in order...
# ...in a list like so: `['000', '001', '010', '011', ...]`
keys = list(map(''.join, itertools.product('01', repeat=input_size)))

# Maps the keys produced to the digits of `rule_binary`
rule_rules = dict(zip(keys, rule_bin))

width, height = size
cells = [['0' for _ in range(width)] for _ in range(height)]
origin = int(width/2)+1
cells[0][origin] = '1'
#cells[0] = [random.choice(["0","1"]) for _ in range(width)]
colors = [(0, 0, 0), (255, 255, 255)]

def decide_rule(row, cell):
    rule_input = ''.join(cells[row-input_size//2][cell-input_size//2:cell+input_size//2+1])
    val = rule_rules[rule_input]
    return val

for r in range(height-1):
    for c in range(width-input_size):
        cell = decide_rule(r+1, c+input_size//2)
        cells[r+1][c+1] = cell

im = Image.new("RGB", size, "#000000")
pixels = im.load()
for r in range(height-1):
    for c in range(width-input_size//2-1):
        pixels[c, r] = colors[int(cells[r+1][c+1])]
im.save(f"rule{rule}.png")
im.show()
