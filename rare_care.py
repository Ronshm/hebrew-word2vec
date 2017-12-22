from collections import Counter
from utils import *
from os.path import join

path = "result/w2v-nn-pos-10"


# create word and pos list&dict.
def create_rare_words_list():
    with open('data/wikipedia.deps', 'r') as fin:
        words = []
        for i, line in enumerate(fin):
            if i % 1000000 == 0:
                print i
            tab = compat_splitting(line)
            if len(tab) > 2:
                words.append(tab[1])
    print "done reading_data."

    counter = Counter(words)

    with open(join(path, "words_list.txt"), 'r') as f:
        words = f.readlines()
    words = [word[:-1] for word in words]
    i = 0
    with open(join(path,"rare_words_10.txt"), 'wb') as f:
        for word in words:
            if counter[word] < 10:
                print "here", counter[word]
                f.write(word + "\n")
                i += 1
            else:
                print word, counter[word]
    print i
    print "rare list created."


def get_context_vec(context_words):
    context_vec = np.zeros(10)

    pass


create_rare_words_list()
