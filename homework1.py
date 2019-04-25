# file: homework1.py
# author: Ishan Gupta

# imports
import os
from collections import defaultdict
from nltk.stem.porter import *
import numpy as np
import pandas as pd
import sys


# returns count of unique words in the document
def unique_words_count(word_dict):
    return len(word_dict.keys())


# returns the total number of processed word tokens
def total_processed_tokens(word_dict):
    sum = 0

    for key, val in word_dict.items():
        sum += val

    return sum


# returns the count of words occurring only once
def once_occurring_word_count(word_dict):
    count = 0

    for key, val in sorted(word_dict.items(), key=lambda kv: (kv[1], kv[0])):
        if val <= 1:
            count += 1
        else:
            break

    return count


# returns the term frequency of top 30 words in
# database.
def get_tf_top_30(word_dict):
    top_30_tokens = []
    i = 0

    for key, val in sorted(word_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
        if i < 30:
            top_30_tokens.append((key, val))
            i += 1
        else:
            break

    return top_30_tokens


# returns document frequency of text of top 30 words
# in database.
def get_dft_top_30(text_post_processing, word_tf):
    word_dft = []

    for value in word_tf:
        count = 0
        for key, val in text_post_processing.items():
            if value[0] in val:
                count += 1
        word_dft.append((value[0], count))

    return word_dft


# returns weighted term frequency of top 30 words
# in database.
def get_weighted_tf_top_30(word_tf):
    word_weight_tf = []

    for value in word_tf:
        if value[1] == 0:
            word_weight_tf.append((value[0], 0))
        else:
            word_weight_tf.append((value[0], 1 + np.log10(value[1])))

    return word_weight_tf


# returns inverse document frequency of top 30 words
# in the database.
def get_idf_top_30(word_dft):

    word_idf = []

    for val in word_dft:
        word_idf.append((val[0], np.log10(404.0 / val[1])))

    return word_idf


# returns tf*idf of top 30 words in the database.
def get_tf_multiplied_idf_top_30(word_tf, word_idf):
    word_tf_idf = []

    for i in range(0, 30):
        word_tf_idf.append((word_tf[i][0], word_tf[i][1]*word_idf[i][1]))

    return word_tf_idf


# returns probabilities of top 30 words in the database.
def get_probabilities_top_30(word_tf, word_dict):
    total_tokens = total_processed_tokens(word_dict)
    word_probabilities = []

    for val in word_tf:
        word_probabilities.append((val[0], val[1] / total_tokens))

    return word_probabilities


# path of the documents.
document_path = sys.argv[1]

###################################################
# this block of code collects the tokens which are
# present in the documents without pre processing.
all_data = defaultdict(dict)
total_count_before_processing = 0

for files in os.listdir(document_path):
    file_name = os.path.join(document_path, files)
    with open(file_name, 'r') as file:
        word_count = {}
        for line in file:
            new_line = line.strip().split(' ')
            total_count_before_processing += len(new_line)
            for word in new_line:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
    all_data[file_name] = word_count
###################################################


###################################################
# this block of code creates a set of stop words
# which are used in the text processing of tokens.
stop_words_path = sys.argv[2]
stop_words = set()
with open(stop_words_path, 'r') as file:
    for line in file:
        new_line = line.strip()
        stop_words.add(str(new_line))
###################################################


###################################################
# this block of code produces a dictionary of dictionaries
# of tokens and their frequencies in related documents.
# the structure is of the form -
# { 'document_name' : {'word_token' : frequency}}
text_post_processing = defaultdict(dict)
stemmer = PorterStemmer()
for files in os.listdir(document_path):
    file_name = os.path.join(document_path, files)
    with open(file_name, 'r') as file:
        word_count = {}
        for line in file:
            after_punctuation = re.sub('[^\w\s]', '', line.strip().lower()).split()
            stemmed = [stemmer.stem(str(word)) for word in after_punctuation]
            new_line = [str(x) for x in stemmed if str(x) not in stop_words]
            for word in new_line:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
    text_post_processing[file_name] = word_count
###################################################


###################################################
# this block of code creates a database of all the
# word tokens present in all the files and their
# cumulative frequency.
word_dict = {}

for key, val in text_post_processing.items():
    for word, freq in val.items():
        if word in word_dict:
            word_dict[word] += freq
        else:
            word_dict[word] = freq
###################################################


if __name__ == '__main__':
    word_tf = get_tf_top_30(word_dict)

    word_dft = get_dft_top_30(text_post_processing, word_tf)

    word_weight_tf = get_weighted_tf_top_30(word_tf)

    word_idf = get_idf_top_30(word_dft)

    word_tf_idf = get_tf_multiplied_idf_top_30(word_tf, word_idf)

    word_probabilities = get_probabilities_top_30(word_tf, word_dict)

    final_calculations = []
    col = ("Term", "Tf", "Tf(weight)", "df", "IDF", "tf*idf", "p(term)")
    for i in range(0, 30):
        final_calculations.append((word_tf[i][0], word_tf[i][1],  word_weight_tf[i][1], word_dft[i][1],
              word_idf[i][1], word_tf_idf[i][1], word_probabilities[i][1]))

    dataframe = pd.DataFrame(final_calculations, columns=col)

    print("1.1 Tokens before processing : {}".format(total_count_before_processing))

    print("1.2 Tokens after processing : {}".format(total_processed_tokens(word_dict)))

    print("2. The number of unique words in the database : {}".format(unique_words_count(word_dict)))

    print("3. The number of words that occur only once in the database : {}".format(once_occurring_word_count(word_dict)))

    print("4. The average number of word tokens per document : {:f}".format(total_processed_tokens(word_dict) / 404.0))

    print("5. For 30 most frequent words in the database :")
    print (dataframe.to_string(index=False))