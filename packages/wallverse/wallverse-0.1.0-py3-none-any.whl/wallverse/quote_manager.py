import os
import random
import sys

import arabic_reshaper
import cowsay
from bidi.algorithm import get_display

from wallverse.database import DataBase
from importlib.resources import files


def resource_path(file_name):
    return files('wallverse').joinpath(file_name)


def wider_cowsay_wrap_lines(lines, max_width=90):
    """Here, because the cowsay package has a default max_width of 49 for its wrap_line function, I'm using
     Monkey Patching to increase the max_width to 90 to prevent distortions. """
    new_lines = []
    for line in lines:
        for line_part in [
            line[i:i + max_width] for i in range(0, len(line), max_width)
        ]:
            new_lines.append(line_part)
    return new_lines


# Replacing cowsay function with a custom one.
cowsay.main.wrap_lines = wider_cowsay_wrap_lines


class QuoteGen:
    def __init__(self):
        self.db = DataBase()
        self.random_quote = None
        self.cowsay_string = None
        self.quote_pack = None

    def get_random_quote(self):
        random_quote = None
        if self.quote_pack == "custom":
            filepath = resource_path(os.path.join("ui_resources", "custom.txt"))
            with open(filepath, encoding="utf-8") as file:
                file_data = file.read().split("%")
                if file_data[0].strip():
                    random_quote = random.choice(file_data)
                else:
                    return "Textbox is empty!"
        else:
            random_quote = self.db.fetch_random_quote(self.quote_pack)
        reshaped_text = arabic_reshaper.reshape(random_quote)
        bidirectional_text = get_display(reshaped_text)
        self.random_quote = bidirectional_text.replace('\t', '    ')
        return self.random_quote

    def set_quote_pack(self, quote_pack):
        self.quote_pack = quote_pack

    def pass_to_cowsay(self, input_text=None, cowsay_character="cow"):
        self.cowsay_string = cowsay.get_output_string(char=cowsay_character, text=input_text)
        return self.cowsay_string
