#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sklearn.cluster import KMeans
from sklearn.metrics import *
from local_utils import *


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


def evaluate(kmeans):
    test_set = load_test_set()
    predicted_labels = kmeans.predict(test_set['x'])
    true_labels = test_set['y']
    print len(true_labels)
    print len(test_set['x'])
    if accuracy_score(true_labels, predicted_labels) < 0.5:
        predicted_labels = [1 - l for l in predicted_labels]
    print sum(predicted_labels)
    print len(predicted_labels)
    print sum(true_labels)
    print len(true_labels)
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
