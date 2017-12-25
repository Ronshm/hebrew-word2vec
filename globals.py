search_result_file = 'search_results.txt'
analogy_result_file = 'analogy_results.txt'

MAX_RESULTS_PRINT_TO_FILE = 5
DEFAULT_NUM_RESULTS = 10

menu_text = '''
        <i size="7"><strong> Hebrew Word2Vec<br><br></strong></i>

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


        <form action="choose_algo" method="post">
        <input type="submit" value="Select which algorithms to show">
        </form>

        <form action="update_num_results" method="post">
          Number of results to show (between 3 and 15), default is 10:
        <input type="number" name="num_results_to_show" min="3" max="15"/>
        <input value="Set" type="submit" />
        </form>
        '''
