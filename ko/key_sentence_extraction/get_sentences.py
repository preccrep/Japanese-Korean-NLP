# the project does not use this file
# this is just an example of how to get key sentences
from krwordrank.sentence import summarize_with_sentences

texts = []

# get the tokenized texts (each line split by space)
with open('../../data/tokens/tokenized_text_kor.txt', 'r') as f:
    line = f.readline()
    while line:
        texts.append(line)
        line = f.readline()
f.close()

texts = texts[:10]


keywords, sents = summarize_with_sentences(texts, num_keywords=100, num_keysents=10)

for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:30]:
    print('%8s:\t%.4f' % (word, r))
