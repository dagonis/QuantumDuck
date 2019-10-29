import argparse

import quantum

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("duckyscript", help="The location of the ducky script you want to translate")
    args = argument_parser.parse_args()
    quantum.DuckScript.create_duckscript_object(args.duckyscript)