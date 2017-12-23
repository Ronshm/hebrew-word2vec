search_result_file = 'search_results.txt'
analogy_result_file = 'analogy_results.txt'

MAX_RESULTS_PRINT_TO_FILE = 5
DEFAULT_NUM_RESULTS = 10

# todo enum class
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

menu_text = '''
        <i size="7"><strong> Hebrew Word2Vec<br><br></strong></i>
        <form action="choose_algo" method="post">
        <input type="submit" value="Select which algorithms to show">
        </form>

         <form action="update_num_results" method="post">
          Number of results to show (between 3 and 15), default is 10:
          <input type="number" name="num_results" min="3" max="15">
          <input value="Search" type="submit" />
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
