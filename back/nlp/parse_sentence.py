import nltk.data
from nltk import word_tokenize
import re
from urllib import urlopen
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib
from textblob import TextBlob

# nltk.download('punkt')

def get_sentences(data):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    return [x.lower() for x in tokenizer.tokenize(data)]

def get_words_from_sentence(sentences):
    regex = re.compile('[^a-zA-Z]')
    words = [x.split(' ') for x in sentences]
    words = [x for s in words for x in s]
    words = [regex.sub('', x) for x in words]
    words = [x.lower() for x in words if len(x) > 0]
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


def rank_word_by_appearance_bank(word_bank, order='acs'):
    sorted_word_bank = []
    for key, value in sorted(word_bank.iteritems(), key=lambda (k,v): (v,k)):
        sorted_word_bank.append((key, value))
    if order == 'acs':
        return sorted_word_bank
    else:
        return sorted_word_bank[::-1]


def find_top_words(sorted_word_bank, num=10):
    return [x[0] for x in sorted_word_bank[:num]]





def get_nouns(text, tags=['NNP', 'NN']):
    blob = TextBlob(text)
    nouns = [word.lower() for word, tag in blob.tags if tag in tags]
    regex = re.compile('[^a-zA-Z]')
    nouns = [regex.sub('', x) for x in nouns]
    nouns = [x for x in nouns if len(x) > 0]
    return nouns

def get_nouns_bank(text):
    nouns = get_nouns(text)
    word_bank = get_word_bank(nouns)
    return word_bank

def get_top_nouns(text, num=10):
    nouns_bank = get_nouns_bank(text)
    sorted_nouns_bank = rank_word_by_appearance_bank(nouns_bank, order='des')
    return find_top_words(sorted_nouns_bank)


''' Find Content
    scope = 1 -> only read this sentence
'''
def search_content(data, key, scope=1):
    sentences = get_sentences(data)
    to_say_sentence = []

    for s in sentences:
        if key.lower() in s:
            to_say_sentence.append(s)

#     flags = [x[1] for x in to_say_sentence]

    return to_say_sentence

''' tag_visible, text_from_html from
    https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
'''
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)
'''end reference'''

def get_text_from_html(to_read_url):
    html = urllib.urlopen(to_read_url).read()
    text = text_from_html(html).lower()
    return text


def find_text_from_html(to_read_url, key):
    text = get_text_from_html(to_read_url)
    return search_content(text, key, scope=1)

def find_top_words_from_html(to_read_url, num=10):
    text = get_text_from_html(to_read_url)
    nouns = get_top_nouns(text, num)
    return nouns

def find_top_words_from_text(text, num=10):
    nouns = get_top_nouns(text, num)
    return nouns

#
# test_url = 'www.google.com'
#
# text = find_text_from_html(test_url, )

def get_webpage_description(to_read_url):
    #template_topic = 'Keywords of this webpage are:'
    #template_wordcount = 'There are around {0} words'

    text = get_text_from_html(to_read_url)
    response = {'topic':'', 'word_count': ''}
    try:
        top_nouns = find_top_words_from_text(text)
        response['topic'] = top_nouns #template_topic + ', '.join(top_nouns)
    except:
        response['topic'] = ''

    try:
        text_length = len(get_words_from_article(text))
        response['word_count'] = text_length #template_wordcount.format(str(text_length))
    except:
        response['word_count'] = ''

    return response


def find_text_from_html(to_read_url, key):
    text = get_text_from_html(to_read_url)
    return search_content(text, key, scope=1)
