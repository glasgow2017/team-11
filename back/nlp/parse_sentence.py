import nltk.data
# nltk.download('punkt')

def get_sentences(data):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    print tokenizer.tokenize(data)
