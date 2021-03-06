import string
import re
from nltk.tokenize import word_tokenize
from itertools import chain

def text_cleansing(title):
    table = str.maketrans(string.punctuation, ' '*len(string.punctuation)) #map punctuation to space
    
    title = title.lower()
    title = re.sub('(\d+)([a-zA-Z]+)', r'\1 \2', title)
    title = re.sub('\]', r' ] ', title)
    title = re.sub('\[', r' [ ', title)
    title = title.translate(table)
    title = re.sub(r'[^(a-z|A-Z|0-9)]', ' ', title)
    title = " ".join(title.split())
    
    return title
  
def data_text_prep(d_train):
    d_train = d_train.copy()
  
    # tokenize
    d_train.loc[:, 'text_token'] = d_train.text.apply(word_tokenize)
    
    title_token = list(chain(*d_train.text_token.tolist()))
    vocab_token = list(set(title_token))
    vocab_token.sort()

    word2idx = dict((w, k) for k, w in enumerate(vocab_token, 2))
    idx2word = dict((k, w) for k, w in enumerate(vocab_token, 2))

    word2idx['<UNK>'] = 1
    idx2word[1] = '<UNK>'
    word2idx['<PAD>'] = 0
    idx2word[0] = '<PAD>'
    
    return word2idx, idx2word


