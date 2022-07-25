# Problem 98:
#     Anagramic Squares
#
# Description:
#     By replacing each of the letters in the word CARE with 1, 2, 9, and 6 respectively,
#       we form a square number:
#         1296 = 36^2.
#
#     What is remarkable is that, by using the same digital substitutions,
#       the anagram, RACE, also forms a square number:
#         9216 = 96^2.
#
#     We shall call CARE (and RACE) a square anagram word pair
#       and specify further that leading zeroes are not permitted,
#       neither may a different letter have the same digital value as another letter.
#
#     Using words.txt (right click and 'Save Link/Target As...'),
#       a 16K text file containing nearly two-thousand common English words,
#       find all the square anagram word pairs (a palindromic word is NOT considered to be an anagram of itself).
#
#     What is the largest square number formed by any member of such a pair?
#
#     NOTE: All anagrams formed must be contained in the given text file.

from collections import defaultdict
from math import floor, sqrt
from typing import DefaultDict, Set, Tuple


def get_anagramic_words(filename: str) -> DefaultDict[int, DefaultDict[str, Set[str]]]:
    """
    Given a `filename` containing a list of common words,
      groups the words together into equivalence classes of sets of anagramic word
      further split up by word length.

    Args:
        filename (str): Name of file containing list of common words

    Returns:
        (defaultdict[int, defaultdict[str, Set[str]]]):
            Map of (word_size)
              -> Map of (anagram_set_key)
                -> Set of anagramic words

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(filename) == str

    # Read words from single line in file
    with open(filename, 'r') as f:
        words = list(map(lambda s: s.strip('"').upper(), f.readline().strip().split(',')))

    # Group together any anagrams from among the words
    anagram_sets = defaultdict(lambda: defaultdict(set))  # `word size` -> `sorted word` -> `set of anagramic words`
    anagram_singletons = set()  # Set of non-anagramic words

    for word in words:
        # Add word to equivalence class denoted by its sorted form
        word_sorted = ''.join(sorted(word))
        word_size = len(word_sorted)
        anagram_sets[word_size][word_sorted].add(word)

        # Keep track of singletons
        word_set_size = len(anagram_sets[word_size][word_sorted])
        if word_set_size == 2:
            anagram_singletons.discard(word_sorted)
        elif word_set_size == 1:
            anagram_singletons.add(word_sorted)
        else:
            pass

    # Purge all the anagramic singletons, as we don't need them
    for anagram_singleton in anagram_singletons:
        anagram_size = len(anagram_singleton)
        anagram_sets[anagram_size].pop(anagram_singleton)
        if len(anagram_sets[anagram_size]) == 0:
            anagram_sets.pop(anagram_size)

    return anagram_sets


def get_anagramic_squares(d_max: int) -> DefaultDict[int, DefaultDict[str, Set[str]]]:
    """
    Calculates and groups together anagramic sets of square numbers
      having at most `n` digits.

    Args:
        d_max (int): Maximum digit-count of square numbers to consider

    Returns:
        (defaultdict[int, defaultdict[str, Set[str]]]):
            Map of (digit_count)
              -> Map of (square_set_key)
                -> Set of anagramic squares

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(d_max) == int and d_max > 0

    # Group together any anagrams from among the squares
    anagram_sets = defaultdict(lambda: defaultdict(set))  # `sqr size` -> `sorted sqr` -> `set of anagramic sqrs`
    anagram_singletons = set()  # Set of non-anagramic sqrs
    for x in range(1, floor(10**(d_max/2))+1):
        square_str = str(x**2)
        square_sorted = ''.join(sorted(list(square_str)))
        square_size = len(square_sorted)
        anagram_sets[square_size][square_sorted].add(square_str)

        # Keep track of singletons
        square_set_size = len(anagram_sets[square_size][square_sorted])
        if square_set_size == 2:
            anagram_singletons.discard(square_sorted)
        elif square_set_size == 1:
            anagram_singletons.add(square_sorted)
        else:
            pass

    # Purge all the anagramic singletons, as we don't need them
    for anagram_singleton in anagram_singletons:
        anagram_size = len(anagram_singleton)
        anagram_sets[anagram_size].pop(anagram_singleton)
        if len(anagram_sets[anagram_size]) == 0:
            anagram_sets.pop(anagram_size)

    return anagram_sets


def main(filename: str) -> Tuple[Tuple[str, int, int], Tuple[str, int, int]]:
    """
    Returns the square anagram word pair using words in `filename`
      for which the largest square number is included as a member.

    Args:
        filename (str): Name of file containing list of common words

    Returns:
        (Tuple[Tuple[str, int, int], Tuple[str, int, int]]):
            2-Tuple of square anagram word pair, where each word is a tuple of ...
              * (str) Word of pair
              * (int) Root of relevant square
              * (int) Square number

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(filename) == str

    # Find all the anagrams in the file
    anagramic_words = get_anagramic_words(filename)

    # All anagramic words
    words = [w for v1 in anagramic_words.values() for v2 in v1.values() for w in v2]

    # Find all the relevant anagramic square numbers
    anagramic_squares = get_anagramic_squares(max(anagramic_words))

    # Squares partitioned by digit-count
    squares_by_size = {k: {v3 for v2 in v1.values() for v3 in v2} for k, v1 in anagramic_squares.items()}

    # Find all square anagram words pairs
    s_best = 0
    p_best = None
    for w1 in words:
        ws = ''.join(sorted(list(w1)))

        # Consider all squares of length matching word
        n = len(w1)
        for s1 in squares_by_size.get(n, {}):
            # Create mapping between (chars in `w1`) <--> (digits in `s1`)
            b = dict(zip(list(w1), list(s1)))
            b_inv = dict(zip(list(s1), list(w1)))

            # Check if mapping is a bijection
            if len(b) < n or len(b_inv) < n:
                continue
            else:
                # Look for anagramic word which is also anagramic square
                for w2 in anagramic_words[n][ws]:
                    if w2 == w1:
                        continue
                    else:
                        s2 = ''.join(map(lambda c: b[c], list(w2)))
                        if s2 in squares_by_size[len(s2)]:
                            s1 = int(s1)
                            s2 = int(s2)
                            s = max(s1, s2)
                            if s > s_best:
                                s_best = s
                                p_best = ((w1, s1), (w2, s2))
                        else:
                            continue

    (w1, s1), (w2, s2) = p_best
    return (w1, int(sqrt(s1)), s1), (w2, int(sqrt(s2)), s2)


if __name__ == '__main__':
    common_words_filename = 'words.txt'
    (common_word_1, root_1, square_1), (common_word_2, root_2, square_2) = main(common_words_filename)
    print('Square anagram word pair in `{}` containing largest square number:'.format(common_words_filename))
    print('  {} -> {} -> {} ^ 2'.format(common_word_1, square_1, root_1))
    print('  {} -> {} -> {} ^ 2'.format(common_word_2, square_2, root_2))
