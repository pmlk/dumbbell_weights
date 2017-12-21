

def generate_two_different(choices: [any]):
    for i, c1 in enumerate(choices):
        for j, c2 in enumerate(choices):
            if j > i:
                yield c1, c2


def generate_all_combinations(choices: [any]):
    for i, c1 in enumerate(choices):
        combination = [c1]
        yield combination.copy()

        tmp_combination = combination.copy()
        for combo in generate_all_combinations(choices[i+1:]):
            combination.extend(list(combo))
            yield combination.copy()
            combination = tmp_combination.copy()


def generate_combos_one_of_each(**kwargs) -> dict:
    # print(kwargs)
    keys = set(kwargs.keys())
    if len(keys) > 0:
        key = keys.pop()
        values = kwargs.pop(key)
        assert type(values) is list
        d = {}
        for v in values:
            d[key] = v
            # print(d)
            if len(kwargs.keys()) > 0:
                for d2 in generate_combos_one_of_each(**kwargs):
                    # print(d2)
                    d.update(d2)
                    yield d.copy()
            else:
                yield d.copy()
