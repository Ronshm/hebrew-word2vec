# !/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import *
from utils import *
from globals import *
from pathes import Path

#
# reload(sys)
# sys.setdefaultencoding('utf-8')


global active_algos
global num_results


@get('')
@get('/')  # @route('/login')
@get('/cyber')
@get('/w2v')
@get('/heb-w2v')
def get_menu():
    return menu_text


@post('/choose_algo')
@get('/choose_algo')
def choose_algo():
    html = ' <b size="6"> Select wanted algorithms <br>'
    html += '<form action="algo_selected" method="post">'
    for algo in sorted(words_dict.keys()):
        html += '<input type="checkbox" name="{0}" value=1> {0}<br>'.format(algo)
    html += '<input type="submit" value="Submit"></form>'
    return html


@post('/algo_selected')
@get('/algo_selected')
def update_wanted_algos():
    global active_algos
    active_algos = []
    for algo in words_dict.keys():
        if request.forms.get(algo):
            active_algos.append(algo)
    active_algos = sorted(active_algos)
    return menu_text


@post('/update_num_results')
@get('/update_num_results')
def update_num_results():
    global num_results
    wanted_num_results = request.forms.get('num_results_to_show')
    num_results = int(wanted_num_results)
    return menu_text


@post('/similar')
@get('/similar')
def search():
    f = open(search_result_file, 'a')
    wanted = request.forms.get('wanted')
    if not wanted:
        return "<p size='4'>Please enter a word</p>"
    text = menu_text
    text += "<p align='center'><b  size='5'>Current searching for words similar to-" + html_space + wanted + "</b><br>"
    for algo in active_algos:
        cur_algo_words = words_dict[algo]
        cur_algo_vec = vectors_dict[algo]
        f.write("Algo: " + algo + "\n")
        text += "<b align = 'center'><br> Algorithm: " + algo + "</b><br>"

        wanted_ind = search_for_word_as_part_of_pos(wanted, algo)
        try:
            wanted_ind.append(cur_algo_words.index(as_appears_in_algo(wanted)))
        except:
            if len(wanted_ind) == 0:
                text += wanted + " is unknown, sorry."
                continue
        for word_ind in wanted_ind:
            f.write("\n\nCurrent searching for words similar to:" + cur_algo_words[word_ind] + "\n")
            text += "<br>Showing results for " + as_appear_in_site(cur_algo_words[word_ind]) + '<br><br>'
            text += get_similar_to_site_and_file(cur_algo_vec[word_ind], algo, f)
    return text + "</p>"


@post('/analogy')
@get('/analogy')
def analogy():
    f = open(analogy_result_file, 'a')
    input_words = [request.forms.get('word1'), request.forms.get('word2'), request.forms.get('word3')]
    for in_word in input_words:
        if not in_word:
            return "<p size='4'>Please enter all the words.</p>"
    text = menu_text
    for algo in active_algos:
        cur_algo_words = words_dict[algo]
        cur_algo_vectors = vectors_dict[algo]
        flag = False
        text += "<br> <b align='center' size='4'>Algorithm: " + algo + "</b><br><br>"
        f.write("Algo: " + algo + "\n")
        words_idx = []
        for in_word in input_words:
            cur_word_idx = search_for_word_as_part_of_pos(in_word, algo)
            try:
                cur_word_idx.append(cur_algo_words.index(as_appears_in_algo(in_word)))
            except:
                if len(cur_word_idx) == 0:
                    text += in_word + " is unknown, sorry."
                    flag = True
            words_idx.append(cur_word_idx)

        if not flag:
            for input_pos_idx_option in list(itertools.product(*words_idx)):
                text += "<p align='center'><b  size='6'>Current looking for:<br>" + cur_algo_words[
                    input_pos_idx_option[2]] + " : word" + "<br>=<br>" + cur_algo_words[
                            input_pos_idx_option[1]] + " : " + cur_algo_words[input_pos_idx_option[0]] + "</b><br>"
                f.write("\n\nCurrent looking for:" + cur_algo_words[input_pos_idx_option[2]] + " : word = " +
                        cur_algo_words[input_pos_idx_option[1]] + " : " + cur_algo_words[
                            input_pos_idx_option[0]] + "\n")
                wanted = cur_algo_vectors[input_pos_idx_option[2]] - cur_algo_vectors[input_pos_idx_option[0]] + \
                         cur_algo_vectors[input_pos_idx_option[1]]
                text += get_similar_to_site_and_file(wanted, algo, f)
    return text + "</p>"


