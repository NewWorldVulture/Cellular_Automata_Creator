from PIL import Image
import PIL
import itertools
import random
import math

size = 500
rule = 23976

# please only input odds. Evens don't work how I want them to yet
input_size = 5
number_of_colors = 3

# turns the rules
size = ((input_size//2+1)*size+2, size+1)

def convert_to_base(n, base):
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, base)
        nums.append(str(r))
    return ''.join(nums)[::-1].zfill(number_of_colors**input_size+number_of_colors)[::-1]

rule_in_base = list(convert_to_base(rule, number_of_colors))

# Produces all n-ary digits that are `input_size` in length in order...
# ...into a list like so: `['000', '001', '010', '011', ...]`
numbers = ''.join([str(x) for x in range(number_of_colors)])
keys = list(map(''.join, itertools.product(numbers, repeat=input_size)))

# Maps the keys produced to the digits of `rule_binary`
rule_rules = dict(zip(keys, rule_formatted))

width, height = size
cells = [['0' for _ in range(width)] for _ in range(height)]
origin = int(width/2)+1
cells[0][origin] = '1'
#cells[0] = [random.choice(["0","1"]) for _ in range(width)]
colors = [(0, 0, 0), (255, 255, 255), (255, 0, 0), (255, 255, 0), (255, 0, 255)]

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
im.save(f"rule{rule}_{input_size}_bit.png")
im.show()
