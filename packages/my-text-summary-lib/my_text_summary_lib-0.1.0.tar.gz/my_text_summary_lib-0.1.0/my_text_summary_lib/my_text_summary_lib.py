# my_text_summary_lib/my_text_summary_lib.py

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from nltk.tokenize.treebank import TreebankWordDetokenizer

nltk.download('stopwords')
nltk.download('punkt')

def summarize_text(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    stop_words = set(stopwords.words('english'))
    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]

    freq_dist = FreqDist(filtered_words)
    most_common_words = freq_dist.most_common(5)

    summary = TreebankWordDetokenizer().detokenize([word for word, _ in most_common_words])

    return summary
