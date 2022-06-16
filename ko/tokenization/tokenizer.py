import os
import mecab_ko as MeCab

# tagger = MeCab.Tagger("-Owakati")
# print(tagger.parse("아버지가방에들어가신다").split())

# tagger = MeCab.Tagger()
# print(tagger.parse("아버지가방에들어가신다"))

from collections import namedtuple

Morpheme = namedtuple("Morpheme", "surface pos pos_s1 pos_s2 pos_s3 conj form")


class Tokenizer:
    def __init__(self, **kwargs):
        self.__mecab = MeCab.Tagger(**kwargs)
        self.__mecab.parse("Initialize parse.")

    def tokenize(self, text):
        return [m for m in self.__iter_morpheme(text)]

    def __iter_morpheme(self, text):
        node = self.__mecab.parseToNode(text)
        node = node.next
        while node.next:
            surface = node.surface
            features = node.feature.split(",")

            yield Morpheme(surface, *features[:6])

            node = node.next


tok = Tokenizer()

# text = '나이로비신화통신바이린기자중국스마트폰제조사오포가일케냐에리노를출시했다오포관계자는이번에출시된리노를전자상거래플랫폼에서사전주문할수있다고밝혔다그는리노는초고속모바일인터넷으로케냐의사진기술모바일엔터테인먼트소비자경험등을한단계끌어올려줄것이라고덧붙였다한편또다른중국스마트폰제조업체인화웨이는케냐모바일및인터넷서비스제공업체인사파리콤의네트워크구축을위한파트너로선정된것으로알려졌다'

# tokens = tok.tokenize(text)
# for token in tokens:
#     print(token)

lines = []

with open('../../data/cleaned/news_contents_cleaned_korean.txt', 'r') as f:
    line = f.readline()
    while line:
        lines.append(line)
        line = f.readline()

f.close()

tokenized_text = []

if not os.path.exists('../../data/tokens/'):
    os.mkdir('../../data/tokens/')

# write tokens to file
f = open('../../data/tokens/tokens_kor.txt', 'w')

for line in lines:
    tokens = tok.tokenize(line)
    token_list = []
    for token in tokens:
        token_list.append(token.surface)
        f.write(token.surface + ',' + token.pos + ',' + token.pos_s1 + ',' +
                token.pos_s2 + ',' + token.pos_s3 + ',' + token.conj + ',' +
                token.form + '\n')
    tokenized_text.append(' '.join(token_list))

f.close()

print('korean tokens complete.')

# write tokenized text to file
f = open('../../data/tokens/tokenized_text_kor.txt', 'w')

for line in tokenized_text:
    f.write(line + '\n')

f.close()

print('korean tokenization complete.')
