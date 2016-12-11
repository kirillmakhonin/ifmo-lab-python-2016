import re


def get_words_from_file(f):
    """
    Get only words from file. Yeah, I'm using regex for first problem set
    :param f: file
    :return: list of str - words
    """
    content = f.read()
    words = re.findall('\w+', content)
    return [word.lower() for word in words]


def get_word_signature(str):
    """
    Calculate signature of annagram as sorted string
    :param str: str - source str
    :return: str signature of string
    """
    return ''.join(sorted(str))


def annagrams():
    with open('annagram_check_test.txt', 'r') as f:
        all_words_set = set(get_words_from_file(f))

        annagrams = dict()

        for word in all_words_set:
            key = get_word_signature(word)
            if key in annagrams:
                annagrams[key].append(word)
            else:
                annagrams[key] = [word]

        good_annagrams = [variants for variants in annagrams.values() if len(variants) > 1]

        for x in good_annagrams:
            print(x)

if __name__ == '__main__':
    annagrams()
