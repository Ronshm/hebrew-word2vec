from utils import *


class Algo():
    def __init__(self, dir_path, name, multi_pos_flag=False, words_counter_flag=False):
        self._dir_path = dir_path
        self._name = name
        path = join('result', self._data_path)
        if not os.path.exists(join(path, "words_list.txt")):
            organize_data(path)
        with open(join(path, "words_list.txt"), 'r') as f:
            cur_words = f.readlines()
        cur_words = [word[:-1] for word in cur_words]
        cur_vecs = np.load(join(path, "words_vectors.npy"))
        self._words_list = cur_words
        self._vecs = cur_vecs
        self._multi_pos_flag = multi_pos_flag
        self._words_counter_flag = words_counter_flag
        if words_counter_flag:
            if not os.path.exists(join(path, 'words_counter.npy')):
                raise Exception("Words counter for algo {} doesn\'t exist".format(self._name))
            else:
                self._words_counter = np.load(open(join(path, 'words_counter.npy')))

    def search_similar(self, wanted_word, f):
        text = ""
        wanted_ind = search_for_word_as_part_of_pos(wanted_word, self._words_list, self._multi_pos_flag)
        try:
            wanted_ind.append(self._words_list.index(as_appears_in_algo(wanted_word)))
        except:
            if len(wanted_ind) == 0:
                text += wanted_word + " is unknown, sorry."
                return ""
        for word_ind in wanted_ind:
            f.write("\n\nCurrent searching for words similar to:" + self._words_list[word_ind] + "\n")
            text += "<br>Showing results for " + as_appear_in_site(self._words_list[word_ind]) + '<br><br>'
            text += self._get_similar_to_site_and_file(self._vecs[word_ind], f)

    def _top_similar_smart(self, wanted, results_to_show=10):
        if not self._words_counter_:
            return self._top_similar(wanted, self._vecs, results_to_show)
        idx, sims = self._top_similar(wanted, self._vecs, results_to_show + 5)
        cur_words_counts = self._words_counter[idx]
        highest = np.max(cur_words_counts)
        smart_score = [(sims[i] + 0.05 * cur_words_counts[i] / highest) for i in range(len(idx))]
        ind = np.argpartition(smart_score, -results_to_show)[-results_to_show:]
        ind = ind[np.argsort([smart_score[i] for i in ind])]
        ind = ind[::-1]
        return [idx[i] for i in ind], [sims[i] for i in ind]

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
        vecs_norms = LA.norm(self._vecs, axis=1)
        sims = np.divide(mul, vecs_norms)
        sims /= vec_norm
        ind = np.argpartition(sims, -results_to_show)[-results_to_show:]
        ind = ind[np.argsort(sims[ind])]
        ind = ind[::-1]
        return ind, sims[ind]

    def _get_similar_to_site_and_file(self, wanted, f):
        global num_results
        text = ""
        inds, sims = self._top_similar_smart(wanted, results_to_show=num_results)
        for i in range(len(inds)):
            text += "similarity:" + str(sims[i]) + html_double_space + as_appear_in_site(
                self._words_list[inds[i]]) + "<br>"
            if i < MAX_RESULTS_PRINT_TO_FILE:
                f.write(self._words_list[inds[i]] + "\n")
        return text

    def get_similar(self, wanted):
        text = ""
        inds, sims = self._top_similar(wanted, self._vecs)
        for i in range(len(inds)):
            text += "similarity:" + str(sims[i]) + html_double_space + self._words_list[inds[i]] + \
                    "<br>"
        return text

    def get_similar_console(self, wanted):
        text = ""
        inds, sims = self._top_similar(wanted, self._vecs)
        for i in range(len(inds)):
            text += "similarity:{} {}\n".format(sims[i], self._words_list[inds[i]])
        return text
