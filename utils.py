import numpy as np
from numpy import linalg as LA
import sys
from os.path import join
from collections import Counter
import os
from pathes import Path

reload(sys)
sys.setdefaultencoding('utf-8')


def compat_splitting(line):
    try:
        ret_value = line.decode('utf8').split()
    except:
        print("error on this line:", line)
        ret_value = []
    return ret_value


def read_vectors(model_path):
    vectors = []
    words = []
    with open(model_path, 'rb') as fin:
        for i, line in enumerate(fin):
            if i == 0:
                continue
            # if len(words) > 10:
            #     break
            tab = compat_splitting(line)
            if len(tab) == 0:
                print("passed error1")
                continue
            try:
                vec = np.array(tab[1:], dtype=float)
            except:
                print("passed error2")
                continue
            # print vec
            word = tab[0]
            if (len(vec) != 100) and (len(vec) != 200) and (len(vec) != 10):
                pass
            else:
                words.append(word + str('\n'))
                vectors.append(vec)
            if np.linalg.norm(vec) == 0:
                print("checkit")
                continue
    return words, vectors


def create_words_counter(path):
    counter_vec = []
    with open(os.path.join(path, "words_list.txt"), 'r') as f:
        words = f.readlines()
    words_in_order = [word[:-1] for word in words]

    with open('data/wiki-processed-data.txt', 'r') as fin:
        words = []
        for i, line in enumerate(fin):
            if i % 1000000 == 0:
                print i
            words.extend(line.split(' ').split('\t').replace('\n', ''))
    print "done reading_data."
    words_counter = Counter(words)

    for word in words_in_order:
        counter_vec.append(words_counter[word])
    with open(join(path, 'words_counter.npy'), 'w') as f:
        np.save(f, np.array(counter_vec))


def read_odeds_vectors(model_path):
    vectors = []
    words = []
    flag = 1
    i = 0
    with open(model_path, 'rb') as fin:
        for _, line in enumerate(fin):
            i += 1
            if flag:
                flag = 0
                continue
            # if len(words) > 10:
            #     break
            tab = compat_splitting(line)
            vec = np.array(tab[1:], dtype=float)
            # print vec
            word = tab[0].split(':')[1].split('~')[0]
            if (len(vec) != 100) and (len(vec) != 200) and (len(vec) != 100):
                print "hereeee", i
                pass
            else:
                words.append(word + str('\n'))
                vectors.append(vec)
            if np.linalg.norm(vec) == 0:
                print("checkit")
                continue
    return words, vectors


def organize_data(path):
    words, vectors = read_vectors(join(path, "out.txt"))
    vectors = np.array(vectors)
    np.save(join(path, "words_vectors.npy"), vectors)
    print("vec saved")
    with open(join(path, "words_list.txt"), 'w') as f:
        for w in words:
            f.write(w)
    print("words saved")


def organize_odeds_data(path):
    words, vectors = read_odeds_vectors(path + "/out.txt")
    vectors = np.array(vectors)
    np.save(join(path, "words_vectors.npy"), vectors)
    print("vec saved")
    with open(join(path, "words_list.txt"), 'w') as f:
        for w in words:
            f.write(w)
    print("words saved")


def top_similar(vec, vec_set, results_to_show=10):
    try:
        mul = np.dot(vec_set, vec)
    except:
        try:
            mul = np.dot(vec, vec_set)
        except:
            for i in range(len(vec_set)):
                if vec_set[i].shape[0] != 100 or vec_set[i].shape[0] != 200:
                    print("error at top similar at vec number " + str(i) + "with shape" + str(vec_set[i].shape))
    vec_norm = LA.norm(vec)
    vecs_norms = LA.norm(vec_set, axis=1)
    sims = np.divide(mul, vecs_norms)
    sims /= vec_norm
    ind = np.argpartition(sims, -results_to_show)[-results_to_show:]
    ind = ind[np.argsort(sims[ind])]
    ind = ind[::-1]
    return ind, sims[ind]


def as_appears_in_algo(word):
    word = word.lstrip()
    word = word.replace("-", "~")
    word = word.replace(" ", "~")
    return word


def as_appear_in_site(word):
    word = word.replace("~", " ")
    return word


def get_similar(wanted, words, vecs):
    text = ""
    inds, sims = top_similar(wanted, vecs)
    for i in range(len(inds)):
        text += "similarity::" + str(sims[i]) + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" + words[inds[i]] + \
                "<br>"
    return text


def get_similar_console(wanted, words, vecs):
    text = ""
    inds, sims = top_similar(wanted, vecs)
    for i in range(len(inds)):
        text += "similarity::" + str(sims[i]) + " " + words[inds[i]] + "\n"
    return text


def get_context_vec(path, context_words, words_list):
    # context_vectors = np.load(join(path, "words_vectors.npy"))
    context_vectors = np.load(join(path, "context_vectors.npy"))
    context_vec = np.zeros(len(context_vectors[0]))
    for word in context_words:
        ind = words_list.index(word)
        context_vec += context_vectors[ind]
        # print context_vectors[ind]
    return context_vec


if __name__ == "__main__":
    # organize_data(join("result", path_w2v_nn_pos_200))
    create_words_counter(join('result', Path.path_w2v_nn_pos_100.value))
    # pass
# _, vectors = read_vectors(join('result', path_nn_pos_10, "context.txt"))
# np.save(join('result', path_nn_pos_10, "context_vectors.npy"), vectors)
# pass
# organize_data(join("result", path_w2v_nn_pos_200))

# organize_data(path_FT)
# organize_data(path_w2v_deps)
# with open(path_FT_deps + "/words_list.txt", 'r') as f:
#     words = f.readlines()
# vectors = np.load(path_FT_deps + "/words_vectors.npy")
# # print len(vectors)
# # print len(words)
# inds, sims = top_similar(vectors[83017], vectors)
# for i in range(len(inds)):
#     print words[inds[i]], sims[i]

# print vectors[25]

# f_nn = open("result/neighbours.txt", 'w')
# for i in range(len(vectors)):
#     if i % 1000 == 0:
#         print "now at ", i
#     indexes, sim = top_similar(vectors[i], vectors)
#     for j in range(10):
#         # try:
#         f_nn.write(str(words[indexes[j]][:-1]) + str('\t') + str(sim[j]) + str('\t'))
#         # except:
#         #     print"here2"
#         #     f_nn.write(str(words[indexes[j]]) + str('\t') + str(sim[i]) + str('\t'))
#     f_nn.write('\n')
