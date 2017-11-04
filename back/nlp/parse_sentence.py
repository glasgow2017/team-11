import nltk.data
# nltk.download('punkt')

def get_sentences(data):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    return tokenizer.tokenize(data)

def get_words_from_sentence(sentences):
    regex = re.compile('[^a-zA-Z]')
    words = [x.split(' ') for x in sentences]
    words = [x for s in words for x in s]
    words = [regex.sub('', x) for x in words]
    words = [x for x in words if len(x) > 0]
    return words

def get_words_from_article(article):
    sentences = get_sentences(article)
    return get_words_from_sentence(sentences)
