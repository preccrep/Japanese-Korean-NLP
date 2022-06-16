import spacy

def load_model_test(path,text):
    nlp = spacy.load(path)
    print("Loading from", path)
    doc = nlp(text)
    for i in doc.ents:
        print(i.text,i.label_)

test_text='【新華社北京４月２６日】中国国家発展改革委員会（発改委）２５日、第１四半期（１～３月）新規着工プロジェクト数前年同期比べ１万２千件増え、計画投資総額５４・９％増加発表。同委員会今年以降、関係方面連携投資安定化着実進め、有効投資積極的拡大、投資安定成長推進。第１四半期全国投資前年同期比９・３％増加。伸び率２０２１年通年４・４ポイント上回り、好調スタート。インフラ投資８・５％増高い伸び維持。１～２月０・４ポイント上回り、月増加傾向示し。投資構造改善進み、ハイテク分野向け投資２７・０％増引き続き高い伸び見せ。投資活力高まり、民間投資８・４％増伸び率２０２１年通年上回っ。'

model_dir='../data/output/model'
load_model_test(model_dir,test_text)
