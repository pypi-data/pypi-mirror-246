import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from Source code:
from Source.deltatextsplitter import deltatextsplitter

# Definition of the Run-function:
def deltatextsplitter_fullrun():
    """
    # Function to run everything from deltatextsplitter.
    # Parameters: none (stored in the code & files)
    # Return: none (stored in the class)
    """

    # Generate the class:
    mydelta = deltatextsplitter()

    # Execute the run:
    mydelta.FullRun(False, False)
    # First Argument:  False will switch-off testmode
    # Second Argument: False will skip the full run and use previous excels.

    # Done.

if __name__ == '__main__':
    deltatextsplitter_fullrun()
