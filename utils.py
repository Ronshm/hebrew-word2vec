import numpy as np
from numpy import linalg as LA
import sys
from os.path import join

reload(sys)
sys.setdefaultencoding('utf-8')

path_w2v = 'w2v'  # win 5
path_w2v_seg = 'w2v-sig'  # win 10
path_FT = 'fastText'  # win 5
path_FT_final = 'fastText-final'  # doesnt work
path_FT_seg = 'fastText-sig'  # win 10
path_w2v_nn_win3 = 'w2v-nn-win3'  # win 3
path_w2v_nn_win5 = 'w2v-nn-win5'  # win 5
path_w2v_nn_win10 = 'w2v-nn-win10'  # win 10
path_w2v_nn_win5_neg10 = 'w2v-nn-win5-neg10'  # win 10
path_w2v_multi_pos = 'w2v-multi-pos'
path_FT_nn = 'fastText-nn'
path_FT_multi_pos = 'fastText-multi-pos'
path_FT_nn_filtered = 'fastText-nn-filtered'
path_w2v_nn_filtered = 'w2v-nn-filtered'
path_odeds_algo_200 = 'odeds-algo-200dim'
path_odeds_algo = 'odeds-algo'
path_w2v_nn_pos_10 = "w2v-nn-pos-10"
path_w2v_nn_pos_100 = "w2v-nn-pos-100"
path_w2v_nn_pos_200 = "w2v-nn-pos-200"
path_w2v_twitter = 'twitter-w2v'
path_w2v_neg_20 = 'w2v-nn-pos-neg-20'
path_w2v_neg_20_min_20 = 'w2v-nn-pos-neg-20-min-20'


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


def top_similar(vec, vec_set):
    try:
        mul = np.dot(vec_set, vec)
    except:
        try:
            mul = np.dot(vec, vec_set)
        except:
            for i in range(len(vec_set)):
                if vec_set[i].shape[0] != 100 or vec_set[i].shape[0] != 200:
                    print i
                    print vec_set[i].shape
    vec_norm = LA.norm(vec)
    vecs_norms = LA.norm(vec_set, axis=1)
    sims = np.divide(mul, vecs_norms)
    sims /= vec_norm
    ind = np.argpartition(sims, -10)[-10:]
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
    pass
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
