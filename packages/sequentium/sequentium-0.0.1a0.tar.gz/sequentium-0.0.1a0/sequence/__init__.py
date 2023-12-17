from sequence.sequences.integer.explicit import *
from sequence.sequences.integer.finite import *
from sequence.sequences.integer.periodic import *
from sequence.sequences.integer.property_defined import *
from sequence.sequences.integer.recursive import *

__version__ = '0.0.1a'

from sequence.cli.cli import CommandLineInterface


def main():
    CommandLineInterface().execute()


if __name__ == '__main__':
    main()
