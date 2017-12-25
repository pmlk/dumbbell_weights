import argparse
import json


import weights as wt
from weights import Weights


def inventory():
    weight_counts = dict()

    input_string = input("Enter different weights (separated by space, decimal-symbol . ): ")
    string_weights = input_string.split()
    print(string_weights)

    weights = [float(x) for x in string_weights]

    for w in weights:
        count = int(input("How many times do you have {} kg: ".format(w)))
        weight_counts[w] = count

    print(weight_counts)

    with open("weights.json", "w") as jfile:
        jfile.write(json.dumps(weight_counts))


def load_weights():
    weight_counts = dict()
    try:
        with open("weights.json", "r") as jfile:
            tmp_weight_counts = json.loads(jfile.read())
    except FileNotFoundError as e:
        print(e)
        print("run 'inventory' command first")
        exit(e.errno)
        return

    for k, v in tmp_weight_counts.items():
        weight_counts[float(k)] = int(v)

    # print(weight_counts)
    return weight_counts


def configure_weights():
    weight_counts = load_weights()

    weights = Weights(weight_counts)
    weight_objects = [weights]

    possible_total_weights = wt.possible_weights(weight_objects)
    double_weights = wt.possible_double_weights(weight_objects)

    input_weights = []

    keep_going = True
    while len(possible_total_weights) > 1 and keep_going:
        print()
        print("possible total weights:")
        for w in possible_total_weights:
            double_indicator = "  "
            if w in double_weights:
                double_indicator = "* "
            print("{}{:4.1f} kg".format(double_indicator, w))

        while True:
            try:
                # enter any non-number to stop
                total_weight = float(input("choose total weight: "))
                if total_weight in possible_total_weights:
                    input_weights.append(total_weight)
                    break
                print("invalid input")
            except ValueError:
                # non-number entered, stopping
                total_weight = 0
                keep_going = False
                break

        if keep_going:
            weight_objects = wt.reduced_weight_objects(weight_objects, total_weight)
            possible_total_weights = wt.possible_weights(weight_objects)
            double_weights = wt.possible_double_weights(weight_objects)

    #
    print("===========================")
    print("selected weights:")
    print(input_weights)
    print()
    print("weight combos:")
    weight_counts = load_weights()
    weights = Weights(weight_counts)
    if len(input_weights):
        combos = wt.get_combos(weights, input_weights)
        for w, c in combos:
            weight = "{:4.1f} kg".format(w)
            # weights_asc = sorted(c)
            weights_dsc = sorted(c, reverse=True)

            print("{}: {}".format(weight, weights_dsc))


if __name__ == "__main__":

    FUNCTION_MAP = {"inventory": inventory,
                    "config": configure_weights}

    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=FUNCTION_MAP.keys())

    args = parser.parse_args()
    # print(args)

    FUNCTION_MAP[args.command]()
