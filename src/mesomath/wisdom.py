import random

from mesomath import Bwei
from mesomath.glyphs import subsdict




def get_scribal_wisdom():
    quotes = [
        "Transcribing tablets from the Paleobabylonian period...",
        "Calculating the reciprocity of a regular number...",
        "In the tradition of the Edubba School...",
        "Consulting the records of the library of Nippur...",
        "Adjusting the sexagesimal point...",
        "Measuring grain rations according to the standard of Umma...",
    ]
    return f" >> {random.choice(quotes)}"


def get_silver_payment():
    payment = Bwei(random.randrange(1000, 6000))
    return payment.cuneiform + " " + subsdict["ku_babbar"]

