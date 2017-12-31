#!/usr/bin/env python
# -*- coding: utf-8 -*-
from copy import deepcopy
from sklearn.cluster import KMeans
import random
import cPickle
from sklearn.metrics import *
import numpy as np
from os.path import join, exists


def get_appearances_map(wanted_word):
    appearances_windows_map = []
    with open('../data/wiki-data-new.txt', 'r') as fin:
        for i, line in enumerate(fin):
            if (i + 1) % 1000000 == 0:
                print i
                # break
            words = line.split()
            for i, word in enumerate(words):
                if word == wanted_word:
                    window = words[max(i - 3, 0): i + 4]
                    if len(window) < 3:
                        print "short"
                        continue
                    appearances_windows_map.append(window)
    return appearances_windows_map


def write_appearances_map_to_file(appearances_map, path):
    with open(path, 'w') as fout:
        for window in appearances_map:
            for word in window:
                fout.write(word + ' ')
            fout.write('\n')


def read_appearances_map_from_file(path):
    windows = []
    with open(path, 'r') as fin:
        for i, line in enumerate(fin):
            words = line.split(' ')
            words[-1].replace('\n', '')
            windows.append(deepcopy(words))
    return windows


def convert_words_window_to_vec(window, w2v_dict):
    window_vec = np.zeros(100)
    with open('errors.txt', 'w') as fout:
        for word in window:
            if word not in w2v_dict.keys():
                fout.write("word: " + word)
                fout.write('\n')
                window.remove(word)
                print 'unrecognized word'
                continue
            cur_word_vec = w2v_dict[word]
            window_vec += cur_word_vec
    window_vec /= len(window)
    return window_vec


def create_windows_vecs(appearances_map, w2v_dict, wanted_word):
    vecs = []
    for window in appearances_map:
        vecs.append(convert_words_window_to_vec([word for word in window if not word == wanted_word], w2v_dict))
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


def part_one(wanted_word):
    if exists(join('data', 'windows-vecs.npy')):
        appearances_map = read_appearances_map_from_file(join('data', 'appearance_map.txt'))
        windows_vecs = np.load(join('data', 'windows-vecs.npy'))
        return appearances_map, windows_vecs
    appearances_map = get_appearances_map(wanted_word)
    write_appearances_map_to_file(appearances_map, join('data', 'appearance_map.txt'))
    d = get_w2v_dict('data')
    windows_vecs = create_windows_vecs(appearances_map, d, wanted_word)
    np.save(join('data', 'windows-vecs.npy'), windows_vecs)
    return appearances_map, windows_vecs


def part_two(appearance_map, windows_vecs):
    kmeans = KMeans(n_clusters=2, random_state=0).fit(windows_vecs)
    labels = kmeans.labels_
    f1 = open(join('data', 'cluster1_sentences.txt'), 'w')
    f2 = open(join('data', 'cluster2_sentences.txt'), 'w')
    cluster1_windows = []
    cluster2_windows = []
    for i, win in enumerate(appearance_map):
        if labels[i]:
            f = f1
            cluster = cluster1_windows
        else:
            f = f2
            cluster = cluster2_windows
        for word in win:
            f.write(word + ' ')
        f.write('\n')
        cluster.append(win)
    return kmeans


def load_test_set():
    if exists(join('data', "test-set.p")):
        test_set = cPickle.load(open(join('data', "test-set.p"), "wb"))
    else:
        x_class1 = read_appearances_map_from_file(join('data', 'test-class1.txt'))
        x_class2 = read_appearances_map_from_file(join('data', 'test-class2.txt'))
        d = get_w2v_dict('data')
        x = []
        x.extend(x_class1)
        x.extend(x_class2)
        data_vecs = create_windows_vecs(x, d, 'בצל')
        labels = [0 for _ in range(len(x_class1))]
        labels.extend([1 for _ in range(len(x_class2))])
        test_set = {'x': data_vecs, 'y': labels}
        cPickle.dump(test_set, open(join('data', "test-set.p"), "wb"))
    return test_set


def evaluate(kmeans):
    test_set = load_test_set()
    predicted_labels = kmeans.predict(test_set['x'])
    true_labels = test_set['y']
    if accuracy_score(true_labels, predicted_labels) < 0.5:
        predicted_labels = [1 - l for l in predicted_labels]
    print "accuracy:", accuracy_score(true_labels, predicted_labels)
    print "recall class 1:", recall_score(true_labels, predicted_labels, pos_label=0)
    print "precision class 1:", precision_score(true_labels, predicted_labels, pos_label=0)
    print "recall class 2:", recall_score(true_labels, predicted_labels, pos_label=1)
    print "precision class 2:", precision_score(true_labels, predicted_labels, pos_label=1)


def main():
    appearances_map, windows_vecs = part_one('בצל')
    kmeans = part_two(appearances_map, windows_vecs)
    evaluate(kmeans)


if __name__ == '__main__':
    main()
