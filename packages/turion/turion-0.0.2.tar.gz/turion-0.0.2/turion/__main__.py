import argparse

from .turion import Turion

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--image", dest="image", default="", help="Image")

config = parser.parse_args()

turion = Turion()
