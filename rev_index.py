from dataclasses import dataclass
import nltk
import glob
import re

nltk.download('punkt')

@dataclass
class IndexItem:
    doc_id: int
    doc_occurences: int

def __read_files__():
    files = []
    for path in glob.glob('documents/*.txt'):
        with open(path, encoding='utf-8') as file:
            contents = file.read()
            stripped_contents = re.sub('[^\w ]', '', contents)
            tokenized_content = nltk.word_tokenize(stripped_contents)
            files.append(tokenized_content)
    return files

def build_rev_index(doc_collection):
    index = {}
    doc_maps = map(__index_document__, doc_collection)
    for i, doc_map in enumerate(doc_maps):
        for word_data in doc_map:
            table = index.get(word_data[0], [])
            table.append(IndexItem(i, word_data[1]))
            index[word_data[0]] = table
    return index

def __index_document__(doc):
    index = {}
    for word in sorted(doc):
        index[word] = index.get(word, 0) + 1
    return index.items()

print(build_rev_index(__read_files__()))