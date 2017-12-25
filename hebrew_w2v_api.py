from os.path import join
from pathes import Path
import numpy as np
from utils import as_appears_in_algo, top_similar_smart
from site import search_for_word_as_part_of_pos

global num_results
path = join('results', Path.path_w2v_nn_pos_100.value)
with open(join(path, "words_list.txt"), 'r') as f:
    cur_words = f.readlines()
cur_words = [word[:-1] for word in cur_words]
cur_vecs = np.load(join(path, "words_vectors.npy"))
cur_counter = np.load(join(path, "words_counter.npy"))


def find_similar(wanted, num_output):
    try:
        wanted_ind = [cur_words.index(as_appears_in_algo(wanted))]
    except:
        wanted_ind = search_for_word_as_part_of_pos(wanted, "w2v main (nn&pos) 100 feat")
        if len(wanted_ind) == 0:
            return None
    inds, _ = top_similar_smart(cur_vecs[wanted], cur_vecs, cur_counter, num_output)
    return cur_words[inds]
