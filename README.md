# [Flo-v-ver](https://github.com/Gagan163264/Flo-v-ver.git)

C code profiler to report instances of errors in floating point computation
## Setup
Download all files using 

`git clone https://github.com/Gagan163264/Flo-v-ver.git`

Python 3 is required, gcc might be required for its preprocessor

Additionally, the python binding for the Z3 SMT solver has to be installed with

`pip install z3-solver`

## Usage
To run navigate to directory and run main.py in terminal

`python3 main.py`

to open up a shell-style prompt

## Arguments and flags
Arguments:
- cmd : Command input, 'show' to show overview of file, 'run' to run profiler, 'q'/'exit' to quit
- filename : Path to input file, test/sine.c by default
Flags:
- -h or --help : help
- -f or --fname : Sets name of function to be analyzed (main by default)
- -li : Sets number of loop iterations before termination (200 by default)
- -p: Sets Z3 variable precision (200 by default)
- -l : Prints loop debug info (assertion checking)
- --showtree : Print the syntax tree
- -v : Verbose

