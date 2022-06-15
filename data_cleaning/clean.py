import re
import os


if not os.path.exists('../data/split'):
    os.makedirs('../data/split')

if not os.path.exists('../data/cleaned'):
    os.makedirs('../data/cleaned')

# def clean(text):
#     text = text.replace('\n', '')
#     text = text.replace('\r', '')
#     text = text.replace('\t', '')
#     text = text.replace('\u3000', '')
#     text = text.replace('\u0020', '')
#     text = text.replace('\u00a0', '')


def split_data(language):
    src_filename = '../data/raw/' + language + '.txt'
    art_id_filename = '../data/split/art_id_' + language + '.txt'
    news_title_filename = '../data/split/news_title_' + language + '.txt'
    news_contents_filename = '../data/split/news_contents_' + language + '.txt'
    news_date_filename = '../data/split/news_date_' + language + '.txt'

    news = []
    with open(file=src_filename) as f:
        line = f.readline()
        while line:
            line = line.split('\t')
            tmp = []
            for itm in line:
                tmp.append(itm[1:-1])
            news.append(tmp)
            line = f.readline()

    f.close()

    # print(news[0])  # ['art_id', '标题', '正文', '发布时间"']

    news = news[1:]

    news_id = []
    news_title = []
    news_contents = []
    news_date = []
    disabled_data = []

    for line in news:
        if (len(line) < 4):
            disabled_data.append(line)
            continue
        news_id.append(line[0])
        news_title.append(line[1])
        news_contents.append(line[2])
        news_date.append(line[3])

    f = open(art_id_filename, 'w')
    for itm in news_id:
        f.write(itm + '\n')
    f.close()

    f = open(news_title_filename, 'w')
    for itm in news_title:
        f.write(itm + '\n')
    f.close()

    f = open(news_contents_filename, 'w')
    for itm in news_contents:
        f.write(itm + '\n')
    f.close()

    f = open(news_date_filename, 'w')
    for itm in news_date:
        f.write(itm + '\n')
    f.close()

    print(f'{language} data split is done.')


def clean_data(language):
    filename = '../data/split/news_contents_' + language + '.txt'
    cleaned_filename = '../data/cleaned/news_contents_cleaned_' + language + '.txt'

    f1 = open(cleaned_filename, 'w')

    with open(file=filename) as f:
        line = f.readline()
        while line:
            line = line.replace('\n', '').replace('\t', '').replace('\r', '')
            line = re.sub('<.*?>', '', line)
            line = re.sub('\u3000', '', line)
            line = re.sub('\u0020', '', line)
            line = re.sub('\u00a0', '', line)
            line = re.sub(
                '[a-z_A-Z0-9-\.!@#\$%\\\^&\*\)\(\+=\{\}\[\]\/",\'<>~\·`\?:;|]',
                '', line)
            # print(line)
            f1.write(line + '\n')
            line = f.readline()

    f1.close()

    print(f'{language} data cleaning is done.')

if __name__ == '__main__':
    split_data('japanese')
    clean_data('japanese')
    split_data('korean')
    clean_data('korean')


