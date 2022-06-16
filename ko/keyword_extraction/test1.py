from krwordrank.word import summarize_with_keywords

texts = ['예시 문장 입니다', '여러 문장의 list of str 입니다','예시 문장 입니다', '여러 문장의 list of str 입니다','예시 문장 입니다', '여러 문장의 list of str 입니다','예시 문장 입니다', '여러 문장의 list of str 입니다','예시 문장 입니다', '여러 문장의 list of str 입니다','예시 문장 입니다', '여러 문장의 list of str 입니다','예시 문장 입니다', '여러 문장의 list of str 입니다','예시 문장 입니다', '여러 문장의 list of str 입니다',]

stopwords = {'영화', '관람객', '너무', '정말', '보고'}

keywords = summarize_with_keywords(texts, min_count=5, max_length=10,
    beta=0.85, max_iter=10, stopwords=stopwords, verbose=True)
keywords = summarize_with_keywords(texts) # with default arguments

