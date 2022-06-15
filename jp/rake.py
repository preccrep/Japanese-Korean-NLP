# use https://github.com/carol975/RAKE_JPN/blob/master/rake.py

import string
import unicodedata

import MeCab
from jpn_stopwords import jpn_stop_words


class Rake:
    def __init__(self):
        self.tagger = MeCab.Tagger("-Owakati")
    
    def remove_punctuation(self,text):
        text = unicodedata.normalize("NFKC", text)  # 全角記号をざっくり半角へ置換（でも不完全）
        # 記号を消し去るための魔法のテーブル作成
        table = str.maketrans("", "", string.punctuation  + "「」、。・※" + string.digits)
        text = text.translate(table)

        return text
        
    def get_word_score(self, word_list):
        freq = {}
        deg = {}

        for word in word_list:
            freq[word] = (freq.get(word) or 0) + 1
            deg[word] = (deg.get(word) or 0) + len(word) - 1 # word length must be > 1 to be considered as a Japanese 'word'
      
        scores = {}
        for word in word_list:
            scores[word] = deg[word]/freq[word]
        
        scores = {k:v for k, v in  sorted(scores.items(), key=lambda item: item[1], reverse=True)}
      
        return scores
    
    def get_keywords(self, text, limit=0):
        parsed_text = self.tagger.parse(text)
        raw_word_list = self.remove_punctuation(parsed_text).split()
        word_list = [word for word in raw_word_list if word not in jpn_stop_words ]
        
        score_list = self.get_word_score(word_list)
        
        if limit == 0:
            return list(score_list.keys())
        else:
            return list(score_list.keys())[:limit]
