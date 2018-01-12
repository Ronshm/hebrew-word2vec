# !/usr/bin/env python
# -*- coding: utf-8 -*-

from api.hebrew_w2v_api import HebrewSimilarWords

obj = HebrewSimilarWords()

print obj.get_similar("בדיקה")
