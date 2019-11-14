import argparse

import quantum

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("duckyscript", help="The location of the ducky script you want to translate")
    argument_parser.add_argument("--full", action="store_true", help="Toggle this to get extra QMK configuration.")
    argument_parser.add_argument("--name", "-n", default="QuantumDuck", help="The name of the Macro key.")
    args = argument_parser.parse_args()
    duck_to_qmk = quantum.DuckScript.create_duckscript_object(args.duckyscript)
    if args.full:
        duck_to_qmk.full_output(args.name)
    else:
        print(duck_to_qmk)