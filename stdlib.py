import fileinput
import re
from collections import *
from functools import partial, reduce
from itertools import *
from pprint import pprint

from more_itertools import *

DEBUG = False


def ints(line):
    return [int(x) for x in re.findall(r"-?\d+", line)]


def read_input(filename="input"):
    return list(line.rstrip("\n") for line in fileinput.input(filename))


def identity(x):
    return x


def inverse_identity(x):
    return not x
