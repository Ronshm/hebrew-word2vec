from pathes import Path
from w2v_algo import Algo


class HebrewSimilarWords:
    def __init__(self):
        self.algo = Algo(Path.path_w2v_twitter, "w2v twitter")
        self._num_results = 10
        # self.algo_container = AlgoContainer()
        # self.algo_container.add_algo(Algo)
        # algo_container.add_algo(Algo(Path.path_w2v_twitter, "w2v twitter", False, True))
        # active_algos = ["fastText"]
        # active_algos = ["w2v twitter"]
        # self.algo_container.set_active_algos(active_algos)

    def set_num_results(self, num_results):
        self._num_results = num_results

    def get_similar(self, word):
        algos_similarity_results = self.algo.search_similar(word, self._num_results)
        return algos_similarity_results[word]
