import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import re
from collections import Counter
import csv
import string
import itertools
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

EXTERNAL_DATA_PATH = 'data/kamus/emoji'
EXTERNAL_DATA_PATH2='data/kamus/kata'
emoticon_data_path = '{}/emoticon.txt'.format(EXTERNAL_DATA_PATH)
emoticon_df = pd.read_csv(emoticon_data_path, sep='\t', header=None)
emoticon_dict = dict(zip(emoticon_df[0], emoticon_df[1]))

emoji_data_path = '{}/emoji.txt'.format(EXTERNAL_DATA_PATH)
emoji_df = pd.read_csv(emoji_data_path, sep='\t', header=None)
emoji_dict = dict(zip(emoji_df[0], emoji_df[1]))

slang_words = pd.read_csv('{}/slangword.csv'.format(EXTERNAL_DATA_PATH2))
slang_dict = dict(zip(slang_words['original'],slang_words['translated']))

normal_words = pd.read_csv('{}/normalisasi_kata.csv'.format(EXTERNAL_DATA_PATH2))
normal_dict = dict(zip(normal_words['ambigu'],normal_words['terjemahan']))

def translate_emoticon(t):
    for w, v in emoticon_dict.items():
        pattern = re.compile(re.escape(w))
        match = re.search(pattern,t)
        if match:
            t = re.sub(pattern,v,t)
    return t

def remove_username(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text)
    text = re.sub(r'\brt\b', '', text)
    return text

def translate_emoji(t):
    for w, v in emoji_dict.items():
        pattern = re.compile(re.escape(w))
        match = re.search(pattern,t)
        if match:
            t = re.sub(pattern,v,t)
    return t

def remove_newline(text):
    return re.sub('\n', ' ',text)

def repeating_char(text):
    return ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))

def remove_url(text):
    return re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', ' ', text)

def remove_non_alphabet(text):
    output = re.sub('[^a-zA-Z ]+', ' ', text)
    return output

def remove_normal_space(text):
    output = text.replace(" "," ")
    return output

def remove_excessive_whitespace(text):
    return re.sub('  +', ' ', text)

def transform_slang_words(text):
    word_list = text.split()
    word_list_len = len(word_list)
    transformed_word_list = []
    i = 0
    while i < word_list_len:
        if (i + 1) < word_list_len:
            two_words = ' '.join(word_list[i:i+2])
            if two_words in slang_dict:
                transformed_word_list.append(slang_dict[two_words])
                i += 2
                continue
        transformed_word_list.append(slang_dict.get(word_list[i], word_list[i]))
        i += 1
    return ' '.join(transformed_word_list)

def normalisasi_words(text):
    word_list = text.split()
    word_list_len = len(word_list)
    transformed_word_list = []
    i = 0
    while i < word_list_len:
        if (i + 1) < word_list_len:
            two_words = ' '.join(word_list[i:i+2])
            if two_words in normal_dict:
                transformed_word_list.append(normal_dict[two_words])
                i += 2
                continue
        transformed_word_list.append(normal_dict.get(word_list[i], word_list[i]))
        i += 1
    return ' '.join(transformed_word_list)

def stemming(text):
    factory=StemmerFactory()
    stemmer=factory.create_stemmer()
    output=stemmer.stem(text)
    return output

def text_prepocessing(text):
    normal_text=text.lower()
    normal_text=remove_newline(normal_text)
    normal_text=remove_username(normal_text)
    normal_text=remove_url(normal_text)
    normal_text=translate_emoji(normal_text)
    normal_text=translate_emoticon(normal_text)
    normal_text=remove_non_alphabet(normal_text)
    normal_text=remove_excessive_whitespace(normal_text)
    normal_text = repeating_char(normal_text)
    normal_text = normalisasi_words(normal_text)
    normal_text=stemming(normal_text)
    # # normal_text=remove_normal_space(normal_text)
    # # normal_text=transform_slang_words(normal_text)
    return normal_text