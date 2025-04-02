import argparse
from collections import defaultdict


class Wordle:

    def __init__(self, dictionary: str, word_length: int):
        self._word_length = word_length
        self._words = []
        self._load_words(dictionary, word_length)
        self._scores = []
        self._valid = [[chr(x) for x in range(97, 123)] for _ in range(word_length)]

    def _load_words(self, dictionary_file: str, word_length: int):
        with open(dictionary_file, 'r') as f:
            for line in f:
                line = line.lower().strip()
                if len(line) == word_length:
                    self._words.append(line)

    def _get_letter_frequency(self) -> dict:
        freq = defaultdict(lambda: 0)
        for word in self._words:
            for letter in word:
                freq[letter] += 1
        return freq

    def _get_scores(self):
        freq = self._get_letter_frequency()
        for word in self._words:
            score = 0
            for letter in word:
                score += freq[letter]
            score /= len(word) - len(set(word)) + 1
            self._scores.append((word, score))

    def is_valid(self, word: str, yellows=None, check_yellows=False) -> bool:
        if yellows is None:
            yellows = []
        for i, letter in enumerate(word):
            if letter not in self._valid[i]:
                return False
        if check_yellows:
            for letter in yellows:
                if letter not in word:
                    return False
        return True

    def play(self, hard=False):
        self._get_scores()
        self._scores.sort(key=lambda x: x[1], reverse=True)

        yellows = []
        while True:

            print(" - ".join(list(map(lambda x: x[0], self._scores))[:10]))

            guess = input("Parola inserita: ")
            guess = guess.lower().strip()

            output = input("Risultato: ")
            output = output.lower().strip()

            for i, o in enumerate(output):
                if o == 'g':
                    self._valid[i] = [guess[i]]
                elif o == 'y':
                    yellows.append(guess[i])
                    if guess[i] in self._valid[i]:
                        self._valid[i].remove(guess[i])
                elif o == 'b':
                    if guess[i] in yellows:
                        self._valid[i].remove(guess[i])
                    else:
                        for j in range(len(self._valid)):
                            if guess[i] in self._valid[j]:
                                self._valid[j].remove(guess[i])

            self._scores = list(
                filter(lambda x: self.is_valid(x[0], yellows=yellows, check_yellows=hard), self._scores))


parser = argparse.ArgumentParser()
parser.add_argument('--dict', default='words.txt',help="Dictionary file")
parser.add_argument('--len', default=5, type=int, help="Word length")
args=parser.parse_args()
w = Wordle(args.dict, args.len)
w.play(True)
