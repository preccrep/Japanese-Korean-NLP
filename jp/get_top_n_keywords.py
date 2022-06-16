import os
from rake import Rake

rake = Rake()
# text = "杉山古墳（すぎやまこふん）は、奈良県奈良市大安寺にある古墳。形状は前方後円墳。大安寺古墳群を構成する古墳の1つ。国の史跡に指定されている（史跡「大安寺旧境内 附 石橋瓦窯跡」のうち）。"

lines = []

with open('../data/cleaned/news_contents_cleaned_japanese.txt', 'r') as f:
    line = f.readline()
    while line:
        lines.append(line)
        line = f.readline()

f.close()

text = ''.join(lines)

if not os.path.exists('../data/keywords/'):
    os.mkdir('../data/keywords/')

n = 50  # number of keywords

f = open('../data/keywords/keywords_jpn.txt', 'w')
# for line in lines:
#     keywords = rake.extract(line, n)
#     for keyword in keywords:
#         print(keyword)
#         # f.write(keyword + '\n')
keywords = rake.get_keywords(text, n)
for keyword in keywords:
    f.write(keyword + '\n')
f.close()

print('japanese keywords complete.')
