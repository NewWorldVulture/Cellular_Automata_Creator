from PIL import Image
import PIL
import itertools
import random


class CellularAutomata():
    def __init__(self, rule_number, automata_input_bits=3, number_of_colors=2,
                    random_first_row=False, verbose=True, img_width=900, img_height=300):
        # Highest rule number for a set of settings.
        self.maximum_rule_number = number_of_colors ** (number_of_colors ** automata_input_bits)
        self.automata_input_bits = automata_input_bits
        self.number_of_colors = number_of_colors
        self.random_first_row = random_first_row
        self.verbose = verbose
        # Proportion the image based on number of bits in `input_size`
        # e.g. for `input_size` 3, make the pic 2:1. For `input_size` 5, it's 4:1
        self.image_size = (img_width, img_height)
        self.ca_width, self.ca_height = img_width, img_height

        self.rule_number = self._convert_rule_to_base(rule_number)
        self.rule_dictionary = self._create_rule_dictionary()

        self.colors = [(0, 0, 0), (255, 255, 255), (0, 200, 60), (255, 255, 0), (255, 0, 255), (255, 0, 0)]


    # Converts `rule_number` to target base `number_of_colors`, with a maximum value of...
    # ... `maximum_rule_number = number_of_colors ** (number_of_colors ** automata_input_bits)`
    # Anything above that just uses unnecessary computer cycles, as they're...
    # ... equivalent to `rule_number % maximum_rule_number`
    def _convert_rule_to_base(self, rule_number):
        if self.verbose:
            print(f"Rule number input:\n{rule_number}\n")
            print(f"Maximum rule number is:\n{self.maximum_rule_number}\n")
        # Treat 0 as special otherwise we're dividing by 0
        if rule_number == 0:
            # Return a number that's just the length of
            return ''.join(['0'] * (self.number_of_colors ** self.automata_input_bits))
        if rule_number > self.maximum_rule_number:
            rule_number = rule_number % self.maximum_rule_number
            if self.verbose:
                print(f"Converting rule to proper base. Smallest equivalent rule:\n{rule_number}\n")
        # We will generate the new rule one digit at a time, so we'll add the digits to a list
        new_rule_number_digits = []
        # Generate each digit of the new rule number in the target base
        while rule_number:
            rule_number, remainder = divmod(rule_number, self.number_of_colors)
            new_rule_number_digits.append(str(remainder))
        
        # Complicated. Rule numbers in Cellular Automata are defined by the following
        new_rule_number = ''.join(new_rule_number_digits)[::-1].zfill(self.number_of_colors**self.automata_input_bits)
        if self.verbose:
            print(f"In-base Rule number:\n{new_rule_number}")
        return new_rule_number


    # Returns a dictionary of possible inputs to the digits of
    def _create_rule_dictionary(self):
        # list of numbers less than `number_of_colors`. Joined as a String. e.g. `012`
        numbers_in_base = ''.join([str(integer) for integer in range(self.number_of_colors)])
        # `rule_input_keys` is a list of all n-ary digits that are `input_size` in length in decreasing order...
        # ... like so: `['222', '221', '220' '212' '211' '210' '202', '201', '200' ...]`
        # We need one key to match to each  value for each possible input for the CA generation
        rule_input_keys = list(map(''.join, itertools.product(numbers_in_base, repeat=self.automata_input_bits)))[::-1]

        # Maps the keys produced to the digits of `rule_number`
        return dict(zip(rule_input_keys, self.rule_number))


    def _decide_value_by_rule(self, row, cell_index):
        # First cell being used as input
        p_cell = cell_index - self.automata_input_bits//2

        # 
        rule_input = "".join([row[j % len(row)] for j in range(p_cell, p_cell + self.automata_input_bits)])
        
        # Look at the `automata_input_bits` above the cell we want to color and ...
        # ... decide what the value of the cell should be based on `rule_dictionary`
        value = self.rule_dictionary[rule_input]
        return value


    def create_automata_image(self):
        # Create a row of '0's as a seed row
        prev_row = ['0' for _ in range(self.ca_width + 1)]

        # If we have a randomly assigned first row, randomly decide values for each cell
        if self.random_first_row:
            prev_row = [random.choice([str(val) for val in range(self.number_of_colors)]) for _ in range(self.ca_width+1)]
        else:
            # Mark the center pixel as '1' (white) if we don't have a randomly assigned first row.
            prev_row[int(self.ca_width//2) + 1] = '1'

        im = Image.new("RGB", self.image_size, "#000000")
        cellular_automata_image = im.load()
        # Create image row by row
        for image_row in range(self.ca_height):
            new_row = [self._decide_value_by_rule(prev_row, cell_index) for cell_index in range(len(prev_row))]
            for row_cell in range(self.ca_width-self.automata_input_bits//2-1):
                cell_color = self.colors[int( new_row[row_cell] )]
                cellular_automata_image[row_cell, image_row] = cell_color
            prev_row = new_row
        im.save(f"rule{self.rule_number}_{self.automata_input_bits}_bit{'_r'*self.random_first_row}.png")
        im.show()


def main():
    new_automata = CellularAutomata(30921345333, 5, 2, False, True)
    new_automata.create_automata_image()

if __name__ == '__main__':
    main()
