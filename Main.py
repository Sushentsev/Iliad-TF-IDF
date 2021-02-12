import requests
from PoemSplitter import PoemSplitter
from CorpusProcessor import CorpusProcessor
from PoemSplitter import PoemSplitter


def read_file(filepath: str) -> str:
    response = requests.get(filepath)
    return response.text


if __name__ == '__main__':
    url = 'http://www.lib.ru/POEEAST/GOMER/gomer01.txt'
    corpus = read_file(url)
    splitter = PoemSplitter()
    processor = CorpusProcessor()
    corpus = splitter.split_text(corpus)
    corpus = processor.proccess_corpus(corpus)
    tf_idf = processor.calculate_tf_idf(corpus)
    processor.save(tf_idf, './Poems_TFIDF')
