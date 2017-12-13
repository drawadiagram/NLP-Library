# Prepare docs for lda

import re
import os
import string
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus.reader.plaintext import PlaintextCorpusReader as plaincorp
# from sklearn.feature_extraction.text import CountVectorizer

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

def clean(my_string):
    """Clean a string.
    This function cleans a string, not a file.
    """
    p = re.compile('[0-9]')

#   stop_free is a string with no stop words and no CRs
#   split() forces read as a list of words instead of a string. this is clever.
#   stop words are removed a word at a time
    stop_free = ' '.join(i for i in my_string.lower().split() if i not in stop)
#   numb_free is a string with no numbers.
#   no split means string is read one char at a time, hence the simple regex
    numb_free = ''.join(i for i in stop_free if not p.match(i))
#   again, reading one char at a time since the punctuation chars are all single
#   with the peculiar exception of '\\' which in fact is still a single char
#   try this with a generator if you don't believe me
    punc_free = ''.join(i for i in numb_free if i not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split() if len(lemma.lemmatize(word))>1)
    return normalized

def anticlean(my_string):
    """Clean a string.
    This function cleans a string, not a file.
    """
    p = re.compile('^[0-9]+$')
    stops = " ".join([i for i in my_string.lower().split() if i in stop])
    numbs = ''.join(i for i in my_string.lower().split() if p.match(i))
    puncs = ''.join(i for i in my_string.lower().split() if i in exclude)
    shorts = " ".join(word for word in my_string.lower().split() if len(lemma.lemmatize(word))>1)
    return ' '.join(s)

# doc_clean = [clean(doc).split() for doc in doc_complete]

# ROUGHLY
# 1 - clean docs
def clean_dir(input_dir, output_dir):
    my_docs = [i for i in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir,i))]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for doc in my_docs:
        docname = os.path.basename(os.path.splitext(doc)[0])
        with open(os.path.join(input_dir, doc)) as f:
            myfile = f.read()
            with open(os.path.join(output_dir,'%s-clean.txt' % docname), 'w+') as g:
                g.write(clean(myfile))

my_docs_dir = '/home/mason/topics/swedish'
my_output_dir = '/home/mason/topics/swedish/cleaned'
clean_dir(my_docs_dir,my_output_dir)

# 2 - create corpus file with nltk and use it to vectorize contents.
my_corpus = plaincorp(my_output_dir, '.*')

# 3 - load up some data structures for package LDA
#   including Document-Term Matrix, Titles, and Vocab
#   a) create a Vocab
#   b) create a numpy array like [doc number, vocab freq counts]
#   Note this is probably very inefficient, and is for education only.
my_vocab = tuple(set(my_corpus.words()))
my_titles = tuple(list(my_corpus.fileids()))
my_freq = np.array([[list(my_corpus.words(i)).count(j) for j in my_vocab] for i in my_corpus.fileids()])
