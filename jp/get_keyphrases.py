import os
# from rake import Rake

# rake = Rake()
# # text = "杉山古墳（すぎやまこふん）は、奈良県奈良市大安寺にある古墳。形状は前方後円墳。大安寺古墳群を構成する古墳の1つ。国の史跡に指定されている（史跡「大安寺旧境内 附 石橋瓦窯跡」のうち）。"

# # text = """
# # 【新華社北京４月２６日】中国国家発展改革委員会（発改委）は２５日、第１四半期（１～３月）の
# # 新規着工プロジェクト数が前年同期に比べ１万２千件増え、計画投資総額も５４・９％増加したと発
# # 表した。同委員会は今年以降、関係方面と連携して投資安定化を着実に進め、有効な投資を積極的に
# # 拡大し、投資の安定成長を推進してきた。第１四半期の全国投資は前年同期比９・３％増加した。伸
# # び率は２０２１年通年を４・４ポイント上回り、好調なスタートとなった。インフラ投資も８・５％
# # 増と高い伸びを維持。１～２月を０・４ポイント上回り、月ごとに増加する傾向を示した。投資構造
# # の改善も進み、ハイテク分野向け投資が２７・０％増と引き続き高い伸びを見せた。投資の活力も高
# # まり、民間投資は８・４％増と伸び率が２０２１年通年をさらに上回った。
# # """

from rake_ja import JapaneseRake, Tokenizer

tok = Tokenizer()
ja_rake = JapaneseRake()

# text = """「人工知能」という名前は1956年にダートマス会議でジョン・マッカーシーにより命名された。
# 現在では、記号処理を用いた知能の記述を主体とする情報処理や研究でのアプローチという意味あいでも使われている。
# 日常語としての「人工知能」という呼び名は非常に曖昧なものになっており、多少気の利いた家庭用電気機械器具の制御システムやゲームソフトの思考ルーチンなどがこう呼ばれることもある。"""

# text = """
# 【新華社北京４月２６日】中国国家発展改革委員会（発改委）は２５日、第１四半期（１～３月）の
# 新規着工プロジェクト数が前年同期に比べ１万２千件増え、計画投資総額も５４・９％増加したと発
# 表した。同委員会は今年以降、関係方面と連携して投資安定化を着実に進め、有効な投資を積極的に
# 拡大し、投資の安定成長を推進してきた。第１四半期の全国投資は前年同期比９・３％増加した。伸
# び率は２０２１年通年を４・４ポイント上回り、好調なスタートとなった。インフラ投資も８・５％
# 増と高い伸びを維持。１～２月を０・４ポイント上回り、月ごとに増加する傾向を示した。投資構造
# の改善も進み、ハイテク分野向け投資が２７・０％増と引き続き高い伸びを見せた。投資の活力も高
# まり、民間投資は８・４％増と伸び率が２０２１年通年をさらに上回った。
# """

# tokens = tok.tokenize(text)
# print(tokens)

# keywords = ja_rake.extract_keywords_from_text(tokens)
# print(keywords)

# phrases = ja_rake.get_ranked_phrases_with_scores()
# print(phrases)

lines = []

with open('../data/cleaned/news_contents_cleaned_japanese.txt', 'r') as f:
    line = f.readline()
    while line:
        lines.append(line)
        line = f.readline()

f.close()

# text = ''.join(lines)

if not os.path.exists('../data/tokens/'):
    os.mkdir('../data/tokens/')

if not os.path.exists('../data/keywords/'):
    os.mkdir('../data/keywords/')

f = open('../data/tokens/tokens_jpn.txt', 'w')

phrases_list = []

for line in lines:
    tokens = tok.tokenize(line)
    keywords = ja_rake.extract_keywords_from_text(tokens)
    phrases = ja_rake.get_ranked_phrases_with_scores()
    phrases_list.append(phrases)
    for token in tokens:
        f.write(token.surface + ',' + token.pos + ',' + token.pos_s1 + ',' +
                token.pos_s2 + ',' + token.pos_s3 + ',' + token.conj + ',' +
                token.form + '\n')
f.close()

print('japanese tokens complete.')

# keywords = ja_rake.extract_keywords_from_text(tokens)

# phrases = ja_rake.get_ranked_phrases_with_scores()

f = open('../data/keywords/keyphrases_jpn.txt', 'w')
for phrases in phrases_list:
    for phrase in phrases:
        f.write(phrase[0] + ',' + phrase[1] + '\n')
f.close()

print('japanese keyphrases complete.')
