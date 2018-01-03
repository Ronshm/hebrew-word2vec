# !/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import *
from utils import *
from globals import *
from pathes import Path
from w2v_algo import Algo, AlgoContainer


#
# reload(sys)
# sys.setdefaultencoding('utf-8')


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
    for algo in sorted(algo_container.get_algos_names()):
        html += '<input type="checkbox" name="{0}" value=1> {0}<br>'.format(algo)
    html += '<input type="submit" value="Submit"></form>'
    return html


@post('/algo_selected')
@get('/algo_selected')
def update_wanted_algos():
    algo_container.set_active_algos([])
    for algo in algo_container.get_algos_names():
        if request.forms.get(algo):
            algo_container.add_to_active_algos(algo)
    return menu_text


@post('/update_num_results')
@get('/update_num_results')
def update_num_results():
    wanted_num_results = request.forms.get('num_results_to_show')
    algo_container.set_num_results(int(wanted_num_results))
    return menu_text


@post('/similar')
@get('/similar')
def search():
    f = open(search_result_file, 'a')
    wanted_word = request.forms.get('wanted')
    if not wanted_word:
        return "<p size='4'>Please enter a word</p>"
    html_text = menu_text
    file_text = ''
    algos_similarity_results = algo_container.search_similar(wanted_word)
    html, text = convert_search_results_to_text(algos_similarity_results, wanted_word)
    html_text += html
    file_text += text
    f.write(file_text)
    return html_text + "</p>"


@post('/analogy')
@get('/analogy')
def analogy():
    f = open(analogy_result_file, 'a')
    input_words = [request.forms.get('word1'), request.forms.get('word2'), request.forms.get('word3')]
    for in_word in input_words:
        if not in_word:
            return "<p size='4'>Please enter all the words.</p>"
    html_text = menu_text
    file_text = ""
    algos_similarity_results = algo_container.search_analogy(input_words)
    html, text = convert_analogy_results_to_text(algos_similarity_results, input_words)
    html_text += html
    file_text += text
    f.write(file_text)
    return html_text + "</p>"

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


def prepare_to_run():
    algo_container = AlgoContainer()
    algo_container.add_algo(Algo(Path.path_FT, "fastText"))
    algo_container.add_algo(Algo(Path.path_w2v, "w2v"))
    algo_container.add_algo(Path.path_w2v_multi_pos, "w2v multi pos", True)
    algo_container.add_algo(Path.path_FT_multi_pos, "fastText multi pos", True)
    algo_container.add_algo(Path.path_FT_nn_filtered, "fastText nn filtered")
    algo_container.add_algo(Path.path_w2v_nn_filtered, "w2v nn filtered")
    algo_container.add_algo(Path.path_odeds_algo_200, "Oded's algorithm 200 dim feature")
    algo_container.add_algo(Path.path_odeds_algo, "Oded's algorithm")
    algo_container.add_algo(Path.path_w2v_nn_pos_10, "w2v main (nn&pos) 10 feat", True, True)
    algo_container.add_algo(Path.path_w2v_nn_pos_100, "w2v main (nn&pos) 100 feat", True, True)
    algo_container.add_algo(Path.path_w2v_nn_pos_200, "w2v main (nn&pos) 200 feat", True, True)
    algo_container.add_algo(Path.path_w2v_twitter, "w2v twitter", False, True)
    algo_container.add_algo(Path.path_w2v_neg_20, "w2v nn&pos more negative(20)", True, True)
    algo_container.add_algo(Path.path_w2v_neg_20_min_20, "w2v nn&pos more negative(20) and higher min", True, True)
    # algo_container.add_algo(Path.path_FT_seg, "fastText seg")
    # algo_container.add_algo(Path.path_w2v_nn_win5, "w2v nn win 5")
    # algo_container.add_algo(Path.path_w2v_seg, "w2v seg")
    # algo_container.add_algo(Path.path_w2v_nn_win3, "w2v nn win 3")
    # algo_container.add_algo(Path.path_w2v_nn_win10, "w2v nn win 10")
    # algo_container.add_algo(Path.path_w2v_nn_win5_neg10, "w2v nn win 5 neg 10")
    # algo_container.add_algo(Path.path_FT_nn, "fastText nn")
    active_algos = ["w2v main (nn&pos) 100 feat", "Oded's algorithm", "w2v twitter", "w2v nn&pos more negative(20)"]
    algo_container.set_active_algos(active_algos)
    return algo_container


if __name__ == "__main__":
    algo_container = prepare_to_run()
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
