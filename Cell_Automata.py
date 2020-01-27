from PIL import Image
import PIL
import itertools
import random

class CellularAutomata():
    def __init__(self, rule_number, image_size=500, automata_input_bits=3, number_of_colors=2,
                    random_first_row=False):
        # Highest rule number for a set of settings.
        self.maximum_rule_number = rule_number ** (automata_input_bits ** number_of_colors)
        self.automata_input_bits = automata_input_bits
        self.number_of_colors = number_of_colors
        self.random_first_row = random_first_row
        # Proportion the image based on number of bits in `input_size`
        # e.g. for `input_size` 3, make the pic 2:1. For `input_size` 5, it's 4:1
        self.image_size = ((automata_input_bits//2+1)*image_size+2, image_size+1)
        self.rule_number = self.convert_rule_to_base(rule_number)
        self.rule_dictionary = self.create_rule_dictionary()

        self.colors = [(0, 0, 0), (255, 255, 255), (255, 0, 0), (255, 255, 0), (255, 0, 255)]

    # Converts `n` to base `base`, with a maximum value of...
    # ... `maximum_rule_number = number_of_colors ** (automata_input_bits ** number_of_colors)`
    # Anything above that just uses unnecessary computer cycles, as they're...
    # ... equivalent to `rule_number % maximum_rule_number`
    def convert_rule_to_base(self, rule_number):
        if rule_number == 0:
            return ['0'] * (self.number_of_colors**self.automata_input_bits+self.number_of_colors)
        if rule_number > self.maximum_rule_number:
            rule_number = rule_number % self.maximum_rule_number
        nums = []
        # Generate each digit of the new rule number in base
        while rule_number:
            rule_number, remainder = divmod(rule_number, self.number_of_colors)
            nums.append(str(remainder))
            # Complicated. Rule numbers in Cellular Automata are defined by
        new_rule_number = ''.join(nums)[::-1].zfill(self.number_of_colors**self.automata_input_bits+self.number_of_colors)[::-1]
        return new_rule_number

    def create_rule_dictionary(self):
        # list of numbers less than `number_of_colors`. Joined as a String. e.g. `012`
        numbers_in_base = ''.join([str(integer) for integer in range(self.number_of_colors)])
        # `rule_input_keys` is a list of all n-ary digits that are `input_size` in length in order...
        # ... like so: `['000', '001', '002' '020', '021', '022' ...]`
        # We need one key per possible value for each possible input for the CA generation
        rule_input_keys = list(map(''.join, itertools.product(numbers_in_base, repeat=self.automata_input_bits)))

        # Maps the keys produced to the digits of `rule_number`
        return dict(zip(rule_input_keys, self.rule_number))

    def decide_value_by_rule(self, row, cell):
        # Look at the `automata_input_bits` above the cell we want to color and ...
        # ... decide what the value of the cell should be based on `rule_dictionary`
        rule_input = ''.join(self.cellular_automata[row-self.automata_input_bits//2]
                                                   [cell-self.automata_input_bits//2:cell+self.automata_input_bits//2+1])
        value = self.rule_dictionary[rule_input]
        return value

    def create_automata_array(self):
        self.ca_width, self.ca_height = self.image_size
        # First create an array filled with '0's
        self.cellular_automata = [['0' for _ in range(self.ca_width)] for _ in range(self.ca_height)]

        # If we have a randomly assigned first row, randomly decide values for each cell
        if self.random_first_row:
            self.cellular_automata[0] = [random.choice([str(val) for val in range(self.number_of_colors)]) for _ in range(self.ca_width)]
        else:
            # Mark the center pixel as '1' (white) if we don't have a randomly assigned first row
            self.cellular_automata[0][int(self.ca_width//2)+1] = '1'

        # The fun stuff. For each cell in each row, decide what the value should be
        for image_row in range(self.ca_height-1):
            for row_cell in range(self.ca_width - self.automata_input_bits):
                cell_value = self.decide_value_by_rule(image_row+1, row_cell+self.automata_input_bits//2)
                self.cellular_automata[image_row+1][row_cell+1] = cell_value


    def create_automata_image(self):
        self.create_automata_array()

        im = Image.new("RGB", self.image_size, "#000000")
        cellular_automata_image = im.load()
        for image_row in range(self.ca_height-1):
            for row_cell in range(self.ca_width-self.automata_input_bits//2-1):
                cell_value = self.cellular_automata[image_row+1][row_cell+1]
                color = self.colors[int(cell_value)]
                cellular_automata_image[row_cell, image_row+1] = color
        im.save(f"rule{self.rule_number}_{self.automata_input_bits}_bit.png")
        im.show()


def main():
    new_automata = CellularAutomata(110)
    new_automata.create_automata_image()

if __name__ == '__main__':
    main()
