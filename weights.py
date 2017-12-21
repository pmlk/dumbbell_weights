import copy

import combinations


class Weights(object):

    def __init__(self, weight_counts: dict, dumbbell_weight: float = 2.0):
        self.available_weights = weight_counts
        self.dumbbell_weight = dumbbell_weight

    def symmetric_configs(self, max_weights: int = 3):
        symmetric_weights = dict()

        for k, v in self.available_weights.items():
            symmetric_weights[k] = int(v / 2)

        available_pairs = []
        for k, v in symmetric_weights.items():
            for _ in range(v):
                available_pairs.append(k)
        # print("pairs: {}".format(available_pairs))

        all_configs = list(combinations.generate_all_combinations(available_pairs))

        limited_configs = []
        for combo in all_configs:
            # print(combo)
            if len(combo) <= max_weights:
                # print("adding combo {}".format(combo))
                limited_configs.append(combo)

        return limited_configs

    def weight_configs(self) -> dict:
        weight_configs = dict()

        configs = self.symmetric_configs()

        weight_configs[self.dumbbell_weight] = [[0]]
        for config in configs:
            weight = sum(config) * 2 + self.dumbbell_weight
            if weight not in weight_configs:
                weight_configs[weight] = []
            weight_configs[weight].append(config)

        return weight_configs

    def configs_for_weight(self, weight: float):
        # print("combos for weight: {}".format(weight))
        all_configs = self.weight_configs()
        if weight in all_configs:
            configs = all_configs[weight]
            unique_config = []
            for config in configs:
                if config not in unique_config:
                    unique_config.append(config)
            # print(unique_combos)
            return unique_config
        return []

    def possible_total_weights(self):
        configs = self.weight_configs()

        sorted_configs = [k for k in sorted(configs.keys())]
        return sorted_configs

    def remove_symmetric_config(self, config: [float]):
        # print("removing combo from {}: {}".format(self, combo))
        for weight in config:
            if weight > 0:
                count = self.available_weights[weight]
                count -= 2
                self.available_weights[weight] = count


def reduced_weight_objects(originals: [Weights], total_weight: float):
    reduced_weights = []
    # print("num originals: {}".format(len(originals)))
    for original in originals:
        combos = original.configs_for_weight(total_weight)
        # print("num combos: {}".format(len(combos)))
        for i, combo in enumerate(combos):
            original.remove_symmetric_config(combo)
            # print("combo #{:3}: {}".format(i, combo))
            reduced_weights.append(copy.deepcopy(original))

    # print("num reduced: {}".format(len(reduced_weights)))
    return reduced_weights


def possible_double_weights(weight_objects: [Weights]):
    cp_weight_objects = [copy.deepcopy(w) for w in weight_objects]
    double_weights = []
    single_weights = possible_weights(cp_weight_objects)

    for w in single_weights:
        reduced_weights = reduced_weight_objects([copy.deepcopy(wo) for wo in cp_weight_objects], w)
        s_weights = possible_weights(reduced_weights)
        if w in s_weights:
            double_weights.append(w)
    return double_weights


def possible_weights(weight_objects: [Weights]):

    possible = []
    for weights in weight_objects:
        for weight in weights.possible_total_weights():
            if weight not in possible:
                possible.append(weight)

    return [w for w in sorted(possible)]


def get_combos(weight_object: Weights, total_weights: [float]):
    # print("total weights: {}".format(total_weights))
    combo_of_configs = []

    weight = total_weights[0]
    configs = weight_object.configs_for_weight(weight)
    for config in configs:
        t = (weight, config)
        # print("tuple: {}".format(t))
        if len(total_weights) == 1:
            combo_of_configs.append(t)
            return combo_of_configs

        reduced_objects = reduced_weight_objects([weight_object], weight)
        for r_weight_object in reduced_objects:
            combos = get_combos(r_weight_object, total_weights[1:])
            # print("combos: {}".format(combos))
            if combos:
                for c in combos:
                    combo_of_configs.append(c)

        combo_of_configs.append(t)
        if len(combo_of_configs) == len(total_weights):
            # print("returning")
            return combo_of_configs
    # return combo_of_configs
