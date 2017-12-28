#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from os.path import join
from utils import *
from pathes import Path


def get_context_vec(path, context_words, words_list):
    # context_vectors = np.load(join(path, "words_vectors.npy"))
    context_vectors = np.load(join(path, "context_vectors.npy"))
    context_vec = np.zeros(len(context_vectors[0]))
    for word in context_words:
        ind = words_list.index(word)
        context_vec += context_vectors[ind]
        # print context_vectors[ind]
    return context_vec


if __name__ == '__main__':
    path = Path.path_w2v_neg_20.value
    with open(join("result", path, "words_list.txt"), 'r') as f:
        cur_words = f.readlines()
    words = [word[:-1] for word in cur_words]
    output_vecs = np.load(join("result", path, "words_vectors.npy"))
    context = get_context_vec(join('result', path), ["חולים", "כנסת", "עקרת", "ספר~תיכון"],
                              words)
    context_vectors = np.load(join('result', path, "context_vectors.npy"))

    print get_similar_console(context, words,
                              # context_vectors)
                              output_vecs)
