import spacy
from spacy.lang.ja import Japanese


# nlp = spacy.load("ja_core_news_lg", disable=["tagger", "parser", "attribute_ruler", "lemmatizer"])
nlp = spacy.load("ja_core_news_lg")


filename='../data/output/jp_contents.txt'
contents=[]
with open(filename) as f:
    line=f.readline()
    while line:
        contents.append(line)
        line=f.readline()

contents=contents[2:3]

TRAIN_DATA = []

for line in contents:
    doc=nlp(line)
    entities=[]
    for e in doc.ents:
        label,start,end=e.label_,e.start,e.end
        entities.append((start,end,label))
    TRAIN_DATA.append((line, {'entities': entities}))

# print(TRAIN_DATA)


# train a spaCy model
import random
# from spacy.tokens import DocBin


# nlp=spacy.blank('ja')
# db=DocBin()


# for text, annotations in TRAIN_DATA:
#     doc = nlp(text)
#     ents = []
#     for start, end, label in annotations:
#         span = doc.char_span(start, end, label=label)
#         ents.append(span)
#     print(ents)
#     doc.ents = ents
#     db.add(doc)
# db.to_disk("./train.spacy")

from spacy.training import Example


def main(model=None, output_dir = None, n_iter=1):   ##参数意义，model：是否存在现有的模型，output_dir：模型存储位置，n_iter迭代次数
    """Load the model, set up the pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model  ###这里的作用是对现有的模型进行优化  *非常重要
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('ja')  # create blank Language class
        print("Created blank 'ja' model")

    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe('ner', last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe('ner')

    # add labels
    for _, annotations in TRAIN_DATA:      # 添加train data的标签
        for ent in annotations.get('entities'):
            # print(ent)
            ner.add_label(ent[2])

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # 仅训练标注的标签，假如没有则会对所有的标签训练，
                                           #建议不要对下载的spacy的模型进行训练可能导致下载的语言模型出错，训练一个空白语言模型就好
        optimizer = nlp.begin_training()   ##模型初始化
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)     ##训练数据每次迭代打乱顺序
            losses = {}                    ##定义损失函数
            for text, annotations in TRAIN_DATA:
                example = Example.from_dict(nlp.make_doc(text), annotations)    ##对数据进行整理成新模型需要的数据
                print("example:",example)
                nlp.update(
                    [example],  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # 更新权重
                    losses=losses)
            print(losses)

    # 保存模型
    if output_dir is not None:
        # output_dir = Path(output_dir)
        # if not output_dir.exists():
        #     output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

main(output_dir='../data/model')

