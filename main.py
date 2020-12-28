import argparse
import sys
from arg_type import arg_type

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()
    #Determine arg type and handle it
    arg_type(args.file)

if __name__ == "__main__":
    main()