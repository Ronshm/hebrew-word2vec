#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils import *
from copy import deepcopy


def get_appearances_map(wanted_word):
    appearances_windows_map = []
    with open('data/wiki-data-new.txt', 'r') as fin:
        for i, line in enumerate(fin):
            if (i + 1) % 1000000 == 0:
                print i
                # break
            words = line.split(' ')
            for i, word in enumerate(words):
                if word == wanted_word:
                    appearances_windows_map.append(words[max(i - 2, 0), i + 3])
    return appearances_windows_map


def write_appearances_map_to_file(appearances_map):
    with open(join('result', 'research', 'appearance_map'), 'w') as fout:
        for window in appearances_map:
            for word in window:
                fout.write(word + ' ')
            fout.write('\n')


def read_appearances_map_from_file():
    windows = []
    with open(join('result', 'research', 'appearance_map'), 'r') as fin:
        for i, line in enumerate(fin):
            words = line.split(' ')
            words[-1].replace('\n', '')
            windows.append(deepcopy(words))
    return windows


def convert_words_window_to_vec(window, w2v_dict):
    window_vec = np.zeros(np.shape(w2v_dict.values[0]))
    for word in window:
        window_vec += w2v_dict[word]
    window_vec /= len(window)
    return window_vec


def create_windows_vecs(appearances_map, w2v_dict):
    vecs = []
    for window in appearances_map:
        vecs.append(convert_words_window_to_vec(window, w2v_dict))
    return np.array(vecs)


def get_w2v_dict(path):
    d = {}
    with open(join(path, "words_list.txt"), 'r') as f:
        cur_words = f.readlines()
    cur_words = [word[:-1] for word in cur_words]
    cur_vecs = np.load(join(path, "words_vectors.npy"))
    for i in range(len(cur_words)):
        d[cur_words[i]] = cur_vecs[i]
    return d


def part_one():
    if os.path.exists(join('result', 'research', 'appearance_map')):
        appearances_map = read_appearances_map_from_file()
        windows_vecs = np.load('windows_vecs.npy')
        return appearances_map, windows_vecs
    appearances_map = get_appearances_map('בצל')
    write_appearances_map_to_file(appearances_map)
    d = get_w2v_dict(join('result', Path.path_research.value))
    windows_vecs = create_windows_vecs(appearances_map, d)
    np.save('windows_vecs.npy', windows_vecs)
    return appearances_map, windows_vecs


def main():
    part_one()


if __name__ == '__main__':
    main()
