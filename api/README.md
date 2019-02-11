# Hebrew Similar Words API:

In order to Use the API you should import HebrewSimilarWords from api.hebrew_w2v_api,
and download and extract the data from https://drive.google.com/drive/folders/1qBgdcXtGjse9Kq7k1wwMzD84HH_Z8aJt?usp=sharing into the main repo directory.

Functions:

Decleration:

     similar_words = HebrewSimilarWords()
  
Usage:

      similar_words.get_similar("בדיקה", num_results = 10)

Change default number of results:

      similar_words.set_num_results(10)

Full script example (also exist on the repo main dir at api_usage_example.py):

      # !/usr/bin/env python
      # -*- coding: utf-8 -*-

      from api.hebrew_w2v_api import HebrewSimilarWords

      similar_words = HebrewSimilarWords()
      similar_words.set_num_results(10)
      results =  similar_words.get_similar("בדיקה")


The output Format is list of dictionaries (one per word), each dictionary includes "word" and "similarity" fields. The words are sorted in the list by their similarity value (from highest to lowest).
