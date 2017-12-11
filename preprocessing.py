import sys
from utils import *
import numpy as np
from collections import Counter

reload(sys)
sys.setdefaultencoding('utf-8')


def write_word(f_word, f_pos):
    if '-' in f_word:
        # print "- char", f_word
        f_word.replace('-', '~')
    if w2i[f_word] in problematic_words_idx:
        if f_pos in ["NNT", "NNP"]:
            f_pos = "NN"
        fout.write(f_pos + "_" + f_word + ' ')
    else:
        fout.write(f_word + ' ')


# create word and pos list&dict.
with open('data/wikipedia.deps', 'r') as fin:
    words = set([])
    pos = set([])
    i = 0
    for _, line in enumerate(fin):
        i += 1
        if i % 1000000 == 0:
            print i
        tab = compat_splitting(line)
        if len(tab) > 2:
            words.add(tab[1])
            pos.add(tab[3])
words_set = set(words)
pos_set = set(pos)

w2i = {word: i for i, word in enumerate(words_set)}
i2w = {i: word for i, word in enumerate(words_set)}
p2i = {part: i for i, part in enumerate(pos_set)}
i2p = {i: part for i, part in enumerate(pos_set)}
print p2i['NNP']
print "done reading_data."
# counter of instances of each pos.
NUM_WORDS = len(words_set)
NUM_POS = len(pos_set)
counter = np.zeros((NUM_WORDS, NUM_POS))
with open('data/small-wikipedia.deps', 'r') as fin:
    words = []
    pos = []
    for _, line in enumerate(fin):
        tab = compat_splitting(line)
        if len(tab) > 2:
            w_id = w2i[tab[1]]
            p_id = p2i[tab[3]]
            counter[w_id][p_id] += 1
print "done counting"
# create list of words with more than one popular pos tag.
problematic_words_idx = []
problematic_pos = [p2i[pos] for pos in ['NN', 'VB', 'JJ']]
# with open('/home/ron/word2vec-heb/common_multi.txt', 'w') as fout:
for i in range(NUM_WORDS):
    ind = np.argpartition(counter[i], -2)[-2:]
    if np.sum(counter[i]) > 10 and counter[i][ind[0]] > np.sum(counter[i]) / 10:
        if ind[0] in problematic_pos and ind[1] in problematic_pos:
            problematic_words_idx.append(i)
        else:
            if counter[i][ind[0]] > np.sum(counter[i]) / 5:
                print "not added: " + i2w[i] + i2p[ind[0]]

print "problematic found."
print len(problematic_words_idx)
problematic_words_idx = set(problematic_words_idx)
print "converted to set"
print len(problematic_words_idx)

word = ''
pos = ''
last_pos = ''
last_word = ''
couples_count = Counter()
with open('data/small-wikipedia.deps', 'r') as fin:
    for i, line in enumerate(fin):
        if i % 1000000 == 0:
            print i
        tab = compat_splitting(line)
        if len(tab) > 2:
            if tab[1][0] == '*':
                continue
            last_word2 = last_word
            last_pos2 = last_pos
            last_word = word
            last_pos = pos
            word = tab[1]
            pos = tab[3]
            if np.sum(counter[w2i[word]]) < 10:
                word = ""
                pos = ""
            if pos == 'NN' and last_pos == 'NNT':
                couples_count[(last_word, word)] += 1
                word = ''
                pos = ''
                last_pos = ''
                last_word = ''
            elif pos == 'NN' and last_pos2 == 'NNT':
                couples_count[(last_word2, word)] += 1
                word = ''
                pos = ''
                last_pos = ''
                last_word = ''

print "done couples counting"

word = ''
pos = ''
last_pos = ''
last_word = ''
before_selection = 0
after_selection = 0
with open('data/small-wikipedia.deps', 'r') as fin:
    with open('data/wiki-processed-data.txt', 'w') as fout:
        for i, line in enumerate(fin):
            if (i + 1) % 1000000 == 0:
                print i
                # break
            tab = compat_splitting(line)
            if len(tab) > 2:
                if tab[1][0] == '*':
                    continue
                last_word2 = last_word
                last_pos2 = last_pos
                last_word = word
                last_pos = pos
                word = tab[1]
                pos = tab[3]
                if pos == 'NN' and last_pos == 'NNT':
                    before_selection += 1
                    if couples_count[(last_word, word)] >\
                            5:
                        after_selection += 1
                        write_word(last_word2, last_pos2)
                        fout.write(last_word + "~" + word + ' ')
                        word = ''
                        pos = ''
                        last_pos = ''
                        last_word = ''
                    else:
                        write_word(last_word2, last_pos2)
                elif pos == 'NN' and last_pos2 == 'NNT':
                    before_selection += 1
                    if couples_count[(last_word2, word)] > 5:
                        after_selection += 1
                        fout.write(last_word2 + "~" + last_word + word + ' ')
                        word = ''
                        pos = ''
                        last_pos = ''
                        last_word = ''
                    else:
                        write_word(last_word2, last_pos2)
                else:
                    write_word(last_word2, last_pos2)
            else:
                fout.write(last_word + ' ' + word + '\n')
                word = ''
                pos = ''
                last_pos = ''
                last_word = ''
print "done"
