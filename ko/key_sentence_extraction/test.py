from krwordrank.sentence import summarize_with_sentences

texts = []

with open('../../data/cleaned/news_contents_cleaned_korean.txt', 'r') as f:
    line = f.readline()
    while line:
        texts.append(line)
        line = f.readline()

print(len(texts))

texts = texts[:100]


keywords, sents = summarize_with_sentences(texts, num_keywords=100, num_keysents=10)
