import random
import url_parser


class MutationFuzzer:
    def __init__(self, seeds, mutation_rate=0.1):
        self.seeds = seeds
        self.mutation_rate = mutation_rate

    def mutate(self, inp):
        input_list = list(inp)

        for i in range(len(input_list)):
            if random.random() < self.mutation_rate:
                input_list[i] = chr(random.randint(32, 126))

        return ''.join(input_list)

    def fuzz(self):
        seed = random.choice(self.seeds)
        return self.mutate(seed)


random.seed(123)
seed = "https://www.polymtl.ca"
mutation_fuzzer = MutationFuzzer([seed])

valid_inputs = set()
trials = 40

for i in range(trials):
    inp = mutation_fuzzer.fuzz()
    print("input " + inp)
    if url_parser.is_valid_url(inp):
        valid_inputs.add(inp)

percentage_of_valid_url = (len(valid_inputs) / trials)*100

print("%s of the generated inputs are valid URLs" % percentage_of_valid_url)
