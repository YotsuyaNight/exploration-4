from dataclasses import dataclass
import glob
import re

@dataclass
class IndexItem:
    doc_id: str
    doc_occurences: int

def read_all_documents():
    files = {}
    for path in glob.glob('scrapped_data/documents/*.txt'):
        with open(path, encoding='utf-8') as file:
            id = re.search("\\\\(.+)\.txt", path).groups()[0]
            contents = file.read().split("\n")
            files[id] = contents
    return files

def fetch_phrase_freq_from_index(index, phrase, id):
    if phrase in index:
        for item in index[phrase]:
            if item.doc_id == id:
                return item.doc_occurences
    return 0

def build_rev_index(doc_collection):
    index = {}
    doc_maps = dict((id, __summarize_doc_words__(contents)) for id, contents in doc_collection.items())
    for id, doc_map in doc_maps.items():
        for word_data in doc_map:
            table = index.get(word_data[0], [])
            table.append(IndexItem(id, word_data[1]))
            index[word_data[0]] = table
    return index

def __summarize_doc_words__(doc):
    index = {}
    for word in sorted(doc):
        index[word] = index.get(word, 0) + 1
    return index.items()
