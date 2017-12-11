#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import *
from utils import *

#
# reload(sys)
# sys.setdefaultencoding('utf-8')

search_result_file = 'search_results.txt'
analogy_result_file = 'analogy_results.txt'
global active_algos

menu_text = '''
        <i size="7"><strong> Hebrew Word2Vec<br><br></strong></i>
        <form action="choose_algo" method="post">
        <input type="submit" value="Select which algorithms to show">
        </form>
	<b size = '7'> <br>Please notice that the algorithm is designed to work for Hebrew words only.<br><br></b>
        <b size="6"> Analogies:<br></b>
	<p size = '5'>This algorithm helps to search for analogies.<br><br> word1 : word2 = word3 : ?<br><br> For example:<br>France : Paris = Japan : Tokyo<br></p>
        <form action="analogy" method="post">
            Enter word1: <input name="word1" type="text" />
            Enter word2: <input name="word2" type="text" />
            Enter word3: <input name="word3" type="text" />
            <input value="Search" type="submit" />
        </form>
        <b size="6"><br><br>Similar words:<br></b>
	<p size = 5>This algorithm helps to search for similar words.<br></p>
        <form action="similar" method="post">
            Enter word: <input name="wanted" type="text" />
            <input value="Search" type="submit" />
        </form>
    '''


@get('')
@get('/')  # @route('/login')
@get('/cyber')
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


@post('/similar')
@get('/similar')
def search():
    # print active_algos
    f = open(search_result_file, 'a')
    wanted = request.forms.get('wanted')
    if not wanted:
        return "<p size='4'>Please enter a word</p>"
    text = menu_text
    text += "<p align='center'><b  size='5'>Current searching for words similar to-&nbsp&nbsp&nbsp" + wanted + "</b><br>"
    f.write("\n\nCurrent searching for words similar to:" + wanted + "\n")
    for algo in active_algos:
        cur_algo_words = words_dict[algo]
        cur_algo_vectors = vectors_dict[algo]
        f.write("Algo: " + algo + "\n")
        text += "<b align = 'center'><br> Algorithm: " + algo + "</b><br>"
        try:
            wanted_ind = cur_algo_words.index(as_appears_in_algo(wanted))
        except:
            wanted_ind = []
            if multi_pos_dict[algo]:
                for i, word in enumerate(cur_algo_words):
                    parts = word.split('_')
                    if len(parts) > 1 and parts[1] == wanted:
                        if len(parts) > 1 and parts[1] == wanted:
                            wanted_ind.append(i)
                            print cur_algo_words[i]
            if len(wanted_ind) == 0:
                text += wanted + " is unknown, sorry."
                continue
        if not isinstance(wanted_ind, list):
            wanted_ind = [wanted_ind]
        for word_ind in wanted_ind:
            text += "<br>Showing results for " + as_appear_in_site(cur_algo_words[word_ind]) + '<br><br>'
            inds, sims = top_similar(cur_algo_vectors[word_ind], cur_algo_vectors)
            for i in range(len(inds)):
                text += "similarity::" + str(sims[i]) + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" + \
                        as_appear_in_site(cur_algo_words[inds[i]]) + "<br>"
                if i > 0 and i < 5:
                    f.write(cur_algo_words[inds[i]] + "\n")
    return text + "</p>"


