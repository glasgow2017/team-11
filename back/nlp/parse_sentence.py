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



def get_word_bank(words):
    word_bank = {}
    for word in words:
        if word in word_bank:
            word_bank[word] += 1
        else:
            word_bank[word] = 1

    return word_bank


def rank_word_by_appearance(words, order='acs'):
    word_bank = get_word_bank(words)
    sorted_word_bank = []
    for key, value in sorted(word_bank.iteritems(), key=lambda (k,v): (v,k)):
        sorted_word_bank.append((key, value))
    if order == 'acs':
        return sorted_word_bank
    else:
        return sorted_word_bank[::-1]


def find_top_words(sorted_word_bank, num=10):
    return sorted_word_bank[:num]
