# Get Tokens and Keyphrases

```
> cd jpn_ke
> python get_keyphrases.py
```
Then a file in the path `../data/tokens/tokens_jpn.txt` will be created, and tokens will be saved in the format as below:

```
【,補助記号,括弧開,*,*,*,*
新華,名詞,固有名詞,一般,*,*,*
社,名詞,普通名詞,助数詞可能,*,*,*
北京,名詞,固有名詞,地名,一般,*,*
４,名詞,数詞,*,*,*,*
月,名詞,普通名詞,助数詞可能,*,*,*
２６,名詞,数詞,*,*,*,*
日,接尾辞,名詞的,助数詞,*,*,*
】,補助記号,括弧閉,*,*,*,*
中国,名詞,固有名詞,地名,国,*,*
国家,名詞,普通名詞,一般,*,*,*
発展,名詞,普通名詞,サ変可能,*,*,*
改革,名詞,普通名詞,サ変可能,*,*,*
委員,名詞,普通名詞,一般,*,*,*
会,名詞,普通名詞,一般,*,*,*
（,補助記号,括弧開,*,*,*,*
発,記号,一般,*,*,*,*
```

It also saves the keyphrases file in the path `../data/rake/keyphrases_jpn.txt` in the format as below:

```
33.0,中国 国家 発展 改革 委員 会
29.75,新華 社 北京 ４ 月 ２６
14.666666666666666,１ 万 ２千 件
13.5,前年 同期 比 ９
12.0,同 委員 会
9.0,５ ％ 増
9.0,４ ％ 増
9.0,２０２１ 年 通年
9.0,着工 プロジェクト 数
8.833333333333334,９ ％ 増加
8.666666666666666,１ 四半 期
8.0,０ ％ 増
8.0,計画 投資 総額
7.833333333333334,３ ％ 増加
6.0,前年 同期
```

where the first column is the score of each phrase and the rest is the tokenized keyphrase.

# Get the Top n Keywords

To get the top n keywords, you only need to run:

```
> python get_top_n_keywords.py
```

in which `n` is default to 50, and you can modify it in the `get_top_n_keywords.py` file.
