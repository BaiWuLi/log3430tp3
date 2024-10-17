import sys
import os
import random
import url_parser
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Partie-A')))
from random_fuzzer import RandomFuzzer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Partie-B')))
from mutation_fuzzer import MutationFuzzer
from num2words import num2words # pip install num2words


class Coverage:
    def __init__(self):
        self.covered_lines = set()

    def trace(self, frame, event, arg):
        if event == "line":
            code = frame.f_code
            filename = code.co_filename
            lineno = frame.f_lineno
            self.covered_lines.add((filename, lineno))
        return self.trace

    def start(self):
        sys.settrace(self.trace)

    def stop(self):
        sys.settrace(None)

    def coverage(self):
        return self.covered_lines


def calculate_cumulative_coverage(input_population, function):
    cumulative_coverage = []
    all_coverage = set()

    for inp in input_population:
        coverage = Coverage()
        coverage.start()
        try:
            function(inp)
        except Exception:
            pass
        coverage.stop()
        all_coverage |= coverage.coverage()
        cumulative_coverage.append(len(all_coverage))
    return cumulative_coverage


def plot(cumulative_coverages, titles):
    for cumulative_coverage in cumulative_coverages:
        plt.plot(cumulative_coverage)
    plt.legend(titles)
    plt.title('Coverage')
    plt.xlabel('# of inputs')
    plt.ylabel('lines covered')
    plt.show()

# TODO
class CustomFuzzer:
    def __init__(self):
        pass

    def fuzz(self):
        pass

# Exemple de couverture avec MutationFuzzer à modifier pour les tâches de la Partie-C
random_seed = 2192826
random.seed(random_seed)
trials = 500
random_fuzzer = RandomFuzzer()
mutation_fuzzer = MutationFuzzer(seeds=["3452020"])
custom_fuzzer = CustomFuzzer()

random_input_set = [random_fuzzer.fuzz() for _ in range(trials)]
mutation_input_set = [mutation_fuzzer.fuzz() for _ in range(trials)]
custom_input_set = [custom_fuzzer.fuzz() for _ in range(trials)]

random_cumulative_coverage = calculate_cumulative_coverage(
    random_input_set, num2words)
mutation_cumulative_coverage = calculate_cumulative_coverage(
    mutation_input_set, num2words)
custom_fuzzer_cumulative_coverage = calculate_cumulative_coverage(
    custom_input_set, num2words)
plot([random_cumulative_coverage, mutation_cumulative_coverage],
     ['RandomFuzzer', 'MutationFuzzer', 'CustomFuzzer']
)
