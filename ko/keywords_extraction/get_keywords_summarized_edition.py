# n is default to 100
import os
from krwordrank.word import summarize_with_keywords

texts = []

# get the tokenized texts (each line split by space)
with open('../../data/tokens/tokenized_text_kor.txt', 'r') as f:
    line = f.readline()
    while line:
        texts.append(line)
        line = f.readline()
f.close()

stopwords = []

with open('../stopwords.txt', 'r') as f:
    line = f.readline()
    while line:
        stopwords.append(line)
        line = f.readline()
f.close()

if not os.path.exists('../../data/keywords/'):
    os.mkdir('../../data/keywords/')

f = open('../../data/keywords/keywords_summarized_kor.txt', 'w')
keywords = summarize_with_keywords(texts, min_count=5, max_length=10,
    beta=0.85, max_iter=10, stopwords=stopwords, verbose=True)
for word, score in sorted(keywords.items(), key=lambda x: -x[1])[:300]:
    if not (word in stopwords):
        f.write(word + ',' + str(score) + '\n')
f.close()

# keywords = summarize_with_keywords(texts, min_count=5, max_length=10,
#     beta=0.85, max_iter=10, stopwords=stopwords, verbose=True)
# keywords = summarize_with_keywords(texts) # with default arguments

