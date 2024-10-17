import random
import traceback
import test_script


class RandomFuzzer:
    def __init__(self, min_length=10, max_length=100, char_start=32, char_range=32):
        self.min_length = min_length
        self.max_length = max_length
        self.char_start = char_start
        self.char_range = char_range

    def fuzz(self):
        length = random.randint(self.min_length, self.max_length)
        return ''.join(
            chr(random.randint(self.char_start, self.char_start + self.char_range))
            for i in range(length)
        )


random.seed(123)
random_fuzzer = RandomFuzzer()
trials = 100
for i in range(trials):
    inp = random_fuzzer.fuzz()
    print("trial: %s \ninput: %s" % (i, inp))
    try:
        test_script.crash_if_too_long(inp)
    except ValueError:
        traceback.print_exc()
        break
