#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sklearn.cluster import KMeans, SpectralClustering, DBSCAN
from sklearn.metrics import *
from sklearn.decomposition import PCA
from local_utils import *
import os
from clustering_methods import ClusteringMethods
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def part_one(wanted_word):
    new_word_data_path = join('data', wanted_word)
    if not os.path.exists(new_word_data_path):
        os.makedirs(new_word_data_path)
    if exists(join(new_word_data_path, 'windows-vecs.npy')):
        appearances_map = read_appearances_map_from_file(join(new_word_data_path, 'appearance_map.txt'))
        windows_vecs = np.load(join(new_word_data_path, 'windows-vecs.npy'))
    else:
        appearances_map = get_appearances_map(wanted_word)
        write_appearances_map_to_file(appearances_map, join(new_word_data_path, 'appearance_map.txt'))
        d = get_w2v_dict('data')
        windows_vecs = create_windows_vecs(appearances_map, d, wanted_word)
        np.save(join(new_word_data_path, 'windows-vecs.npy'), windows_vecs)
    reduced_dim_vecs_path = join(new_word_data_path, 'reduced-windows-vecs.npy')
    if exists(reduced_dim_vecs_path):
        reduce_vecs = np.load(reduced_dim_vecs_path)
    else:
        print "pca start"
        reduce_vecs = PCA(n_components=3).fit_transform(windows_vecs)
        np.save(reduced_dim_vecs_path, reduce_vecs)
        print "done pca"
    return appearances_map, windows_vecs, reduce_vecs


def part_two(cluster_type, wanted_word, appearance_map, windows_vecs, reduced_vecs):
    print "start clustering"
    if cluster_type == ClusteringMethods.Kmeans:
        cluster_algo = KMeans(n_clusters=2, random_state=0).fit(windows_vecs)
    elif cluster_type == ClusteringMethods.Spectral:
        cluster_algo = SpectralClustering(n_clusters=2).fit(windows_vecs)
    elif cluster_type == ClusteringMethods.DBScan:
        cluster_algo = DBSCAN().fit(windows_vecs)
        pass
    elif cluster_type == ClusteringMethods.HDBScan:
        pass
    elif cluster_type == ClusteringMethods.PcaDBScan:
        cluster_algo = DBSCAN().fit(reduced_vecs)
        pass
    elif cluster_type == ClusteringMethods.PcaHDBScan:
        pass
    elif cluster_type == ClusteringMethods.PcaKmeans:
        cluster_algo = KMeans(n_clusters=2, random_state=0).fit(reduced_vecs)
        pass
    labels = cluster_algo.labels_
    print "done clustering"
    new_word_data_path = join('data', cluster_type.value, wanted_word)
    create_dir(new_word_data_path)
    f1 = open(join(new_word_data_path, 'cluster1_sentences.txt'), 'w')
    f2 = open(join(new_word_data_path, 'cluster2_sentences.txt'), 'w')
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
    return cluster_algo


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


def plot(vecs, labels=None):
    xs = []
    ys = []
    zs = []
    z_flag = False
    if len(vecs[0]) > 2:
        z_flag = True
    else:
        zs = 0
    for i in range(len(vecs)):
        cur_vec = vecs[i]
        xs.append(cur_vec[0])
        ys.append(cur_vec[1])
        if z_flag:
            zs.append(cur_vec[2])

    # print xs, '\n', ys, '\n', zs
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    if labels:
        colors_list = []
        for label in labels:
            c = 'b' if label else 'g'
            colors_list.append(c)
        ax.scatter(xs=xs, ys=ys, zs=zs, c=colors_list)
    else:
        ax.scatter(xs=xs, ys=ys, zs=zs)
    plt.show(block=True)


def main(word):
    for cluster_method in ClusteringMethods:
        # test_set = load_test_set()
        appearances_map, windows_vecs, reduced_vecs = part_one(word)
        # pca = PCA(n_components=3)
        # pca.fit(windows_vecs)
        # test_reduced = pca.transform(test_set['x'])
        # plot(test_reduced, labels=test_set['y'])
        cluster = part_two(cluster_method, word, appearances_map, windows_vecs, reduced_vecs)
        # evaluate(kmeans)


if __name__ == '__main__':
    main("בצל")
    # main("לכת")
    main("מאור")
    main("בריאה")
    # main("שכל")
    main("שטף")
    # main("מכל")
    main("מעלה")
    main("בצורת")
    # main("שכח")
    # main("שאף")
    # main("מידע")
    main("למידה")
    # main("מעתיקה")
    # main("מתואר")
    main("מיון")
    main("ליון")
    # main("משני")
    # main("משנה")
    # main("מבנה")