def add_algorithm(path, name, multi_pos_flag=False, words_counter_flag=False):
    path = join('result', path.value)
    if not os.path.exists(join(path, "words_list.txt")):
        organize_data(path)
    with open(join(path, "words_list.txt"), 'r') as f:
        cur_words = f.readlines()
    cur_words = [word[:-1] for word in cur_words]
    cur_vecs = np.load(join(path, "words_vectors.npy"))
    words_dict[name] = cur_words
    vectors_dict[name] = cur_vecs
    multi_pos_dict[name] = multi_pos_flag
    if words_counter_flag:
        words_counters_dict[name] = np.load(open(join(path, 'words_counter.npy')))


def prepare_to_run():
    global active_algos
    global num_results
    num_results = DEFAULT_NUM_RESULTS
    add_algorithm(Path.path_FT, "fastText")
    add_algorithm(Path.path_w2v, "w2v")
    # add_algorithm(Path.path_FT_seg, "fastText seg")
    # add_algorithm(Path.path_w2v_nn_win5, "w2v nn win 5")
    # add_algorithm(Path.path_w2v_seg, "w2v seg")
    # add_algorithm(Path.path_w2v_nn_win3, "w2v nn win 3")
    # add_algorithm(Path.path_w2v_nn_win10, "w2v nn win 10")
    # add_algorithm(Path.path_w2v_nn_win5_neg10, "w2v nn win 5 neg 10")
    add_algorithm(Path.path_w2v_multi_pos, "w2v multi pos", True)
    add_algorithm(Path.path_FT_multi_pos, "fastText multi pos", True)
    # add_algorithm(Path.path_FT_nn, "fastText nn")
    add_algorithm(Path.path_FT_nn_filtered, "fastText nn filtered")
    add_algorithm(Path.path_w2v_nn_filtered, "w2v nn filtered")
    add_algorithm(Path.path_odeds_algo_200, "Oded's algorithm 200 dim feature")
    add_algorithm(Path.path_odeds_algo, "Oded's algorithm")
    add_algorithm(Path.path_w2v_nn_pos_10, "w2v main (nn&pos) 10 feat", True, True)
    add_algorithm(Path.path_w2v_nn_pos_100, "w2v main (nn&pos) 100 feat", True, True)
    add_algorithm(Path.path_w2v_nn_pos_200, "w2v main (nn&pos) 200 feat", True, True)
    add_algorithm(Path.path_w2v_twitter, "w2v twitter", False, True)
    add_algorithm(Path.path_w2v_neg_20, "w2v nn&pos more negative(20)", True, True)
    add_algorithm(Path.path_w2v_neg_20_min_20, "w2v nn&pos more negative(20) and higher min", True, True)
    active_algos = ["w2v main (nn&pos) 100 feat", "Oded's algorithm", "w2v twitter", "w2v nn&pos more negative(20)"]
    active_algos = sorted(active_algos)
    # run(host='77.126.119.142', port=80, debug=True)
    # run(host='192.168.1.15', port=80, debug=True)
    # run(host='localhost', port=7765, debug=False)
    # run(host='132.71.121.195', port=8079, debug=False)


if __name__ == "__main__":
    words_dict = {}
    vectors_dict = {}
    multi_pos_dict = {}
    words_counters_dict = {}
    prepare_to_run()
    run(host='', port=7765, debug=False)
    #

    # context = get_context_vec(join('result', path_w2v_nn_pos_10), ["לחם", "אב", "מלאכה", "ספר", "כנסת"],
    #                           words_dict['w2v main (nn&pos) 10 feat'])
    #
    # print get_similar_console(context, words_dict['w2v main (nn&pos) 10 feat'],
    #                           vectors_dict['w2v main (nn&pos) 10 feat'])
    #
    # context = get_context_vec(join('result', path_w2v_nn_pos_10), ["חוף", "סירה", "אוקיאנוס", "ים", "גלים"],
    #                           words_dict['w2v main (nn&pos) 10 feat'])
    #
    # print get_similar_console(context, words_dict['w2v main (nn&pos) 10 feat'],
    #                           vectors_dict['w2v main (nn&pos) 10 feat'])

    # active_algos = []
