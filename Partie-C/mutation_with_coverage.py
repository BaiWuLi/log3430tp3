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

class CustomFuzzer:
    def __init__(self, min_base=0, max_base=9, min_digits=1, max_digits=5):
        self.min_base = min_base
        self.max_base = max_base
        self.min_digits = min_digits
        self.max_digits = max_digits
        self.multipliers = [10**i for i in range(0, 6)]
        self.random_fuzzer = RandomFuzzer()
        
    def make_choice(self, true_prob, false_prob):
        return random.choices([True, False], [true_prob, false_prob])[0]

    def generate_complex_number(self):
        num_digits = random.randint(self.min_digits, self.max_digits)
        digits = [str(random.randint(self.min_base, self.max_base)) for _ in range(num_digits)]
        complex_number = int(''.join(digits))
        return complex_number

    def fuzz(self):
        use_random_fuzzer = self.make_choice(0.05, 0.95)

        if use_random_fuzzer:
            result = self.random_fuzzer.fuzz()
        else:
            base = self.generate_complex_number()
            multiplier = random.choice(self.multipliers)
            multiply = self.make_choice(0.5, 0.5)
            negative = self.make_choice(0.5, 0.5)

            if multiply:
                result = base * multiplier
            else:
                result = base / multiplier

            result *= -1 if negative else 1
            
            make_list = self.make_choice(0.05, 0.95)
            if make_list:
                result = [result]

            to_str = self.make_choice(0.5, 0.5)
            if to_str:
                result = str(result)
            
        return result

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
plot([random_cumulative_coverage, mutation_cumulative_coverage, custom_fuzzer_cumulative_coverage],
     ['RandomFuzzer', 'MutationFuzzer', 'CustomFuzzer']
)
