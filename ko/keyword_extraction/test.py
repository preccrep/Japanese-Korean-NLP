from krwordrank.word import KRWordRank

min_count = 5   # 단어의 최소 출현 빈도수 (그래프 생성 시)
max_length = 10 # 단어의 최대 길이
wordrank_extractor = KRWordRank(min_count=min_count, max_length=max_length)

beta = 0.85    # PageRank의 decaying factor beta
max_iter = 10

# texts = ['예시 문장 입니다', '여러 문장의 list of str 입니다','예시 문장 입니다', '여러 문장의 list of str 입니다','예시 문장 입니다', '여러 문장의 list of str 입니다','예시 문장 입니다', '여러 문장의 list of str 입니다','예시 문장 입니다', '여러 문장의 list of str 입니다','예시 문장 입니다', '여러 문장의 list of str 입니다','예시 문장 입니다', '여러 문장의 list of str 입니다','예시 문장 입니다', '여러 문장의 list of str 입니다',]

texts = []

with open('../../data/cleaned/news_contents_cleaned_korean.txt', 'r') as f:
    line = f.readline()
    while line:
        texts.append(line)
        line = f.readline()

print(len(texts))

texts = texts[:16]


keywords, rank, graph = wordrank_extractor.extract(texts, beta, max_iter)

for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:30]:
    print('%8s:\t%.4f' % (word, r))

# stopwords = {'영화', '관람객', '너무', '정말', '보고'}
# passwords = {word:score for word, score in sorted(
#     keywords.items(), key=lambda x:-x[1])[:300] if not (word in stopwords)}



