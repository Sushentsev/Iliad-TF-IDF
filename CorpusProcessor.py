from typing import List, DefaultDict, Set
from collections import defaultdict
from math import log2
import re
import pandas as pd
import os


class CorpusProcessor:
    def _process_document(self, document: List[str]) -> List[str]:
        processed_document = []
        for line in document:
            line = line.strip()
            line = re.split(";|,-|,| - |:|\.| |!|\?|\(|\)|\"|\'", line)
            line = [word.lower() for word in line if word.strip() and not word.isdigit()]
            processed_document.extend(line)

        return processed_document

    def proccess_corpus(self, corpus: List[List[str]]) -> List[List[str]]:
        processed_corpus = []
        for document in corpus:
            processed_document = self._process_document(document)
            processed_corpus.append(processed_document)

        return processed_corpus

    def _get_words(self, corpus: List[List[str]]) -> Set[str]:
        words = set()
        for document in corpus:
            words.update(set(document))

        return words

    def _get_words_occurences(self, corpus: List[List[str]]) -> DefaultDict[str, Set[int]]:
        words_occurrences = defaultdict(set)
        for doc_index, document in enumerate(corpus):
            for word in document:
                words_occurrences[word].add(doc_index)

        return words_occurrences

    def _calucale_tf(self, document: List[str]) -> DefaultDict[str, float]:
        tf = defaultdict(float)
        for word in document:
            tf[word] += 1

        for word in tf:
            tf[word] /= len(document)

        return tf

    def _calculate_idf(self, corpus: List[List[str]]) -> DefaultDict[str, float]:
        words = self._get_words(corpus)
        words_occurrences = self._get_words_occurences(corpus)
        idf = defaultdict(int)
        for word in words:
            idf[word] = log2(len(corpus) / len(words_occurrences[word]))

        return idf

    def calculate_tf_idf(self, corpus: List[List[str]]) -> DefaultDict[int, DefaultDict[str, float]]:
        tf_idf = defaultdict(defaultdict)
        idf = self._calculate_idf(corpus)

        for doc_index, document in enumerate(corpus):
            tf = self._calucale_tf(document)
            for word in set(document):
                tf_idf[doc_index][word] = tf[word] * idf[word]

        return tf_idf

    def save(self, tf_idf: DefaultDict[int, DefaultDict[str, float]], path: str):
        for poem_index, poem in enumerate(tf_idf):
            df = pd.DataFrame.from_dict(tf_idf[poem], orient='index')
            df = df.reset_index()
            df.columns = ['Words', 'TF-IDF']
            df = df.sort_values(by=['TF-IDF'], ascending=False)

            if not os.path.exists(path):
                os.mkdir(path)

            df.to_csv(f'{path}/Poem_{poem_index + 1}.csv', index=False)
