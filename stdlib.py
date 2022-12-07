import fileinput
import re
from more_itertools import *
from pprint import pprint
from collections import *
from itertools import *


def ints(line):
    return [int(x) for x in re.findall(r'-?\d+', line)]


def read_input(filename="input"):
    return list(line.rstrip("\n") for line in fileinput.input(filename))


def identity(x):
    return x
