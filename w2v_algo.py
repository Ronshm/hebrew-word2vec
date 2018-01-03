from utils import *
from numpy import linalg as LA
import itertools


class AlgoContainer:
    def __init__(self):
        self._algos_dict = {}
        self._active_algos = []
        self._num_results = 10

    def set_num_results(self, num):
        self._num_results = num

    def add_algo(self, algo):
        self._algos_dict[algo.get_name()] = algo

    def set_active_algos(self, names_list):
        self._active_algos = [name for name in names_list if name in self._algos_dict.keys()]

    def get_algos_names(self):
        return self._algos_dict.keys()

    def get_algos(self):
        return self._algos_dict.values()

    def get_active_algos(self):
        return [self._active_algos[algo_name] for algo_name in self._active_algos]

    def add_to_active_algos(self, name):
        if name in self._algos_dict.keys():
            if name not in self._active_algos:
                self._active_algos.append(name)

    def remove_from_active_algos(self, name):
        if name in self._active_algos:
            self._active_algos.remove(name)

    def search_similar(self, word):
        result_dict = {}
        for algo in self._active_algos:
            result_dict[algo] = self._algos_dict[algo].search_similar(word, self._num_results)
        return result_dict

    def search_analogy(self, words):
        result_dict = {}
        for algo in self._active_algos:
            result_dict[algo] = self._algos_dict[algo].search_analogy(words, self._num_results)
        return result_dict


class Algo:
    def __init__(self, data_path, name, multi_pos_flag=False, words_counter_flag=False):
        self._data_path = data_path
        self._name = name
        self._multi_pos_flag = multi_pos_flag
        self._words_counter_flag = words_counter_flag
        self._load_algo_data()

    def _load_algo_data(self):
        path = join('result', self._data_path)
        if not os.path.exists(join(path, "words_list.txt")):
            organize_data(path)
        with open(join(path, "words_list.txt"), 'r') as f:
            cur_words = f.readlines()
        cur_words = [word[:-1] for word in cur_words]
        cur_vecs = np.load(join(path, "words_vectors.npy"))
        self._words_list = cur_words
        self._vecs = cur_vecs / LA.norm(cur_vecs, axis=1)

        if self._words_counter_flag:
            if not os.path.exists(join(path, 'words_counter.npy')):
                raise Exception("Words counter for algo {} doesn\'t exist".format(self._name))
            else:
                self._words_counter = np.load(open(join(path, 'words_counter.npy')))

    def search_similar(self, word, num_results):
        results_dict = {}
        wanted_ind = search_for_word_as_part_of_pos(word, self._words_list, self._multi_pos_flag)
        try:
            wanted_ind.append(self._vecs.index(as_appears_in_algo(word)))
        except:
            if len(wanted_ind) == 0:
                return {}
        for word_ind in wanted_ind:
            results = self._top_similar_smart(self._vecs[word_ind], num_results=num_results)
            results_dict[self._words_list[word_ind]] = results
        return results_dict

    def search_analogy(self, input_words, num_results):
        results_dict = {}

        words_idx = []
        for in_word in input_words:
            cur_word_idx = search_for_word_as_part_of_pos(in_word, self._words_list, self._multi_pos_flag)
            try:
                cur_word_idx.append(self._words_list.index(as_appears_in_algo(in_word)))
            except:
                if len(cur_word_idx) == 0:
                    return {}
            words_idx.append(cur_word_idx)

        for input_pos_idx_option in list(itertools.product(*words_idx)):
            wanted_vec = self._vecs[input_pos_idx_option[2]] - self._vecs[input_pos_idx_option[0]] + \
                         self._vecs[input_pos_idx_option[1]]
            results = self._top_similar_smart(wanted_vec, num_results=num_results)
            results_dict[(self._words_list[word_ind] for word_ind in input_pos_idx_option)] = results

        return results_dict

    def _top_similar_smart(self, wanted_vec, num_results=10):
        if not self._words_counter:
            idx, sims = self._top_similar(wanted_vec, self._vecs, num_results)
            results = [{'word': self._words_list[idx[i]], 'similarity': sims[i]} for i in range(num_results)]
            return results
        idx, sims = self._top_similar(wanted_vec, self._vecs, num_results + 5)
        cur_words_counts = self._words_counter[idx]
        highest = np.max(cur_words_counts)
        smart_score = [(sims[i] + 0.05 * cur_words_counts[i] / highest) for i in range(len(idx))]
        ind = np.argpartition(smart_score, -num_results)[-num_results:]
        ind = ind[np.argsort([smart_score[i] for i in ind])]
        ind = ind[::-1]
        results = [{'word': self._words_list[i], 'similarity': sims[i], 'appearances': cur_words_counts[i]}
                   for i in ind]
        return results

    def _top_similar(self, vec, results_to_show=10):
        try:
            mul = np.dot(self._vecs, vec)
        except:
            try:
                mul = np.dot(vec, self._vecs)
            except:
                for i in range(len(self._vecs)):
                    if self._vecs[i].shape[0] != 100 or self._vecs[i].shape[0] != 200:
                        print("error at top similar at vec number {} with shape {}".format(i, self._vecs[i].shape))
        vec_norm = LA.norm(vec)
        sims = np.divide(mul, self._vecs)
        sims /= vec_norm
        ind = np.argpartition(sims, -results_to_show)[-results_to_show:]
        ind = ind[np.argsort(sims[ind])]
        ind = ind[::-1]
        return ind, sims[ind]
