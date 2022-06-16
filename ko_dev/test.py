from eunjeon import Mecab

tagger = Mecab('/Users/preccrep/opt/anaconda3/lib/python3.8/site-packages/mecab_ko_dic/dicdir') 
list1 = tagger.nouns("고양이가 냐 하고 울면 나는 녜 하고 울어야지")
print(list1)

poem = """
    흘러내린 머리카락이 흐린 호박빛 아래 빛난다.
    유영하며.
    저건가보다.
    세월의 힘을 이겨낸 마지막 하나 남은 가로등.
    미래의 색, 역겨운 청록색으로 창백하게 바뀔 마지막 가로등
    난 유영한다. 차분하게 과거에 살면서 현재의 공기를 마신다.
    가로등이 깜빡인다.

    나도 깜빡여준다.
"""

list2 = tagger.morphs(poem)
print(list2)

list3 = tagger.pos("다람쥐 헌 쳇바퀴에 타고 파")
print(list3)
