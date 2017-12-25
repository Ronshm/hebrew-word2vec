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
    with open(join("result", Path.path_w2v_nn_pos_200.value, "words_list.txt"), 'r') as f:
        cur_words = f.readlines()
    words = [word[:-1] for word in cur_words]
    output_vecs = np.load(join("result", Path.path_w2v_nn_pos_200.value, "words_vectors.npy"))
    context = get_context_vec(join('result', Path.path_w2v_nn_pos_200.value), ["חולים", "כנסת", "עקרת", "ספר~תיכון"],
                              words)
    context_vectors = np.load(join(join('result', Path.path_w2v_nn_pos_200.value), "context_vectors.npy"))

    print get_similar_console(context, words,
                              # context_vectors)
                              output_vecs)