@post('/analogy')
@get('/analogy')
def analogy():
    f = open(analogy_result_file, 'a')
    word1 = request.forms.get('word1')
    word2 = request.forms.get('word2')
    word3 = request.forms.get('word3')
    if (not word1) or (not word2) or (not word3):
        return "<p size='4'>Please enter all the words.</p>"
    text = menu_text
    text += "<p align='center'><b  size='6'>Current looking for:<br>" + word3 + " : word" + "<br>=<br>" + word2 + " : " + word1 \
            + "</b><br>"
    f.write("\n\nCurrent looking for:" + word3 + " : word = " + word2 + " : " + word1 + "\n")
    for algo in active_algos:
        cur_algo_words = words_dict[algo]
        cur_algo_vectors = vectors_dict[algo]
        flag = 0
        text += "<br> <b size='4'>Algorithm: " + algo + "</b><br><br>"
        f.write("Algo: " + algo + "\n")
        try:
            word1_idx = cur_algo_words.index(as_appears_in_algo(word1))
        except:
            flag = 1
            text += word1 + " is unknown, sorry."
        try:
            word2_idx = cur_algo_words.index(as_appears_in_algo(word2))
        except:
            flag = 1
            text += word2 + " is unknown, sorry."
        try:
            word3_idx = cur_algo_words.index(as_appears_in_algo(word3))
        except:
            flag = 1
            text += word3 + " is unknown, sorry."
        if not flag:
            wanted = cur_algo_vectors[word3_idx] - cur_algo_vectors[word1_idx] + cur_algo_vectors[word2_idx]
            inds, sims = top_similar(wanted, cur_algo_vectors)
            for i in range(len(inds)):
                text += "similarity::" + str(sims[i]) + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" + \
                        as_appear_in_site(cur_algo_words[inds[i]]) + "<br>"
                if i < 5:
                    f.write(cur_algo_words[inds[i]] + "\n")
    return text + "</p>"


def add_algorithm(path, name, multi_pos_flag=0):
    path = os.path.join('result', path)
    if not os.path.exists(os.path.join(path, "words_list.txt")):
        organize_data(path)
    with open(os.path.join(path, "words_list.txt"), 'r') as f:
        cur_words = f.readlines()
    cur_words = [word[:-1] for word in cur_words]
    cur_vecs = np.load(os.path.join(path, "words_vectors.npy"))
    words_dict[name] = cur_words
    vectors_dict[name] = cur_vecs
    multi_pos_dict[name] = multi_pos_flag


def main():
    global active_algos
    add_algorithm(path_FT, "fastText")
    add_algorithm(path_w2v, "w2v")
    # add_algorithm(path_FT_seg, "fastText seg")
    # add_algorithm(path_w2v_nn_win5, "w2v nn win 5")
    # add_algorithm(path_w2v_seg, "w2v seg")
    # add_algorithm(path_w2v_nn_win3, "w2v nn win 3")
    # add_algorithm(path_w2v_nn_win10, "w2v nn win 10")
    # add_algorithm(path_w2v_nn_win5_neg10, "w2v nn win 5 neg 10")
    add_algorithm(path_w2v_multi_pos, "w2v multi pos", 1)
    add_algorithm(path_FT_multi_pos, "fastText multi pos", 1)
    # add_algorithm(path_FT_nn, "fastText nn")
    add_algorithm(path_FT_nn_filtered, "fastText nn filtered")
    add_algorithm(path_w2v_nn_filtered, "w2v nn filtered")
    add_algorithm(path_odeds_algo_200, "Oded's algorithm 200 dim feature")
    add_algorithm(path_odeds_algo, "Oded's algorithm")
    add_algorithm(path_w2v_nn_pos_10, "w2v main (nn&pos) 10 feat", 1)
    add_algorithm(path_w2v_nn_pos_100, "w2v main (nn&pos) 100 feat", 1)
    add_algorithm(path_w2v_nn_pos_200, "w2v main (nn&pos) 200 feat", 1)
    active_algos = ["w2v main (nn&pos) 100 feat", "Oded's algorithm", "fastText multi pos", "w2v multi pos"]
    active_algos = sorted(active_algos)
    # run(host='77.126.119.142', port=80, debug=True)
    # run(host='192.168.1.15', port=80, debug=True)
    # run(host='localhost', port=7765, debug=False)
    run(host='', port=7765, debug=False)
    # run(host='132.71.121.195', port=8079, debug=False)


if __name__ == "__main__":
    words_dict = {}
    vectors_dict = {}
    multi_pos_dict = {}
    main()
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
